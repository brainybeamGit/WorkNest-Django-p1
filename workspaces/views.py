
import razorpay
from django.conf import settings
from django.urls import reverse
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Workspace, Booking, MembershipPlan, Subscription, Payment
from decimal import Decimal
from datetime import datetime, date
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from .models import Subscription, Payment
from django.db.models import Q

from .models import (
    Workspace,
    Booking,
    Amenity,
    MembershipPlan,
    Subscription,
    Payment,
    CheckIn,
    Invoice,
)


def razorpay_configured():
    return bool(settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET)


def get_razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


def home(request):
    membership_plans = MembershipPlan.objects.filter(is_active=True)
    featured_workspaces = Workspace.objects.filter(is_available=True)[:3]

    return render(request, 'workspaces/home.html', {
        'membership_plans': membership_plans,
        'featured_workspaces': featured_workspaces,
        'workspace_count': Workspace.objects.filter(is_available=True).count(),
    })


def spaces(request):
    workspaces = Workspace.objects.filter(is_available=True)

    return render(request, 'workspaces/spaces.html', {
        'workspaces': workspaces
    })


@login_required
def booking(request, workspace_id):
    workspace = get_object_or_404(
        Workspace,
        id=workspace_id,
        is_available=True
    )

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        booking_date = request.POST.get('booking_date', '')
        booking_end_date = request.POST.get('booking_end_date', '')
        booking_type = request.POST.get('booking_type', 'Hourly')
        start_time = request.POST.get('start_time', '')
        end_time = request.POST.get('end_time', '')

        if booking_type not in ['Hourly', 'Daily', 'Monthly']:
            messages.error(request, 'Please select a valid booking type.')

        elif not all([customer_name, email, phone, booking_date]):
            messages.error(request, 'Please fill in all required fields.')

        else:
            try:
                selected_date = date.fromisoformat(booking_date)

                if selected_date < date.today():
                    messages.error(
                        request,
                        'Please select today or a future date.'
                    )

                else:
                    if booking_type == 'Monthly':
                        if not booking_end_date:
                            messages.error(
                                request,
                                'Please select the booking end date.'
                            )
                            raise ValueError('Missing monthly end date.')

                        selected_end_date = date.fromisoformat(
                            booking_end_date
                        )

                        if selected_end_date < selected_date:
                            messages.error(
                                request,
                                'End date cannot be before the start date.'
                            )
                            raise ValueError('Invalid monthly date range.')

                       # Charge one monthly rate for a booking of up to 30 days.
                        
                        number_of_days = (
                            selected_end_date - selected_date
                            ).days + 1
                        
                        number_of_months = max(
                             1,
                             (number_of_days - 1) // 30 + 1
                             )
                        total_price = (
                            workspace.effective_monthly_rate
                            * number_of_months
                            )

                        # Monthly bookings reserve the workspace for
                        # every date in the selected date range.
                        overlapping_booking = Booking.objects.filter(
                             workspace=workspace,
                             status__in=['Pending', 'Confirmed'],
                             ).filter(
                                 booking_date__lte=selected_end_date
                                 ).filter(
                                    Q(booking_end_date__gte=selected_date)
    | Q(booking_end_date__isnull=True, booking_date__gte=selected_date)
).exists()

                    else:
                        selected_end_date = None

                        if booking_type == 'Daily':
                            start_time = '09:00'
                            end_time = '18:00'

                        if not all([start_time, end_time]):
                            messages.error(
                                request,
                                'Please select a start and end time.'
                            )
                            raise ValueError('Missing booking time.')

                        start = datetime.strptime(start_time, '%H:%M')
                        end = datetime.strptime(end_time, '%H:%M')

                        if start >= end:
                            messages.error(
                                request,
                                'End time must be later than start time.'
                            )
                            raise ValueError('Invalid booking time.')

                        # Check monthly bookings that cover this date.
                        monthly_overlap = Booking.objects.filter(
                            workspace=workspace,
                            booking_type='Monthly',
                            status__in=['Pending', 'Confirmed'],
                            booking_date__lte=selected_date,
                            booking_end_date__gte=selected_date
                        ).exists()

                        # Check same-day hourly/daily bookings.
                        same_day_overlap = Booking.objects.filter(
                            workspace=workspace,
                            booking_date=selected_date,
                            status__in=['Pending', 'Confirmed'],
                            start_time__lt=end_time,
                            end_time__gt=start_time
                        ).exclude(
                            booking_type='Monthly'
                        ).exists()

                        overlapping_booking = (
                            monthly_overlap or same_day_overlap
                        )

                        hours = Decimal(
                            str((end - start).total_seconds() / 3600)
                        )

                        if booking_type == 'Daily':
                            total_price = workspace.effective_daily_rate
                        else:
                            total_price = (
                                hours * workspace.price_per_hour
                            )

                    if overlapping_booking:
                        messages.error(
                            request,
                            'This workspace is already booked for '
                            'the selected date or time. Please choose '
                            'another date or time.'
                        )

                    else:
                        new_booking = Booking.objects.create(
                            member=request.user,
                            workspace=workspace,
                            customer_name=customer_name,
                            email=email,
                            phone=phone,
                            booking_date=selected_date,
                            booking_end_date=selected_end_date,
                            start_time=start_time or '09:00',
                            end_time=end_time or '18:00',
                            total_price=total_price,
                            booking_type=booking_type,
                            status='Pending'
                        )

                        messages.success(
                            request,
                            'Booking created! Complete payment to confirm it.'
                        )

                        return redirect(
                            'pay_booking',
                            booking_id=new_booking.id
                        )

            except ValueError:
                pass

    return render(request, 'workspaces/booking.html', {
        'workspace': workspace,
        'today': date.today().isoformat(),
        'prefill_date': request.GET.get('date', ''),
        'saved_phone': (
            request.POST.get('phone', '')
            or (
                request.user.profile.phone
                if hasattr(request.user, 'profile')
                else ''
            )
        ),
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        member=request.user
    ).order_by('-created_at')

    return render(request, 'workspaces/my_bookings.html', {
        'bookings': bookings
    })


@login_required
@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        member=request.user
    )

    if booking.status == 'Pending' or (
        booking.status == 'Confirmed' and booking.booking_date > date.today()
    ):
        booking.status = 'Cancelled'
        booking.plan_hours_used = 0
        booking.save()
        booking.payments.filter(status='Successful').update(status='Refunded')
        messages.success(
            request,
            'Booking cancelled successfully!'
        )

    elif booking.status == 'Confirmed':
        messages.error(
            request,
            'Only upcoming bookings can be cancelled.'
        )

    else:
        messages.error(
            request,
            'This booking is already cancelled.'
        )
    return redirect('my_bookings')




