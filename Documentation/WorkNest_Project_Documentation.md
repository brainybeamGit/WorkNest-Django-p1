# WORKNEST
## Co-working Space Booking System

**Project Name:** WorkNest – Co-working Space Booking  
**Organization:** BrainyBeam Info-Tech Pvt. Ltd.

**Technologies:** Python 3, Django, HTML5, CSS3, Bootstrap 5, JavaScript, SQLite3, ReportLab, Razorpay Test Mode, Git, GitHub.

---

# 1. Abstract

WorkNest is a web-based Co-working Space Booking System designed to simplify the reservation and management of shared workspaces. It provides a platform for members to explore workspaces such as hot desks, private cabins, and meeting rooms and make bookings according to their requirements.

The system supports member registration and login, workspace availability checking, hourly and daily bookings, monthly workspace bookings, membership plans, payment processing, check-in and check-out, and PDF invoice generation.

Administrators can manage workspace information, amenities, membership plans, members, bookings, payments, and related operational information through the administrative interfaces.

The application uses Python and Django for backend development, HTML, CSS, Bootstrap, and JavaScript for the frontend, and SQLite3 for data storage. ReportLab is used for PDF invoice generation, while Razorpay test mode supports payment testing without processing real payments.

# 2. Introduction

WorkNest is an online platform designed to organize co-working space operations through a centralized web application.

Freelancers, professionals, and startup teams can use the platform to explore available workspaces, check availability, select booking periods, and manage their reservations.

The application also supports membership management, payment processing, check-in and check-out, and invoice downloads. Administrative functionality helps manage workspaces and monitor booking-related information.

The project demonstrates the practical application of web development, database management, authentication, booking workflows, and payment integration.

# 3. Problem Statement

Manual management of co-working spaces can make it difficult to track workspace availability, maintain booking records, manage memberships, and prepare invoices. It may also increase the risk of overlapping reservations and inefficient use of available workspaces.

WorkNest addresses these challenges by providing a centralized web-based system for workspace booking and administration.

# 4. Objectives

- Provide an online platform for workspace booking.
- Manage workspaces, including hot desks, private cabins, and meeting rooms.
- Allow users to check workspace availability.
- Support hourly, daily, and monthly workspace booking options.
- Provide member registration and login.
- Manage membership plans and subscriptions.
- Support payment processing and testing through Razorpay test mode.
- Provide check-in and check-out functionality.
- Generate downloadable PDF invoices.
- Maintain booking, payment, and membership records.
- Support administrative management and booking-related reporting.

# 5. Scope of the Project

WorkNest provides member-facing and administrative functionality.

## 5.1 Member Interface

The member interface supports the following operations:

- Register and log in.
- Browse workspaces.
- Check workspace availability.
- Create hourly, daily, and monthly bookings.
- View booking information.
- Purchase membership plans.
- Make payments through the available payment workflow.
- Check in and check out.
- Cancel eligible bookings.
- Download available PDF invoices.

## 5.2 Administrative Interface

The administrative functionality supports the management of workspaces, amenities, membership plans, members, bookings, payments, and related records.

Booking and operational information can be used to monitor workspace usage and financial activity.

The exact administrative operations available depend on the implemented views, permissions, and Django admin configuration.

# 6. Technology Stack

| Sr. No. | Technology | Purpose |
|---|---|---|
| 1 | Python 3 | Backend programming |
| 2 | Django | Web application framework |
| 3 | HTML5 | Web page structure |
| 4 | CSS3 | Styling and layout |
| 5 | Bootstrap 5 | Responsive user interface |
| 6 | JavaScript | Interactive frontend functionality |
| 7 | SQLite3 | Database management |
| 8 | ReportLab | PDF invoice generation |
| 9 | Razorpay Test Mode | Payment integration testing |
| 10 | Git | Version control |
| 11 | GitHub | Source code hosting |
| 12 | Visual Studio Code | Code editing and development |

# 7. Main Modules

## 7.1 Authentication Module

This module manages member registration, login, and authentication required to access protected features.

## 7.2 Workspace Management Module

This module maintains workspace information, including workspace type, description, capacity, pricing, availability, and amenities.

## 7.3 Availability Checking Module

This module allows users to check whether a workspace is available for their selected booking period.

The availability interface supports hourly, daily, and monthly selection options. The monthly option accepts a start date and an end date.

## 7.4 Booking Management Module

The booking module manages workspace reservations and their associated information.

Supported booking types include:

- **Hourly Booking:** Reservation based on the selected start and end times.
- **Daily Booking:** Reservation for a full day.
- **Monthly Booking:** Reservation for a selected date range, with pricing based on the configured monthly rate and booking duration.

Booking records include information such as the member, workspace, dates, booking type, amount, and status.

## 7.5 Membership Management Module

This module manages membership plans and member subscriptions. Eligible membership hours can be applied to supported bookings according to the implemented business rules.

## 7.6 Payment Module

The payment module handles the available payment workflow and records payment-related information.

Razorpay test mode is used to test online payment processing. Test mode is intended for development and does not represent a live payment transaction.

## 7.7 Invoice Generation Module

The system uses ReportLab to generate downloadable PDF invoices for supported transactions.

Invoice information can include customer details, workspace or membership details, transaction information, and the applicable amount.

## 7.8 Check-in and Check-out Module

This module records member check-in and check-out information associated with workspace usage.

