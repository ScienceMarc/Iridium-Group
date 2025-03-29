import csv

# ISBN10	ISBN13	Title	Author	Cover	Publisher	Pages
book_data = {
    'ISBN10': [],
    'ISBN13': [],
    'Title': [],
    'Author': [],
    'Cover': [],
    'Publisher': [],
    'Pages': [],
}

# ID0000id,ssn,first_name,last_name,email,address,city,state,phone
borrower_data = {
    'ID': [],
    'SSN': [],
    'First Name': [],
    'Last Name': [],
    'Email': [],
    'Address': [],
    'City': [],
    'State': [],
    'Phone': [],
}

# Output file schemas

book_csv_data = {
    'Isbn': book_data['ISBN10'], # ISBN10 could just be grabbed
    'Title': book_data['Title'], # Title could just be grabbed
}

book_authors_csv_data = {
    'Author_id': [],
    'Isbn': [],
}

authors_csv_data = {
    'Author_id': [],
    'Name': [],
}

borrower_csv_data = {
    'Card_id': [],
    'Ssn': [],
    'Bname': [],
    'Address': [],
    'Phone': [],
}

# Ingest the books CSV
book_file = open('books.csv', 'r')
reader = csv.reader(book_file, delimiter='\t')
next(reader)  # Skip the header row
for row in reader:
    if len(row) != 7:
        print('Invalid row')
        exit()
    # Empty fields are replaced with 'NULL'
    book_data['ISBN10'].append(row[0])
    book_data['ISBN13'].append(row[1])
    book_data['Title'].append(row[2] == '' and 'NULL' or row[2])
    book_data['Author'].append(row[3] == '' and 'NULL' or row[3])
    book_data['Cover'].append(row[4] == '' and 'NULL' or row[4])
    book_data['Publisher'].append(row[5] == '' and 'NULL' or row[5])
    book_data['Pages'].append(row[6] == '' and 'NULL' or row[6])

book_file.close()

borrower_file = open('borrowers.csv', 'r')
reader = csv.reader(borrower_file, delimiter=',')
next(reader)  # Skip the header row
for row in reader:
    if len(row) != 9:
        print('Invalid row')
        print(row)
        exit()
    # Empty fields are replaced with 'NULL'
    borrower_data['ID'].append(row[0])
    borrower_data['SSN'].append(row[1])
    borrower_data['First Name'].append(row[2] == '' and 'NULL' or row[2])
    borrower_data['Last Name'].append(row[3] == '' and 'NULL' or row[3])
    borrower_data['Email'].append(row[4] == '' and 'NULL' or row[4])
    borrower_data['Address'].append(row[5] == '' and 'NULL' or row[5])
    borrower_data['City'].append(row[6] == '' and 'NULL' or row[6])
    borrower_data['State'].append(row[7] == '' and 'NULL' or row[7])
    borrower_data['Phone'].append(row[8] == '' and 'NULL' or row[8])


# Needed author IDs, so hashmap used to find unique names
authorNames = set()
for author in book_data['Author']:
    names = author.split(',')
    for name in names:
        authorNames.add(name.strip())

# Convert set to list, so that we can get index of author name
authorNames = list(authorNames)
for i in range(len(authorNames)):
    authors_csv_data['Author_id'].append(i)
    authors_csv_data['Name'].append(authorNames[i])

# Create book_authors_csv_data
for i in range(len(book_data['ISBN10'])):
    authorList = book_data['Author'][i].split(',')
    for author in authorList:
        authorIndex = authorNames.index(author.strip())
        book_authors_csv_data['Author_id'].append(authorIndex)
        book_authors_csv_data['Isbn'].append(book_data['ISBN10'][i])

# Create borrower_csv_data
for i in range(len(borrower_data['ID'])):
    borrower_csv_data['Card_id'].append(borrower_data['ID'][i])
    borrower_csv_data['Ssn'].append(borrower_data['SSN'][i])
    borrower_csv_data['Bname'].append(borrower_data['First Name'][i] + ' ' + borrower_data['Last Name'][i])
    borrower_csv_data['Address'].append(borrower_data['Address'][i] + ', ' + borrower_data['City'][i] + ', ' + borrower_data['State'][i])
    borrower_csv_data['Phone'].append(borrower_data['Phone'][i])

# Write to CSV files, very repetitive
book_file = open('book.csv', 'w')
writer = csv.writer(book_file, delimiter=',')
writer.writerow(['Isbn', 'Title'])
for i in range(len(book_csv_data['Isbn'])):
    writer.writerow([book_csv_data['Isbn'][i], book_csv_data['Title'][i]])
book_file.close()

book_authors_file = open('book_authors.csv', 'w')
writer = csv.writer(book_authors_file, delimiter=',')
writer.writerow(['Author_id', 'Isbn'])
for i in range(len(book_authors_csv_data['Author_id'])):
    writer.writerow([book_authors_csv_data['Author_id'][i], book_authors_csv_data['Isbn'][i]])
book_authors_file.close()

authors_file = open('authors.csv', 'w')
writer = csv.writer(authors_file, delimiter=',')
writer.writerow(['Author_id', 'Name'])
for i in range(len(authors_csv_data['Author_id'])):
    writer.writerow([authors_csv_data['Author_id'][i], authors_csv_data['Name'][i]])
authors_file.close()

borrower_file = open('borrower.csv', 'w')
writer = csv.writer(borrower_file, delimiter=',')
writer.writerow(['Card_id', 'Ssn', 'Bname', 'Address', 'Phone'])
for i in range(len(borrower_csv_data['Card_id'])):
    writer.writerow([borrower_csv_data['Card_id'][i], borrower_csv_data['Ssn'][i], borrower_csv_data['Bname'][i], borrower_csv_data['Address'][i], borrower_csv_data['Phone'][i]])
borrower_file.close()
