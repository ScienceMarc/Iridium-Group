/*
 *    File name: create_library_data.sql
 *       Author: Azlaan Shafi, Shiv Bhavsar
 *    Last Edit: 2025-03-31
 *  Description: This file is created for the Milestone 2 
 *               part of the CS4347 Project.
 *
 */


 -- If the database "LIBRARY" already exists, then delete it.
DROP DATABASE IF EXISTS LIBRARY_SYSTEM;
-- Create the Database "LIBRARY"
CREATE DATABASE LIBRARY_SYSTEM;

-- Set the currently active database to be "LIBRARY"
USE LIBRARY_SYSTEM;

DROP TABLE IF EXISTS BOOK;
CREATE TABLE BOOK (
  Isbn       CHAR(10) NOT NULL, 
  Title      VARCHAR(100) NOT NULL,
  CONSTRAINT pk_book PRIMARY KEY (Isbn)
);  

DROP TABLE IF EXISTS AUTHORS;
CREATE TABLE AUTHORS (
  Author_id     INT NOT NULL, 
  Name          VARCHAR(25) NOT NULL,
  CONSTRAINT pk_authors PRIMARY KEY (Author_id)
);

DROP TABLE IF EXISTS BORROWER;
CREATE TABLE BORROWER (
  Card_id       CHAR(8) NOT NULL,
  Ssn           CHAR(9) NOT NULL UNIQUE, 
  BName         VARCHAR(50) NOT NULL,
  Address       VARCHAR(100) NOT NULL,
  Phone         CHAR(14) NOT NULL,
  CONSTRAINT pk_borrower PRIMARY KEY (Card_id)
);

DROP TABLE IF EXISTS BOOK_AUTHORS;
CREATE TABLE BOOK_AUTHORS (
  Author_id     INT NOT NULL, 
  Isbn          CHAR(10) NOT NULL,
  CONSTRAINT pk_book_authors PRIMARY KEY (Isbn, Author_id),
  CONSTRAINT fk_book_authors_isbn FOREIGN KEY (Isbn) REFERENCES BOOK(Isbn),
  CONSTRAINT fk_book_authors_author FOREIGN KEY (Author_id) REFERENCES AUTHORS(Author_id)
);

DROP TABLE IF EXISTS BOOK_LOANS;
CREATE TABLE BOOK_LOANS (
  Loan_id     INT NOT NULL,
  Isbn        CHAR(10) NOT NULL, 
  Card_id     CHAR(8) NOT NULL,
  Date_out    DATE NOT NULL,
  Date_due    DATE NOT NULL,
  Date_in     DATE,
  CONSTRAINT pk_book_loans PRIMARY KEY (Loan_id),
  CONSTRAINT fk_book_loans_isbn FOREIGN KEY (Isbn) REFERENCES BOOK(Isbn),
  CONSTRAINT fk_book_loans_card FOREIGN KEY (Card_id) REFERENCES BORROWER(Card_id)
);

DROP TABLE IF EXISTS FINES;
CREATE TABLE FINES (
  Loan_id     INT NOT NULL, 
  Fine_amt    DECIMAL(10,2) NOT NULL,
  Paid        BOOLEAN DEFAULT 0 NOT NULL,
  CONSTRAINT pk_fines PRIMARY KEY (Loan_id),
  CONSTRAINT fk_fines_loan FOREIGN KEY (Loan_id) REFERENCES BOOK_LOANS(Loan_id)
);