## 7.9 Administrative Module

The administrative functionality supports the management of workspaces, amenities, membership plans, members, bookings, payments, and related records.

## 7.10 Reports Module

Booking, occupancy, and payment information can support operational monitoring and revenue reporting through the available reporting functionality.

# 8. Database Description

WorkNest uses SQLite3 as its database. Django models define the application's data structures and relationships.

The main models include the following:

| Sr. No. | Model | Purpose |
|---|---|---|
| 1 | User | Stores user account and authentication information. |
| 2 | Workspace | Stores workspace details, type, capacity, pricing, and availability. |
| 3 | Amenity | Stores available workspace facilities. |
| 4 | MembershipPlan | Stores membership plan information, pricing, duration, and eligible hours. |
| 5 | Subscription | Stores member subscription records. |
| 6 | Booking | Stores workspace reservations, dates, booking type, amount, and status. |
| 7 | CheckIn | Stores check-in and check-out records. |
| 8 | Invoice | Stores invoice-related information. |
| 9 | Payment | Stores payment transaction information and payment status. |

The Workspace and Amenity models have a many-to-many relationship, allowing workspaces to offer multiple amenities.

The Booking model connects a member with a workspace and stores the details of the reservation.

The exact database schema is defined by the Django models and migrations in the project source code.

# 9. Project Workflow

The general member booking workflow is as follows:

1. The member registers or logs in.
2. The member browses available workspaces.
3. The member selects a workspace.
4. The member checks availability for the required date or time.
5. The member chooses an appropriate booking type.
6. The system calculates the booking amount according to the configured pricing rules.
7. The member proceeds through the available payment workflow or an eligible membership-hours option.
8. The system updates the booking and payment records according to the payment result.
9. The member uses the check-in and check-out functionality when available.
10. The member can access the supported invoice download functionality.

# 10. Installation and Setup

The following steps describe the standard process for setting up a Django project. The actual dependencies and environment settings should be checked against the project files.

## 10.1 Prerequisites

- Python 3
- pip
- Git
- Visual Studio Code or another code editor
- A web browser

## 10.2 Download the Project

Clone the project repository:

```bash
git clone https://github.com/brainybeamGit/WorkNest-Django-p1.git
```

Navigate to the project directory:

```bash
cd WorkNest-Django-p1
```

## 10.3 Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

## 10.4 Install Dependencies

If the project contains a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

## 10.5 Apply Database Migrations

```bash
python manage.py migrate
```

## 10.6 Create an Administrative Account

```bash
python manage.py createsuperuser
```

Enter the requested username, email address, and password.

## 10.7 Run the Development Server

```bash
python manage.py runserver
```

Open the local development address in a web browser:

```text
http://127.0.0.1:8000/
```

The Django administrative interface is generally available at:

```text
http://127.0.0.1:8000/admin/
```

The exact URLs depend on the project's URL configuration.

## 10.8 Payment Configuration

Configure the Razorpay test credentials and other required settings according to the project's existing configuration.

Secret keys and credentials should be stored securely and must not be committed to the public GitHub repository.

# 11. Testing

The project should be tested to verify the behavior of its main modules.

| Sr. No. | Test Area | Testing Objective |
|---|---|---|
| 1 | Registration and Login | Verify account creation and authentication. |
| 2 | Workspace Management | Verify workspace information and amenities. |
| 3 | Availability Checking | Verify date and time availability checks. |
| 4 | Hourly Booking | Verify hourly reservation and pricing. |
| 5 | Daily Booking | Verify daily reservation and pricing. |
| 6 | Monthly Booking | Verify the selected date range, duration, pricing, and availability. |
| 7 | Membership | Verify membership plans and subscription records. |
| 8 | Payment | Verify the configured payment workflow using test mode. |
| 9 | Invoice Generation | Verify that supported transactions generate downloadable PDF invoices. |
| 10 | Check-in and Check-out | Verify usage records. |
| 11 | Booking Cancellation | Verify cancellation behavior and booking status. |
| 12 | Administrative Functions | Verify access permissions and management operations. |
| 13 | Reports | Verify the accuracy of available booking, occupancy, and revenue information. |

Testing results should be recorded after each test has been performed. A feature should be marked as successfully tested only after its expected behavior has been verified.

# 12. Limitations

- SQLite3 is suitable for development and small-scale demonstrations but may not be appropriate for every production deployment.
- Razorpay test mode does not process real payments.
- The availability and functionality of individual modules depend on their implementation and configuration.
- Production deployment requires appropriate security settings, protected credentials, and a suitable hosting environment.

# 13. Future Enhancements

Potential future enhancements include:

- Email and SMS booking notifications.
- QR-code-based check-in.
- Advanced analytics dashboards.
- Management of multiple co-working centres.
- Mobile application integration.
- Additional reporting and automated booking notifications.

These features should be considered future enhancements unless they are already implemented in the application.

# 14. Conclusion

WorkNest is a web-based application for managing co-working space bookings, memberships, payments, and related administrative operations.

The project demonstrates the use of Python, Django, SQLite3, HTML, CSS, Bootstrap, and JavaScript to develop a structured web application. ReportLab supports PDF invoice generation, while Razorpay test mode enables payment workflow testing.

The application provides a foundation for organizing workspace reservations and member information. Further testing, documentation, and deployment improvements can help prepare the system for broader use.