def check_availability(request, workspace_id):
    workspace = get_object_or_404(
        Workspace,
        id=workspace_id,
        is_available=True
    )

    booking_type = request.GET.get('booking_type', 'Hourly')
    booking_date = request.GET.get('booking_date', '')
    booking_end_date = request.GET.get('booking_end_date', '')
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')

    available = None
    error = ''

    if booking_date:
        try:
            selected_date = date.fromisoformat(booking_date)

            if selected_date < date.today():
                error = 'Please select today or a future date.'

            elif booking_type == 'Monthly':
                if not booking_end_date:
                    error = 'Please select an end date.'
                else:
                    selected_end_date = date.fromisoformat(
                        booking_end_date
                    )

                    if selected_end_date < selected_date:
                        error = 'End date must be on or after the start date.'
                    else:
                        overlapping = Booking.objects.filter(
                            workspace=workspace,
                            status__in=['Pending', 'Confirmed'],
                            booking_date__lte=selected_end_date
                        ).filter(
                            Q(booking_end_date__gte=selected_date)
                            | Q(
                                booking_end_date__isnull=True,
                                booking_date__gte=selected_date
                            )
                        ).exists()

                        available = not overlapping

            elif booking_type == 'Daily':
                overlapping = Booking.objects.filter(
                    workspace=workspace,
                    status__in=['Pending', 'Confirmed'],
                    booking_date=selected_date,
                    booking_type__in=['Daily', 'Monthly']
                ).exists()

                available = not overlapping

            elif booking_type == 'Hourly':
                if not start_time or not end_time:
                    error = 'Please select start and end times.'

                elif start_time >= end_time:
                    error = 'End time must be later than start time.'

                else:
                    overlapping = Booking.objects.filter(
                        workspace=workspace,
                        status__in=['Pending', 'Confirmed'],
                        booking_date=selected_date
                    ).filter(
                        Q(booking_type='Monthly')
                        | Q(
                            start_time__lt=end_time,
                            end_time__gt=start_time
                        )
                    ).exists()

                    available = not overlapping

            else:
                error = 'Please select a valid booking type.'

        except ValueError:
            error = 'Please enter a valid date and time.'

    return render(request, 'workspaces/check_availability.html', {
        'workspace': workspace,
        'available': available,
        'error': error,
        'booking_type': booking_type,
        'booking_date': booking_date,
        'booking_end_date': booking_end_date,
        'start_time': start_time,
        'end_time': end_time,
        'today': date.today().isoformat(),
    })


