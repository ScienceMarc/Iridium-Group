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

## Setup & Running Instructions

### 1. Clone the Repository
```
git clone <repo-url>
cd Iridium-Group
```

### 2. Set Up MySQL Database
- You can use MySQL via Docker or a local installation.
- Make sure your MySQL server is running and accessible.
- Update `library_portal/settings.py` with your MySQL credentials if needed.

#### **If using Docker:**
- Start your MySQL container (example):
  ```
  docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=yourpassword -p 3306:3306 -d mysql:8
  ```
- You do **not** need MySQL Workbench open for the app to work (Workbench is optional for manual DB inspection).

### 3. Set Up Python Environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### 5. Import Initial Data (Only Once)
```
python import_data.py
```
- **Note:** You only need to import data if the database is empty or has been reset. You do NOT need to re-import every time you run the server.

### 6. Run the Development Server
```
python manage.py runserver 8001
```
- Visit [http://127.0.0.1:8001/](http://127.0.0.1:8001/) in your browser.

### 7. Using the App
- **Book Search:** Search by ISBN, title, or author. See availability and borrower info.
- **Book Loans:** Check out/in books by ISBN and borrower card number. Search/filter active loans.
- **Borrower Management:** Add new borrowers. SSN must be unique. Card numbers are auto-generated.
- **Fines:** Update, search, and pay fines. Fines are grouped by borrower. Only pay if all late books are returned. Toggle to view paid/unpaid fines.

### 8. Admin Access (Optional)
- Create a superuser for Django admin:
  ```
  python manage.py createsuperuser
  ```
- Visit [http://127.0.0.1:8001/admin/](http://127.0.0.1:8001/admin/)

---

**Data is persistent as long as your MySQL database is not reset or deleted.**

If you have any issues, check your MySQL connection, Docker container, or reach out for help!

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