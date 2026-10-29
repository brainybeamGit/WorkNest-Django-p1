import calendar as pycalendar
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from io import BytesIO

import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import Booking, Invoice, Payment, Subscription, Workspace

DAY_START = time(9, 0)
DAY_END = time(18, 0)
DAY_HOURS = Decimal('9')


def razorpay_ready():
    return bool(settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET)


def rzp_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


def booking_hours(booking):
    start = datetime.combine(booking.booking_date, booking.start_time)
    end = datetime.combine(booking.booking_date, booking.end_time)
    return Decimal(str(round((end - start).total_seconds() / 3600, 2)))


def member_free_hours(user):
    today = timezone.localdate()
    subs = Subscription.objects.filter(
        member=user, status='Active', end_date__gte=today
    ).select_related('plan')
    if not subs:
        return Decimal('0')
    total = Decimal(sum(s.plan.free_hours for s in subs))
    since = min(s.start_date for s in subs)
    used = Booking.objects.filter(
        member=user, created_at__date__gte=since
    ).exclude(status='Cancelled').aggregate(t=Sum('plan_hours_used'))['t'] or 0
    return max(total - Decimal(used), Decimal('0'))


def ensure_invoice(booking=None, subscription=None):
    if booking is not None:
        existing = Invoice.objects.filter(booking=booking).first()
        if existing:
            return existing
        amount = booking.total_price - (
            booking.plan_hours_used * booking.workspace.price_per_hour
            if booking.plan_hours_used else 0
        )
        inv = Invoice.objects.create(
            number=f'TMP-B{booking.id}', member=booking.member,
            booking=booking, amount=max(amount, 0),
        )
    else:
        existing = Invoice.objects.filter(subscription=subscription).first()
        if existing:
            return existing
        inv = Invoice.objects.create(
            number=f'TMP-S{subscription.id}', member=subscription.member,
            subscription=subscription, amount=subscription.plan.price,
        )
    inv.number = f'WN-{timezone.localdate():%Y%m}-{inv.id:05d}'
    inv.save(update_fields=['number'])
    return inv


def mark_booking_paid(booking):
    booking.payment_status = 'Paid'
    booking.status = 'Confirmed'
    booking.save(update_fields=['payment_status', 'status', 'plan_hours_used'])
    ensure_invoice(booking=booking)


@login_required
def pay_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, member=request.user)

    if booking.status == 'Cancelled' or booking.payment_status == 'Paid':
        return redirect('my_bookings')
    if booking.booking_type == 'Monthly':
        hours = Decimal('0')
        free_hours = member_free_hours(request.user)
        plan_covers = False
    else:
        hours = booking_hours(booking)
        free_hours = member_free_hours(request.user)
        plan_covers = free_hours >= hours and hours > 0


    monthly_days = None

    if booking.booking_type == 'Monthly' and booking.booking_end_date:
        monthly_days = (
            booking.booking_end_date - booking.booking_date
        ).days + 1

    ctx = {
        'booking': booking,
        'hours': hours,
        'free_hours': free_hours,
        'plan_covers': plan_covers,
        'razorpay_enabled': razorpay_ready(),
        'monthly_days': monthly_days,
    }

    if request.method != 'POST':
        return render(request, 'workspaces/booking_payment.html', ctx)

    action = request.POST.get('action')

    if action == 'plan':
        if not ctx['plan_covers']:
            messages.error(request, 'Not enough free plan hours for this booking.')
            return redirect('pay_booking', booking_id=booking.id)
        booking.plan_hours_used = hours
        mark_booking_paid(booking)
        messages.success(
            request,
            f'Booking confirmed using {hours} free plan hour(s).'
        )
        return redirect('my_bookings')

    if action == 'pay':
        if not razorpay_ready():
            Payment.objects.create(
                member=request.user, booking=booking, amount=booking.total_price,
                payment_method='Demo', status='Successful',
                transaction_id=f'DEMO-B{booking.id}-{int(timezone.now().timestamp())}',
            )
            mark_booking_paid(booking)
            messages.success(request, 'Demo payment successful! Booking confirmed.')
            return redirect('my_bookings')

        try:
            order = rzp_client().order.create({
                'amount': int(booking.total_price * 100),
                'currency': 'INR',
                'receipt': f'booking_{booking.id}',
            })
        except Exception:
            messages.error(request, 'Could not start the payment. Please try again.')
            return redirect('pay_booking', booking_id=booking.id)

        Payment.objects.create(
            member=request.user, booking=booking, amount=booking.total_price,
            payment_method='Razorpay', razorpay_order_id=order['id'],
            status='Pending',
        )
        ctx.update({
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'order_id': order['id'],
            'amount_paise': order['amount'],
        })
        return render(request, 'workspaces/booking_payment.html', ctx)

    return redirect('pay_booking', booking_id=booking.id)


