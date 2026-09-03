# Hospital-patient
# Hospital Patient Data Management

## Project Overview

Hospital Patient Data Management is a Python-based application developed
for managing patient information and improving data quality.

The system uses SQLite for database management and performs SQL CRUD
operations, data cleaning, validation, normalization, and fuzzy duplicate
detection.

## Technologies Used

- Python
- SQLite
- SQL
- Regular Expressions (RegEx)
- Fuzzy String Matching

## Features

- Create Patient table
- Insert patient records
- SELECT patient records
- UPDATE patient records
- DELETE inappropriate records
- Normalize patient names
- Standardize gender values
- Validate phone numbers
- Validate email addresses
- Validate patient age
- Handle missing values
- Detect exact duplicate records
- Detect potential duplicates using fuzzy matching
- Store cleaned records in Clean_Patient table

## Database Tables

### Patient

The Patient table contains:

- Patient_ID
- Name
- Age
- Gender
- Phone
- Email
- Diagnosis

### Clean_Patient

The Clean_Patient table stores validated and cleaned patient records.

## Data Cleaning

The system performs:

1. Name normalization
2. Gender standardization
3. Phone number validation
4. Email validation
5. Age validation
6. Missing value handling
7. Exact duplicate detection
8. Fuzzy duplicate detection

## Algorithms Used

### RegEx

Regular expressions are used to validate phone numbers and email addresses.

### Fuzzy Matching

Python's SequenceMatcher is used to identify patient names that are
potentially similar.

## How to Run

### Step 1

Install Python 3.x.

### Step 2

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/Hospital-Patient-Data-Management.git
