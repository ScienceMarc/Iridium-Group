/*
 *    File name: create_library_data.sql
 *       Author: Azlaan Shafi
 *    Last Edit: 2025-03-29
 *  Description: This file is created for the Milestone 2 
 *               part of the CS4347 Project.
 *
 */


 -- If the database "LIBRARY" already exists, then delete it.
DROP DATABASE IF EXISTS LIBRARY;
-- Create the Database "LIBRARY"
CREATE DATABASE LIBRARY;

-- Set the currently active database to be "LIBRARY"
USE LIBRARY;

DROP TABLE IF EXISTS FINES;
CREATE TABLE FINES (
  Loan_id     INT NOT NULL, 
  Fine_amt    DECIMAL(10,2) NOT NULL,
  Paid        BOOLEAN DEFAULT 0 NOT NULL,
  CONSTRAINT pk_fines PRIMARY KEY (Loan_id)
);

DROP TABLE IF EXISTS BOOK_LOANS;
CREATE TABLE BOOK_LOANS (
  Loan_id     INT NOT NULL,
  Isbn        CHAR(9) NOT NULL, 
  Card_id     CHAR(8) NOT NULL,
  Date_out    DATE NOT NULL,
  Date_due    DATE NOT NULL,
  Date_in     DATE,
  CONSTRAINT pk_book_loans PRIMARY KEY (Loan_id),
  CONSTRAINT fk_book_loans FOREIGN KEY (Loan_id) references FINES(Loan_id)
);

DROP TABLE IF EXISTS BOOK_AUTHORS;
CREATE TABLE BOOK_AUTHORS (
  Author_id     INT NOT NULL, 
  Isbn          CHAR(9) NOT NULL,
  CONSTRAINT pk_book_authors PRIMARY KEY (Author_id)
);

DROP TABLE IF EXISTS BOOK;
CREATE TABLE BOOK (
  Isbn       CHAR(9) NOT NULL, 
  Title      VARCHAR(25) NOT NULL,
  CONSTRAINT pk_book PRIMARY KEY (Isbn),
  CONSTRAINT fk_book_isbn FOREIGN KEY (Isbn) references BOOK_AUTHORS(Isbn),
  CONSTRAINT fk_book_isbn FOREIGN KEY (Isbn) references BOOK_LOANS(Isbn)
);  

DROP TABLE IF EXISTS AUTHORS;
CREATE TABLE AUTHORS (
  Author_id     INT NOT NULL, 
  Name          VARCHAR(25) NOT NULL,
  CONSTRAINT pk_authors PRIMARY KEY (Author_id),
  CONSTRAINT fk_authors_id FOREIGN KEY (Author_id) references BOOK_AUTHORS(Author_id)
);

DROP TABLE IF EXISTS BORROWER;
CREATE TABLE BORROWER (
  Card_id       CHAR(8) NOT NULL,
  Ssn           CHAR(9) UNIQUE NOT NULL, 
  BName         VARCHAR(25) NOT NULL,
  Address       VARCHAR(50) NOT NULL,
  City          VARCHAR(25) NOT NULL,
  State         CHAR(2) NOT NULL,
  Phone         CHAR(14) NOT NULL,
  CONSTRAINT pk_borrower PRIMARY KEY (Card_id),
  CONSTRAINT fk_borrower_id FOREIGN KEY (Card_id) references BOOK_LOANS(Card_id)
);