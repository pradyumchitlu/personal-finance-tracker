# Personal Finance Tracker

## Overview
A comprehensive web application for tracking personal finances, managing budgets, and gaining insights into spending habits.

## Features
- User Authentication
- Income and Expense Tracking
- Budget Setting and Monitoring
- Spending Visualization
- Data Export and Analysis

## Tech Stack
- Backend: Flask (Python)
- Database: SQLite
- Frontend: HTML, CSS, Bootstrap
- Data Visualization: Plotly

## Setup and Installation

### Prerequisites
- Python 3.8+
- pip

### Installation Steps
1. Clone the repository
```bash
git clone https://github.com/yourusername/personal-finance-tracker.git
cd personal-finance-tracker
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
- Copy `.env.example` to `.env`
- Update the values in `.env`

5. Initialize the database
```bash
flask db upgrade
```

6. Run the application
```bash
flask run
```

## Usage
- Register a new account
- Add income and expense transactions
- Set monthly budgets
- View dashboard and reports
- Export financial data

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License
