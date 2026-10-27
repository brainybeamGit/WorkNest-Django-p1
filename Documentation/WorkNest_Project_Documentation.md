# WORKNEST
## Co-working Space Booking System

**Project Name:** WorkNest – Co-working Space Booking

**Organization:** BrainyBeam Info-Tech Pvt. Ltd.

**Technologies:** Python 3, Django, HTML, CSS, Bootstrap 5, JavaScript, SQLite3, ReportLab, Razorpay Test Mode.

---

# 1. Abstract

WorkNest is a web-based Co-working Space Booking System designed to simplify the management and reservation of shared workspaces. The system allows members to book hot desks, private cabins, and meeting rooms according to their requirements.

Members can register, log in, view available spaces, make bookings, purchase membership plans, complete payments, check in and check out, and download PDF invoices.

Administrators can manage spaces, amenities, membership plans, members, bookings, payments, occupancy, and revenue reports.

The application will be developed using Python and Django, with SQLite3 as the database. Bootstrap 5 will be used to create a responsive interface. ReportLab will support PDF invoice generation, and Razorpay test mode will be used to test payment processing.

# 2. Introduction

WorkNest is an online platform designed to manage co-working spaces efficiently. It provides a centralized system for freelancers, startups, and professionals who require flexible workspaces.

The platform supports hot desks, private cabins, and meeting rooms. Members can search for available spaces, select dates and times, and make reservations online.

The system also provides membership management, payment processing, check-in and check-out, and invoice generation. Administrators can monitor bookings, occupancy, and revenue through the administrative interface.

# 3. Problem Statement

Manual management of co-working spaces can make it difficult to track availability, manage reservations, maintain membership records, and prepare invoices. It may also lead to overlapping bookings and inefficient use of available spaces.

WorkNest aims to solve these problems by providing a centralized online system for workspace booking and administration.

# 4. Objectives

- To provide online booking for co-working spaces.
- To manage hot desks, private cabins, and meeting rooms.
- To display space availability based on dates and times.
- To provide member registration and login.
- To manage membership plans and subscriptions.
- To support payment processing through Razorpay test mode.
- To implement check-in and check-out functionality.
- To generate downloadable PDF invoices.
- To track occupancy and revenue.
- To simplify administrative operations.

# 5. Scope of the Project

The system will provide two primary interfaces: Admin and Member.

The Admin interface will manage spaces, amenities, membership plans, members, bookings, payments, invoices, occupancy, and revenue reports.

The Member interface will support registration, login, space searching, booking, membership purchases, payments, check-in, check-out, booking cancellation, and invoice downloads.

The application is intended to provide a convenient and organized method for managing co-working space operations.

# 6. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Backend programming |
| Django | Web application framework |
| HTML5 | Web page structure |
| CSS3 | Styling |
| Bootstrap 5 | Responsive interface |
| JavaScript | Interactive functionality |
| SQLite3 | Database management |
| ReportLab | PDF invoice generation |
| Razorpay Test Mode | Payment testing |
| Git and GitHub | Version control and code hosting |

# 7. Main Modules

## 7.1 Admin Module

- Manage spaces and amenities.
- Create and manage membership plans.
- View and manage members.
- Monitor bookings and occupancy.
- Track payments and invoices.
- Generate revenue reports.

## 7.2 Member Module

- Register and log in.
- Search available spaces.
- Book desks, cabins, and meeting rooms.
- Purchase membership plans.
- Make payments.
- Check in and check out.
- Cancel eligible bookings.
- Download PDF invoices.

# 8. Main Database Tables

| Table | Purpose |
|---|---|
| User | Store account and authentication information |
| Space | Store workspace details and rates |
| Amenity | Store facility information |
| SpaceAmenity | Link spaces with amenities |
| MembershipPlan | Store membership plan details |
| Subscription | Store member subscriptions |
| Booking | Store booking information |
| CheckIn | Store arrival and departure records |
| Invoice | Store invoice information |
| Payment | Store payment records |

The database schema will be finalized during implementation based on the Django models and required relationships.

# 9. Project Workflow

1. The member registers or logs in.
2. The member searches for available spaces.
3. The member selects a space and booking time.
4. The system checks availability.
5. The booking amount is calculated.
6. The member pays or uses eligible membership hours.
7. The system confirms the booking.
8. The member checks in upon arrival.
9. The member checks out when leaving.
10. The system records usage and generates the invoice.

# 10. Testing

The application will be tested to verify:

- Registration and login.
- Space and amenity management.
- Availability checking.
- Booking creation and cancellation.
- Membership plan purchases.
- Payment verification.
- Check-in and check-out.
- PDF invoice generation.
- Occupancy and revenue reports.

# 11. Future Enhancements

- Email and SMS booking notifications.
- QR-code-based check-in.
- Advanced analytics dashboards.
- Multiple co-working centre management.
- Mobile application integration.

# 12. Conclusion

WorkNest aims to provide an efficient and user-friendly solution for co-working space management. By integrating workspace booking, membership management, payments, check-in and check-out, and invoice generation, the system will help simplify administrative activities and improve the member experience.