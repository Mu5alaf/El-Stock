# Order Processing System

## Description

This project is a simplified Order Processing System for an online store. It handles order processing, including stock validation, payment processing with a mock payment gateway, and sending order confirmation emails to customers.

## Features

1. **Stock Management**: Validates product availability and updates stock counts after each successful order.
2. **Payment Processing**: Integrates with a mock payment gateway to simulate payment processing.
3. **Order Confirmation Emails**: Sends order confirmation emails to customers with order details.
4. **Error Handling**: Manages issues gracefully during the order processing flow.
5. **User Authentication**: Ensures only registered users can place orders.

## Setup

### Prerequisites

- Python 3.9 or higher
- Docker (for containerization)
- Django 4.2.13

### Installation

1. Clone the repository:

    ```sh
    git clone <[repository_url](https://github.com/Mu5alaf/Order-Processing-System.git)>
    cd <Order-Processing-System>
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Run the database migrations:

    ```sh
    python manage.py migrate
    ```

5. Create a superuser:

    ```sh
    python manage.py createsuperuser
    ```

6. Start the development server:

    ```sh
    python manage.py runserver
    ```

### Docker Setup

1. Build the Docker image:

    ```sh
    docker build -t order-processing-system .
    ```

2. Run the Docker container:

    ```sh
    docker run -d -p 8000:8000 order-processing-system
    ```

## Usage

1. Access the application at `http://localhost:8000`.
2. Register a new user or log in with an existing user.
3. Browse products and add them to the cart.
4. Proceed to checkout and complete the order.

## Mock Payment Gateway

The project uses a mock payment gateway for simulating payments. Payment success is always returned.

## Email Configuration

To enable email sending, configure the email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your_smtp_server'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
