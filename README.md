# Iridium-Group

## How to Use This Project

1. **Install Prerequisites**:
    - Ensure you have **MySQL** and **Python 3** installed on your system.
    - Install the `mysql-connector` Python library

2. **Run Script**:
    - Run `script.sh` and all the relevant files for this milestone will run. 
    - It will:
    1. Create the database
    2. Import CSV data from Milestone1
    3. Create a Borrower (Nick Halden)
    4. Search the database for "Nigel Williams"
    5. Checks out a book "Jetzt Will Ich's Wirklich Wissen" for "Nick Halden"
    6. Searches loans by Loan ID (uses Nick Halden's ID)
    7. Checks in the recently checked out book
    8. Update Fines (book_loans file)
    9. Update Fines (fines file)
    10. List a dummy Borrower's fines

    Execute using:
    - ``` bash script.sh ```