# Library Management System

A Django-based web application for managing library operations including book search, checkout, returns, and fine management.

## Features

- Book search by ISBN, title, or author
- Book checkout and return functionality
- Borrower management
- Fine calculation and payment processing
- User-friendly web interface

## Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd library-management-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a MySQL database named `LIBRARY_SYSTEM`:
```sql
CREATE DATABASE LIBRARY_SYSTEM;
```

5. Update database settings in `library_portal/settings.py` with your MySQL credentials if needed.

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Open your web browser and navigate to:
```
http://localhost:8000
```

3. For admin access, go to:
```
http://localhost:8000/admin
```

## Usage

### Book Search
- Use the search bar to find books by ISBN, title, or author
- Results show book availability and borrower information
- Click "Check Out" to borrow a book
- Click "Check In" to return a book

### Fine Management
- Search for fines by borrower ID or name
- View fine details including amount and status
- Pay fines for returned books

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.