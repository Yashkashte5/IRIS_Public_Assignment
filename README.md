# FastAPI Excel Processor

This project is a FastAPI-based application that reads and parses an Excel file (`/Data/capbudg.xls`) and exposes endpoints to interact with tables and rows in the file.

## Project Overview

The main goal of this application is to demonstrate API development skills using FastAPI, along with parsing structured data from Excel and exposing it through clear, RESTful endpoints.

## Features

- Parses `.xls` Excel sheets into structured Python dictionaries
- Automatically detects section headers and organizes data
- API endpoints to list tables, extract rows, and calculate sums

## API Endpoints

### 1. GET `/list_tables`

**Function:** Returns a list of all parsed table/section names from the Excel file.

**Example Response:**
```json
{
  "tables": ["INITIAL INVESTMENT", "OPERATING CASHFLOWS", "BOOK VALUE & DEPRECIATION"]
}
```

### 2. GET `/get_table_details?table_name=...`

**Function:** Returns the list of row labels (typically first-column entries) under a specified table name.

**Example Response:**
```json
{
  "table": "INITIAL INVESTMENT",
  "rows": [
    "Initial Investment=",
    "Opportunity cost (if any)=",
    "Lifetime of the investment",
    "Salvage Value at end of project=",
    "Deprec. method(1:St.line;2:DDB)=",
    "Tax Credit (if any )=",
    "Other invest.(non-depreciable)="
  ]
}
```

### 3. GET `/row_sum?table_name=...&row_name=...`

**Function:** Calculates the sum of all numeric values in the specified row of the selected table.

**Example Response:**
```json
{
  "table": "INITIAL INVESTMENT",
  "row": "Tax Credit (if any )=",
  "sum": 10
}
```

## Folder Structure

```
.
├── main.py
├── Data/
│   └── capbudg.xls
├── FastAPI_Excel_Parser.postman_collection.json
├── README.md
```

## Your Insights

### Potential Improvements

- Support uploading `.xlsx` files through an API endpoint
- Provide an endpoint to refresh the Excel file in real-time
- Normalize table and row names for case-insensitive access
- Handle merged cells and formatting inconsistencies in complex Excel sheets
- Add frontend support using Streamlit or a simple HTML UI

### Missed Edge Cases

- Empty or corrupt Excel files
- Tables with no numeric data
- Malformed or duplicate table names
- Inconsistent first-column formats (e.g., blank labels or merged headers)
- Unexpected special characters or encoding issues

## Testing

To test the application:

1. Install dependencies:
```bash
pip install fastapi uvicorn pandas openpyxl xlrd
```

2. Run the FastAPI server:
```bash
uvicorn main:app --reload --port 9090
```

3. Access API:
- Swagger UI: http://localhost:9090/docs
- Raw Endpoint: http://localhost:9090/list_tables

## Postman Collection

The Postman collection is included as `FastAPI_Excel_Parser.postman_collection.json` in the root of the project. Import this file into Postman and run the following requests:

- `GET /list_tables`
- `GET /get_table_details?table_name=...`
- `GET /row_sum?table_name=...&row_name=...`

Base URL: `http://localhost:9090`


