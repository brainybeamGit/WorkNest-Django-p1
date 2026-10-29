
from django.db import models
from django.conf import settings

class Workspace(models.Model):
    WORKSPACE_TYPES = [
        ('Hot Desk', 'Hot Desk'),
        ('Private Cabin', 'Private Cabin'),
        ('Meeting Room', 'Meeting Room'),
    ]

    name = models.CharField(max_length=100)
    workspace_type = models.CharField(
        max_length=50,
        choices=WORKSPACE_TYPES
    )
    description = models.TextField()
    price_per_hour = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    daily_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text='Full-day (9 AM - 6 PM) rate. Leave 0 to use 8x the hourly rate.'
    )
    monthly_rate = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    help_text='Monthly workspace booking rate. Leave 0 to use 30x daily rate.'
    
    )
    capacity = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    amenities = models.ManyToManyField(
    'Amenity',
    blank=True,
    related_name='workspaces'
)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def effective_daily_rate(self):
        return self.daily_rate or self.price_per_hour * 8

    @property
    
    def effective_monthly_rate(self):
        return self.monthly_rate or self.effective_daily_rate * 30

    def __str__(self):
        return self.name


class Booking(models.Model):
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )

    BOOKING_STATUS = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    booking_date = models.DateField()
    booking_end_date = models.DateField(
    null=True,
    blank=True
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default='Pending'
    )

    booking_type = models.CharField(
    max_length=10,
    choices=[
        ('Hourly', 'Hourly'),
        ('Daily', 'Daily'),
        ('Monthly', 'Monthly'),
    ],
    default='Hourly'
    )
    
    payment_status = models.CharField(
        max_length=10,
        choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid')],
        default='Unpaid'
    )
    plan_hours_used = models.DecimalField(
        max_digits=6, decimal_places=2, default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.workspace.name}"
class Amenity(models.Model):
        name = models.CharField(max_length=100, unique=True)
        description = models.TextField(blank=True)

        def __str__(self):
             return self.name

class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)
    free_hours = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    SUBSCRIPTION_STATUS = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
    ]

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_STATUS,
        default='Active'
    )

    def __str__(self):
        return f"{self.member.username} - {self.plan.name}"


class Payment(models.Model):
    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Successful', 'Successful'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.PROTECT,
        related_name='payments',
        null=True,
        blank=True
    )

    booking = models.ForeignKey(
        'Booking',
        on_delete=models.SET_NULL,
        related_name='payments',
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50,
        default='Razorpay'
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - ₹{self.amount} - {self.status}"


class CheckIn(models.Model):
    CHECKIN_STATUS = [
        ('Checked In', 'Checked In'),
        ('Checked Out', 'Checked Out'),
    ]

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='checkin'
    )

    check_in_time = models.DateTimeField(
        null=True,
        blank=True
    )

    check_out_time = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=CHECKIN_STATUS,
        default='Checked In'
    )

    def __str__(self):
        return f"Check-in: {self.booking.customer_name}"


class Invoice(models.Model):
    number = models.CharField(max_length=30, unique=True)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices'
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='invoice'
    )
    subscription = models.OneToOneField(
        Subscription,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='invoice'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number
