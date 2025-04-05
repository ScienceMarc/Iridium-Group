# Iridium-Group

## How to Use This Project

1. **Install Prerequisites**:
    - Ensure you have **MySQL** and **Python 3** installed on your system.
    - Install the `mysql-connector` Python library

2. **Set Up the Database**:
    - Run the `create_library_data.sql` script in MySQL to create the necessary database and tables
    - ``` SOURCE create_library_data.sql; ```

3. **Import Data**:
    - Execute the `import_data.py` script to load the CSV files from Milestone 1 into the database:
    - ``` python3 import_data.py ```

4. **Run Requirements**:
    - After setting up, you can execute the following features in any order:
      - **Book Search and Availability**:
        - You can modify the search criteria by inserting the keyword in line 48 of the code then execute the `search_books.py` script.
        - If nothing is changed, a search with the keyword "will" shall be executed.
        - ``` python3 search_books.py ```

      - **Book Loans**:
        - You can modify the search criteria by inserting the keyword in line 48 of the code then execute the `book_loans.py` script.
        - ``` python3 book_loans.py ```

      - **Borrower Management**:
        - You can modify the borrower information by modifying the information in lines 53-56 of the code then execute the `borrower_management.py` script.
        - If nothing is changed, borrower "Nick Halden" will be created.
        - After creation, the script can be run again to view the error message if a borrower with the same SSN were to be added.
        - ``` python3 borrower_management.py ```

      - **Fines**:
        - Execute the `fines.py` script.
        - ``` python3 fines.py ```
