# Nails Salon FastAPI Backend

A FastAPI-based backend for managing a nail salon's employees, work records, payments, and work details.

## Features

- **Employee Management**: Create, read, update, and delete employee records
- **Work Tracking**: Record work/services with amounts, tips, and discounts
- **Payment Processing**: Track payments linked to work records
- **Work Details**: Associate employees with work and manage compensation
- **Input Validation**: Pydantic validators for all monetary amounts and percentages
- **Error Handling**: Comprehensive error responses with proper HTTP status codes
- **Logging**: Structured logging for all database operations
- **SQLite Database**: Connection pooling for efficient database access

## Setup

### Prerequisites

- Python 3.10+
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/muahaio123/py_nails_fastapi.git
cd py_nails_fastapi/backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database (optional - configure path via environment variable):
```bash
set DATABASE_PATH=../natural_nails.db
```

## Running the Server

Start the development server:

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

The server will be available at `http://127.0.0.1:8000`

### Interactive API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Employees

- `GET /employees/all_employees` - Retrieve all employees
- `GET /employees/by-id/{emp_id}` - Get employee by ID
- `POST /employees/new_employee` - Create new employee
- `PUT /employees/update_employee` - Update existing employee
- `DELETE /employees/delete_employee/{emp_id}` - Delete employee

### Works

- `GET /works/all_works` - Retrieve all work records
- `GET /works/by-id/{work_id}` - Get work record by ID
- `GET /works/between-dates/{from_datetime}/{to_datetime}` - Get works in date range
- `POST /works/new_work` - Create new work record
- `PUT /works/update_work` - Update existing work record
- `DELETE /works/delete_work/{work_id}` - Delete work record

### Payments

- `GET /payments/all_payments` - Retrieve all payments
- `GET /payments/by-id/{pmt_id}` - Get payment by ID
- `GET /payments/by-pmtids/{pmt_ids}` - Get payments by list of IDs
- `POST /payments/new_payment` - Create new payment
- `PUT /payments/update_payment` - Update existing payment
- `DELETE /payments/delete_payment/{pmt_id}` - Delete payment

### Work Details

- `GET /details/all_details` - Retrieve all work details
- `GET /details/by-id/{detail_id}` - Get work detail by ID
- `GET /details/by-workids` - Get details by work IDs (query param: `work_ids`)
- `GET /details/by-empid/{emp_id}` - Get details by employee ID
- `POST /details/new_detail` - Create new work detail
- `PUT /details/update_detail` - Update existing work detail
- `DELETE /details/delete_detail/{detail_id}` - Delete work detail

## Request/Response Examples

### Create an Employee

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/employees/new_employee" \
  -H "Content-Type: application/json" \
  -d '{
    "emp_name": "John Doe",
    "emp_phone": "555-1234",
    "emp_ssn": "123-45-6789",
    "emp_address": "123 Main St",
    "emp_work_percentage": 50,
    "emp_cash_percentage": 30,
    "emp_salary": 2000
  }'
```

**Response (201 Created):**
```json
{
  "emp_id": 1,
  "emp_name": "John Doe",
  "emp_phone": "555-1234",
  "emp_ssn": "123-45-6789",
  "emp_address": "123 Main St",
  "emp_work_percentage": 50,
  "emp_cash_percentage": 30,
  "emp_salary": 2000
}
```

### Create a Work Record

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/works/new_work" \
  -H "Content-Type: application/json" \
  -d '{
    "work_datetime": "2025-12-08 10:30:00",
    "work_amount": 100.00,
    "work_tip": 20.00,
    "work_discount": 5.00,
    "work_grandtotal": 115.00,
    "work_notes": "Manicure and pedicure"
  }'
```

**Response (201 Created):**
```json
{
  "work_id": 1,
  "work_datetime": "2025-12-08 10:30:00",
  "work_amount": 100.00,
  "work_tip": 20.00,
  "work_discount": 5.00,
  "work_grandtotal": 115.00,
  "work_notes": "Manicure and pedicure"
}
```

## Validation Rules

### Employee
- `emp_work_percentage`: 0-100
- `emp_cash_percentage`: 0-100
- `emp_salary`: >= 0

### Works
- `work_amount`: >= 0
- `work_tip`: >= 0
- `work_discount`: >= 0
- `work_grandtotal`: >= 0

### Payments
- `pmt_amount`: >= 0

### Work Details
- `emp_amount`: >= 0
- `emp_tip`: >= 0

## Error Handling

The API returns standard HTTP status codes:

- `200 OK` - Successful request
- `201 Created` - Resource successfully created
- `400 Bad Request` - Invalid input (validation error)
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server-side error

Error responses include a detail message:
```json
{
  "detail": "Employee 999 not found"
}
```

## Configuration

### Database Path

Set the `DATABASE_PATH` environment variable to customize the database location:

```bash
set DATABASE_PATH=C:\path\to\natural_nails.db
```

Default: `../natural_nails.db`

### Logging

Logs are output to the console with INFO level by default. Check the terminal output for operation logs:

```
2025-12-08 10:30:45 - service.employees - INFO - Employee created: 1 - John Doe
```

## Project Structure

```
backend/
├── main.py                 # FastAPI app and endpoint definitions
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── service/
    ├── database.py        # Connection pool and database utilities
    ├── employees.py       # Employee CRUD operations
    ├── works.py          # Work/service CRUD operations
    ├── payments.py       # Payment CRUD operations
    └── emp_work_detail.py # Work detail CRUD operations
```

## Development

### Running Tests

To test the API, use the interactive Swagger UI at `/docs` or make HTTP requests:

```bash
# Get all employees
curl http://127.0.0.1:8000/employees/all_employees

# Get specific employee
curl http://127.0.0.1:8000/employees/by-id/1
```

### Making Changes

1. Edit service files in `service/` folder
2. The server will auto-reload with `--reload` flag
3. Check logs for any issues
4. Test via Swagger UI or curl

## License

This project is part of the py_nails_fastapi repository.

## Support

For issues or questions, please refer to the main repository: https://github.com/muahaio123/py_nails_fastapi