def membership_plans(request):
    plans = MembershipPlan.objects.filter(is_active=True)

    return render(request, 'workspaces/membership_plans.html', {
        'plans': plans
    })

@staff_member_required
def admin_dashboard(request):
    from django.db.models import Sum

    tab = request.GET.get('tab', 'overview')
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    revenue = Payment.objects.filter(status='Successful').aggregate(t=Sum('amount'))['t'] or 0
    bookings_value = Booking.objects.filter(status='Confirmed').aggregate(t=Sum('total_price'))['t'] or 0

    context = {
        'tab': tab,
        'q': q,
        'status': status,
        'total_workspaces': Workspace.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_members': Booking.objects.values('member').distinct().count(),
        'pending_bookings': Booking.objects.filter(status='Pending').count(),
        'confirmed_bookings': Booking.objects.filter(status='Confirmed').count(),
        'cancelled_bookings': Booking.objects.filter(status='Cancelled').count(),
        'total_revenue': bookings_value,
        'membership_revenue': revenue,
        'active_subscriptions': Subscription.objects.filter(status='Active').count(),
        'recent_bookings': Booking.objects.select_related('workspace', 'member').order_by('-created_at')[:6],
    }

    if tab == 'bookings':
        qs = Booking.objects.select_related('workspace', 'member').order_by('-created_at')
        if status:
            qs = qs.filter(status=status)
        if q:
            qs = qs.filter(customer_name__icontains=q) | qs.filter(workspace__name__icontains=q)
        context['bookings'] = qs[:100]
    elif tab == 'members':
        from django.contrib.auth import get_user_model
        users = get_user_model().objects.annotate(
            booking_count=Count('bookings', distinct=True)
        ).order_by('-date_joined')
        if q:
            users = users.filter(username__icontains=q) | users.filter(email__icontains=q)
        today = timezone.localdate()
        active = {
            s.member_id: s.plan.name
            for s in Subscription.objects.filter(status='Active', end_date__gte=today).select_related('plan')
        }
        context['members'] = [{'user': u, 'plan': active.get(u.id)} for u in users[:100]]
    elif tab == 'memberships':
        context['subscriptions'] = Subscription.objects.select_related('member', 'plan').order_by('-start_date', '-id')[:100]
    elif tab == 'payments':
        context['payments'] = Payment.objects.select_related('member', 'plan', 'booking__workspace').order_by('-created_at')[:100]
    elif tab == 'invoices':
        context['invoices'] = Invoice.objects.select_related(
            'member', 'booking__workspace', 'subscription__plan'
        ).order_by('-created_at')[:100]
    elif tab == 'workspaces':
        context['workspaces'] = Workspace.objects.order_by('name')
    elif tab == 'reports':
        from .booking_flow import report_data
        context.update(report_data())
    return render(request, 'workspaces/admin_dashboard.html', context)


@staff_member_required
@require_POST
def admin_action(request):
    action = request.POST.get('action')
    obj_id = request.POST.get('id')
    next_tab = request.POST.get('tab', 'overview')

    if action in ('confirm_booking', 'cancel_booking'):
        booking = get_object_or_404(Booking, id=obj_id)
        booking.status = 'Confirmed' if action == 'confirm_booking' else 'Cancelled'
        booking.save(update_fields=['status'])
        messages.success(request, f'Booking for {booking.customer_name} marked {booking.status}.')
    elif action == 'toggle_workspace':
        ws = get_object_or_404(Workspace, id=obj_id)
        ws.is_available = not ws.is_available
        ws.save(update_fields=['is_available'])
        messages.success(request, f'{ws.name} is now {"available" if ws.is_available else "unavailable"}.')
    elif action == 'cancel_subscription':
        sub = get_object_or_404(Subscription, id=obj_id)
        sub.status = 'Cancelled'
        sub.save(update_fields=['status'])
        messages.success(request, f'Subscription for {sub.member.username} cancelled.')

    return redirect(f"{reverse('admin_dashboard')}?tab={next_tab}")