@login_required
@require_POST
def verify_booking_payment(request):
    order_id = request.POST.get('razorpay_order_id', '')
    payment = get_object_or_404(
        Payment, razorpay_order_id=order_id, member=request.user,
        booking__isnull=False,
    )
    booking = payment.booking

    if payment.status == 'Successful':
        return redirect('my_bookings')

    try:
        rzp_client().utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': request.POST.get('razorpay_payment_id', ''),
            'razorpay_signature': request.POST.get('razorpay_signature', ''),
        })
    except razorpay.errors.SignatureVerificationError:
        payment.status = 'Failed'
        payment.save(update_fields=['status'])
        messages.error(
            request,
            'Payment verification failed. If money was deducted, please contact support.'
        )
        return redirect('pay_booking', booking_id=booking.id)

    payment.transaction_id = request.POST.get('razorpay_payment_id', '')
    payment.status = 'Successful'
    payment.save(update_fields=['transaction_id', 'status'])
    mark_booking_paid(booking)
    messages.success(request, 'Payment successful! Your booking is confirmed.')
    return redirect('my_bookings')


def build_pdf(title, number, lines, total_label, total_value, note=''):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFillColorRGB(0.31, 0.27, 0.9)
    pdf.rect(0, height - 110, width, 110, fill=1, stroke=0)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont('Helvetica-Bold', 26)
    pdf.drawString(45, height - 60, 'WorkNest')
    pdf.setFont('Helvetica', 11)
    pdf.drawString(45, height - 82, 'Co-working space for freelancers & startups')
    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawRightString(width - 45, height - 60, title)
    pdf.setFont('Helvetica', 10)
    pdf.drawRightString(width - 45, height - 80, number)

    y = height - 160
    pdf.setFillColorRGB(0.12, 0.14, 0.25)
    for label, value in lines:
        pdf.setFont('Helvetica-Bold', 10)
        pdf.drawString(45, y, label)
        pdf.setFont('Helvetica', 10)
        pdf.drawString(190, y, str(value))
        y -= 24

    y -= 10
    pdf.setFillColorRGB(0.93, 0.94, 1)
    pdf.roundRect(40, y - 40, width - 80, 60, 10, fill=1, stroke=0)
    pdf.setFillColorRGB(0.31, 0.27, 0.9)
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(55, y + 2, total_label)
    pdf.setFont('Helvetica-Bold', 20)
    pdf.drawString(55, y - 28, total_value)

    if note:
        pdf.setFillColorRGB(0.4, 0.4, 0.4)
        pdf.setFont('Helvetica-Oblique', 9)
        pdf.drawString(45, y - 70, note)

    pdf.setFillColorRGB(0.45, 0.45, 0.45)
    pdf.setFont('Helvetica', 9)
    pdf.drawCentredString(width / 2, 60, 'Thank you for choosing WorkNest!')
    pdf.save()
    return buffer.getvalue()


@login_required
def booking_invoice(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related('workspace'), id=booking_id
    )
    if booking.member != request.user and not request.user.is_staff:
        raise Http404
    if booking.payment_status != 'Paid':
        messages.warning(request, 'Invoice is available once the booking is paid.')
        return redirect('my_bookings')

    inv = ensure_invoice(booking=booking)
    payment = booking.payments.filter(status='Successful').first()
    method = payment.payment_method if payment else 'Membership plan hours'
    txn = payment.transaction_id if payment and payment.transaction_id else '—'
    lines = [
        ('Invoice date', inv.created_at.strftime('%d %b %Y')),
        ('Billed to', booking.customer_name),
        ('Email', booking.email),
        ('Workspace', f'{booking.workspace.name} ({booking.workspace.workspace_type})'),
        ('Booking type', booking.booking_type),
        ('Date', booking.booking_date.strftime('%d %b %Y')),
        ('Time', f'{booking.start_time:%I:%M %p} - {booking.end_time:%I:%M %p}'),
        ('Booking total', f'Rs. {booking.total_price}'),
        ('Plan hours used', f'{booking.plan_hours_used} h' if booking.plan_hours_used else '—'),
        ('Payment method', method),
        ('Transaction ID', txn),
    ]
    pdf = build_pdf(
        'INVOICE', inv.number, lines, 'AMOUNT PAID', f'Rs. {inv.amount}',
        'Demo payment - no real money processed.' if method == 'Demo' else '',
    )
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{inv.number}.pdf"'
    return response


def day_booked_hours(workspace, day):
    total = Decimal('0')
    for b in Booking.objects.filter(
        workspace=workspace, booking_date=day, status__in=['Pending', 'Confirmed']
    ):
        total += booking_hours(b)
    return total


