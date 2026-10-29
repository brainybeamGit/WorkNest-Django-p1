
from django.urls import path
from . import views, booking_flow

urlpatterns = [
    path('', views.home, name='home'),
    path('spaces/', views.spaces, name='spaces'),
    path('booking/<int:workspace_id>/', views.booking, name='booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('check-availability/<int:workspace_id>/', views.check_availability, name='check_availability'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('membership-plans/', views.membership_plans, name='membership_plans'),
    path('subscribe/<int:plan_id>/', views.subscribe_plan, name='subscribe_plan'),
    path('admin-dashboard/action/', views.admin_action, name='admin_action'),
    path('pay-booking/<int:booking_id>/', booking_flow.pay_booking, name='pay_booking'),
    path('verify-booking-payment/', booking_flow.verify_booking_payment, name='verify_booking_payment'),
    path('booking-invoice/<int:booking_id>/', booking_flow.booking_invoice, name='booking_invoice'),
    path('calendar/<int:workspace_id>/', booking_flow.space_calendar, name='space_calendar'),
    path('admin-dashboard/revenue-report/', booking_flow.revenue_report_pdf, name='revenue_report'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('download-invoice/<int:subscription_id>/', views.download_invoice, name='download_invoice'),
    path('my-membership/', views.my_membership, name='my_membership'),

    path('check-in/<int:booking_id>/', views.check_in, name='check_in'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

]
