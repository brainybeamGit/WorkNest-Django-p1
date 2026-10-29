# WorkNest – Co-working Space Booking System

## Project Overview

WorkNest is a web-based Co-working Space Booking System developed using Python and Django. It helps users explore workspaces, check availability, make bookings, manage subscriptions, and access booking invoices.

The system provides an interface for users to manage their bookings and an administrative interface to manage workspace-related information.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Backend:** Python, Django
- **Database:** SQLite3
- **PDF Generation:** ReportLab
- **Payment Gateway:** Razorpay (Test Mode)
- **Version Control:** Git and GitHub

## Features and Modules

### 1. User Authentication
- User registration and login
- User account access

### 2. Workspace Management
- View available workspaces
- Explore workspace details and amenities

### 3. Availability Checking
- Check workspace availability for selected dates
- Support for hourly, daily, and monthly booking types

### 4. Booking Management
- Create workspace bookings
- Calculate booking prices according to the selected booking type
- View booking details
- Cancel bookings, where permitted

### 5. Membership and Subscription
- View membership plans
- Manage membership subscriptions
- Apply eligible membership benefits to bookings

### 6. Online Payments
- Integrate Razorpay in Test Mode
- Process test payments for bookings

### 7. Invoice Generation
- Generate PDF invoices for bookings and payments

### 8. Check-in and Check-out
- Manage workspace check-in and check-out records

### 9. Admin Panel
- Manage application data through the Django admin interface
- Manage users, workspaces, bookings, and related records according to configured permissions

### 10. Reports and Dashboard
- Display relevant booking and business information
- Support occupancy and revenue reporting where implemented

## Project Requirements

Before running the project, install:

- Python
- pip
- Git (optional, if cloning the repository)
- A code editor such as Visual Studio Code

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/brainybeamGit/WorkNest-Django-p1.git
```

Navigate into the project folder:

```bash
cd WorkNest-Django-p1
```

> If you already have the project on your computer, open its existing folder instead of cloning it again.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

If the project contains a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

If this file is missing, install the dependencies specified by the project instead.

### Step 5: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 6: Create an Admin Account

```bash
python manage.py createsuperuser
```

Follow the terminal prompts to set your username, email address, and password.

If a superuser already exists, you do not need to create another one.

### Step 7: Start the Development Server

```bash
python manage.py runserver
```

### Step 8: Open the Application

Open these addresses in your browser:

- **Website:** http://127.0.0.1:8000/
- **Django Admin:** http://127.0.0.1:8000/admin/

The website URL may differ if the project uses a different URL configuration.

## Payment Configuration

WorkNest uses Razorpay in Test Mode for payment integration.

- Configure the required Razorpay test credentials using the project's existing settings.
- Keep secret keys and other credentials private.
- Do not commit `.env` files or real payment credentials to GitHub.
- Use test credentials when testing payments.

## Basic Project Checks

To check the Django project configuration, run:

```bash
python manage.py check
```

To run the project's automated tests, if configured, run:

```bash
python manage.py test
```

## Project Structure

The project may contain the following components, depending on its current implementation:

- `manage.py` – Django command-line utility
- Project configuration – Django settings and URL configuration
- Application modules – Models, views, forms, URLs, and business logic
- `templates/` – HTML templates
- `static/` – CSS, JavaScript, and other static files
- `Documentation/` – Project documentation
- `requirements.txt` – Python dependency list, if included

## Future Enhancements

Possible future improvements include:

- Email notifications for booking confirmation
- Advanced workspace search and filtering
- Improved analytics and reporting
- Additional online payment options
- Enhanced mobile responsiveness

## Conclusion

WorkNest provides a web-based solution for managing co-working space bookings, memberships, payments, and related operations. The project demonstrates the use of Django, database management, frontend technologies, and payment integration in a practical web application.