def space_calendar(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id, is_available=True)
    today = timezone.localdate()

    try:
        year, month = [int(x) for x in request.GET.get('month', '').split('-')]
        first = date(year, month, 1)
    except (ValueError, TypeError):
        first = today.replace(day=1)

    prev_month = (first - timedelta(days=1)).replace(day=1)
    next_month = (first + timedelta(days=32)).replace(day=1)

    bookings = Booking.objects.filter(
        workspace=workspace,
        booking_date__year=first.year,
        booking_date__month=first.month,
        status__in=['Pending', 'Confirmed'],
    )
    hours_by_day = {}
    for b in bookings:
        hours_by_day[b.booking_date] = hours_by_day.get(b.booking_date, Decimal('0')) + booking_hours(b)

    weeks = []
    for week in pycalendar.Calendar(firstweekday=0).monthdatescalendar(first.year, first.month):
        row = []
        for d in week:
            hrs = hours_by_day.get(d, Decimal('0'))
            if d < today:
                state = 'past'
            elif hrs >= DAY_HOURS:
                state = 'busy'
            elif hrs > 0:
                state = 'partial'
            else:
                state = 'free'
            row.append({
                'date': d, 'in_month': d.month == first.month,
                'state': state, 'today': d == today,
            })
        weeks.append(row)

    selected = None
    try:
        selected = date.fromisoformat(request.GET.get('day', ''))
    except ValueError:
        pass
    slots = []
    if selected:
        slots = Booking.objects.filter(
            workspace=workspace, booking_date=selected,
            status__in=['Pending', 'Confirmed'],
        ).order_by('start_time')

    return render(request, 'workspaces/space_calendar.html', {
        'workspace': workspace,
        'month_label': first.strftime('%B %Y'),
        'weeks': weeks,
        'weekdays': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'prev_month': prev_month.strftime('%Y-%m'),
        'next_month': next_month.strftime('%Y-%m'),
        'month_param': first.strftime('%Y-%m'),
        'selected': selected,
        'selected_past': bool(selected and selected < today),
        'slots': slots,
    })


def report_data():
    today = timezone.localdate()
    month_start = today.replace(day=1)
    window = 30
    since = today - timedelta(days=window)

    occupancy = []
    for ws in Workspace.objects.order_by('name'):
        booked = Decimal('0')
        for b in Booking.objects.filter(
            workspace=ws, booking_date__gte=since, booking_date__lte=today,
            status='Confirmed',
        ):
            booked += booking_hours(b)
        capacity_hours = DAY_HOURS * window
        pct = min(int(booked / capacity_hours * 100), 100) if capacity_hours else 0
        occupancy.append({'workspace': ws, 'hours': booked, 'percent': pct})

    months = []
    cursor = month_start
    for _ in range(6):
        nxt = (cursor + timedelta(days=32)).replace(day=1)
        paid = Payment.objects.filter(
            status='Successful', created_at__date__gte=cursor, created_at__date__lt=nxt
        )
        total = paid.aggregate(t=Sum('amount'))['t'] or 0
        months.append({
            'label': cursor.strftime('%b %Y'),
            'total': total,
            'membership': paid.filter(booking__isnull=True).aggregate(t=Sum('amount'))['t'] or 0,
            'bookings': paid.filter(booking__isnull=False).aggregate(t=Sum('amount'))['t'] or 0,
        })
        cursor = (cursor - timedelta(days=1)).replace(day=1)
    months.reverse()
    peak = max([m['total'] for m in months] + [1])
    for m in months:
        m['percent'] = int(m['total'] / peak * 100)

    ok = Payment.objects.filter(status='Successful')
    return {
        'occupancy': occupancy,
        'months': months,
        'window': window,
        'total_revenue': ok.aggregate(t=Sum('amount'))['t'] or 0,
        'membership_revenue': ok.filter(booking__isnull=True).aggregate(t=Sum('amount'))['t'] or 0,
        'booking_revenue': ok.filter(booking__isnull=False).aggregate(t=Sum('amount'))['t'] or 0,
        'total_invoices': Invoice.objects.count(),
    }


@staff_member_required
def revenue_report_pdf(request):
    data = report_data()
    lines = [
        ('Generated', timezone.localtime().strftime('%d %b %Y %I:%M %p')),
        ('Membership revenue', f"Rs. {data['membership_revenue']}"),
        ('Booking revenue', f"Rs. {data['booking_revenue']}"),
        ('Invoices issued', data['total_invoices']),
    ]
    for m in data['months']:
        lines.append((f"Revenue {m['label']}", f"Rs. {m['total']}"))
    for o in data['occupancy']:
        lines.append((f"Occupancy: {o['workspace'].name[:18]}",
                      f"{o['percent']}% ({o['hours']} h in last {data['window']} days)"))
    pdf = build_pdf(
        'REVENUE REPORT', timezone.localdate().isoformat(), lines,
        'TOTAL REVENUE', f"Rs. {data['total_revenue']}",
    )
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="WorkNest_Revenue_Report.pdf"'
    return response