@login_required
def subscribe_plan(request, plan_id):
    plan = get_object_or_404(
        MembershipPlan,
        id=plan_id,
        is_active=True
    )

    if request.method != 'POST':
        return render(
            request,
            'workspaces/payment.html',
            {'plan': plan, 'razorpay_enabled': razorpay_configured()}
        )

    today = timezone.localdate()

    existing_subscription = Subscription.objects.filter(
        member=request.user,
        plan=plan,
        status='Active',
        end_date__gte=today
    ).exists()

    if existing_subscription:
        messages.warning(
            request,
            'You already have an active membership for this plan.'
        )
        return redirect('my_membership')

    if razorpay_configured():
        try:
            order = get_razorpay_client().order.create({
                'amount': int(plan.price * 100),
                'currency': 'INR',
                'receipt': f'plan_{plan.id}_user_{request.user.id}',
            })
        except Exception:
            messages.error(
                request,
                'Could not start the payment. Please try again.'
            )
            return redirect('subscribe_plan', plan_id=plan.id)

        Payment.objects.create(
            member=request.user,
            plan=plan,
            amount=plan.price,
            payment_method='Razorpay',
            razorpay_order_id=order['id'],
            status='Pending'
        )

        return render(
            request,
            'workspaces/payment.html',
            {
                'plan': plan,
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'order_id': order['id'],
                'amount_paise': order['amount'],
            }
        )

    payment = Payment.objects.create(
        member=request.user,
        plan=plan,
        amount=plan.price,
        payment_method='Demo',
        status='Successful',
        transaction_id=(
            f'DEMO-{request.user.id}-{plan.id}-'
            f'{timezone.now().timestamp()}'
        )
    )

    subscription = Subscription.objects.create(
        member=request.user,
        plan=plan,
        start_date=today,
        end_date=today + timedelta(days=plan.duration_days),
        status='Active'
    )

    messages.success(
        request,
        'Demo payment successful! Your membership is active.'
    )

    return render(
        request,
        'workspaces/payment_success.html',
        {
            'payment': payment,
            'subscription': subscription,
        }
    )

@login_required
@require_POST
def verify_payment(request):
    order_id = request.POST.get('razorpay_order_id', '')
    payment_id = request.POST.get('razorpay_payment_id', '')
    signature = request.POST.get('razorpay_signature', '')

    payment = get_object_or_404(
        Payment,
        razorpay_order_id=order_id,
        member=request.user
    )

    if payment.status == 'Successful':
        return redirect('my_membership')

    try:
        get_razorpay_client().utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        })
    except razorpay.errors.SignatureVerificationError:
        payment.status = 'Failed'
        payment.save(update_fields=['status'])
        messages.error(
            request,
            'Payment verification failed. If money was deducted, '
            'please contact support.'
        )
        return redirect('membership_plans')

    payment.transaction_id = payment_id
    payment.status = 'Successful'
    payment.save(update_fields=['transaction_id', 'status'])

    today = timezone.localdate()
    subscription = Subscription.objects.create(
        member=request.user,
        plan=payment.plan,
        start_date=today,
        end_date=today + timedelta(days=payment.plan.duration_days),
        status='Active'
    )

    messages.success(
        request,
        'Payment successful! Your membership is active.'
    )

    return render(
        request,
        'workspaces/payment_success.html',
        {
            'payment': payment,
            'subscription': subscription,
        }
    )


