from django.contrib import admin
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


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'workspace_type',
        'price_per_hour',
        'daily_rate',
        'capacity',
        'is_available',
    )

    list_filter = ('workspace_type', 'is_available')
    search_fields = ('name', 'description')
    filter_horizontal = ('amenities',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'workspace',
        'customer_name',
        'booking_date',
        'start_time',
        'end_time',
        'booking_type',
        'payment_status',
        'status',
    )

    list_filter = ('status', 'payment_status', 'booking_type', 'booking_date')
    search_fields = ('customer_name', 'email')


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'duration_days',
        'free_hours',
        'is_active',
    )

    list_filter = ('is_active', 'duration_days')
    search_fields = ('name', 'description')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'member',
        'plan',
        'start_date',
        'end_date',
        'status',
    )

    list_filter = ('status', 'plan', 'start_date')
    search_fields = ('member__username', 'plan__name')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'member',
        'plan',
        'amount',
        'payment_method',
        'transaction_id',
        'status',
        'created_at',
    )

    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = (
        'member__username',
        'transaction_id',
        'plan__name',
    )


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'booking',
        'check_in_time',
        'check_out_time',
        'status',
    )

    list_filter = ('status',)
    search_fields = (
        'booking__customer_name',
        'booking__workspace__name',
    )

    readonly_fields = ('check_in_time', 'check_out_time')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'member', 'amount', 'created_at')
    search_fields = ('number', 'member__username')