@login_required
def download_invoice(request, subscription_id):
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id,
        member=request.user
    )
    from .booking_flow import ensure_invoice
    ensure_invoice(subscription=subscription)

    payment = Payment.objects.filter(
        member=request.user,
        plan=subscription.plan,
        status='Successful'
    ).order_by('-created_at').first()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    pdf.setTitle("WorkNest Membership Invoice")

    pdf.setFillColorRGB(0.14, 0.36, 0.92)
    pdf.rect(0, height - 125, width, 125, fill=1, stroke=0)

    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawString(45, height - 55, "WorkNest")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(45, height - 80, "Your Workspace, Your Productivity")

    pdf.setFillColorRGB(0.14, 0.36, 0.92)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(45, height - 165, "MEMBERSHIP INVOICE")

    pdf.setFillColorRGB(0.25, 0.25, 0.25)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(
        45, height - 195,
        f"Invoice No: WN-{subscription.id:04d}"
    )

    y = height - 245

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(45, y, "MEMBER DETAILS")

    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(
        45, y,
        f"Member Name: {subscription.member.username}"
    )

    y -= 22
    pdf.drawString(
        45, y,
        f"Membership Plan: {subscription.plan.name}"
    )

    y -= 22
    pdf.drawString(
        45, y,
        f"Start Date: {subscription.start_date}"
    )

    y -= 22
    pdf.drawString(
        45, y,
        f"Expiry Date: {subscription.end_date}"
    )

    y -= 45

    pdf.setFillColorRGB(0.94, 0.96, 1)
    pdf.roundRect(40, y - 25, width - 80, 65, 10, fill=1, stroke=0)

    pdf.setFillColorRGB(0.14, 0.36, 0.92)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(55, y + 15, "TOTAL AMOUNT")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(
        55, y - 10,
        f"Rs. {subscription.plan.price}"
    )

    y -= 80

    pdf.setFillColorRGB(0.2, 0.2, 0.2)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(45, y, "PAYMENT DETAILS")

    y -= 25

    pdf.setFont("Helvetica", 10)

    transaction_id = (
        payment.transaction_id
        if payment and payment.transaction_id
        else "Not Available"
    )

    payment_status = (
        payment.status if payment else "No payment record found"
    )

    pdf.drawString(45, y, f"Transaction ID: {transaction_id}")

    y -= 22
    pdf.drawString(45, y, f"Payment Status: {payment_status}")

    y -= 22
    pdf.drawString(
        45, y,
        f"Subscription Status: {subscription.status}"
    )

    if not payment or payment.payment_method == 'Demo':
        pdf.setFillColorRGB(1, 0.96, 0.86)
        pdf.roundRect(40, 100, width - 80, 55, 8, fill=1, stroke=0)

        pdf.setFillColorRGB(0.45, 0.30, 0.05)
        pdf.setFont("Helvetica", 9)
        pdf.drawCentredString(
            width / 2, 130,
            "Demo invoice generated for project testing."
        )
        pdf.drawCentredString(
            width / 2, 115,
            "No real payment was processed."
        )

    pdf.setFillColorRGB(0.45, 0.45, 0.45)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(
        width / 2, 65,
        "Thank you for choosing WorkNest!"
    )

    pdf.save()
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="WorkNest_Invoice_{subscription.id}.pdf"'
    )

    return response


@login_required
def my_membership(request):
    subscriptions = Subscription.objects.filter(
        member=request.user
    ).select_related('plan').order_by('-start_date')

    from .booking_flow import member_free_hours
    today = timezone.localdate()
    total = sum(
        s.plan.free_hours for s in subscriptions
        if s.status == 'Active' and s.end_date >= today
    )
    remaining = member_free_hours(request.user)
    used = max(total - remaining, 0)
    percent = int(used / total * 100) if total else 0

    return render(
        request,
        'workspaces/my_membership.html',
        {
            'subscriptions': subscriptions,
            'hours_total': total,
            'hours_used': used,
            'hours_left': remaining,
            'hours_percent': percent,
        }
    )


@login_required
@require_POST
def check_in(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        member=request.user
    )

    if booking.status != 'Confirmed':
        messages.error(
            request,
            'Only confirmed bookings can be checked in.'
        )
        return redirect('my_bookings')

    checkin, created = CheckIn.objects.get_or_create(
        booking=booking
    )

    action = request.POST.get('action')

    if action == 'check_in':
        if checkin.check_in_time is not None:
            messages.warning(
                request,
                'You have already checked in for this booking.'
            )
        else:
            checkin.check_in_time = timezone.now()
            checkin.status = 'Checked In'
            checkin.save()

            messages.success(
                request,
                'Check-in successful! Enjoy your workspace.'
            )

    elif action == 'check_out':
        if checkin.check_in_time is None:
            messages.error(
                request,
                'Please check in before checking out.'
            )
        elif checkin.check_out_time is not None:
            messages.warning(
                request,
                'You have already checked out.'
            )
        else:
            checkin.check_out_time = timezone.now()
            checkin.status = 'Checked Out'
            checkin.save()
            if booking.payment_status == 'Paid':
                from .booking_flow import ensure_invoice
                ensure_invoice(booking=booking)

            messages.success(
                request,
                'Check-out successful!'
            )

    else:
        messages.error(
            request,
            'Invalid check-in/check-out action.'
        )

    return redirect('my_bookings')