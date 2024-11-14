from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .models import Transaction, Budget

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Get user's transactions
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(
        Transaction.date.desc()).limit(10).all()
    
    # Calculate total income and expenses
    income = sum(t.amount for t in Transaction.query.filter_by(
        user_id=current_user.id, transaction_type='income').all())
    expenses = sum(t.amount for t in Transaction.query.filter_by(
        user_id=current_user.id, transaction_type='expense').all())
    
    # Get current month's budgets
    from datetime import datetime
    current_month = datetime.now().month
    current_year = datetime.now().year
    budgets = Budget.query.filter_by(
        user_id=current_user.id, 
        month=current_month, 
        year=current_year
    ).all()
    
    # Calculate budget status
    budget_status = []
    for budget in budgets:
        category_expenses = sum(t.amount for t in Transaction.query.filter_by(
            user_id=current_user.id, 
            transaction_type='expense', 
            category=budget.category
        ).all())
        
        status = {
            'category': budget.category,
            'budget_amount': budget.amount,
            'current_spending': category_expenses,
            'remaining': budget.amount - category_expenses,
            'percentage_used': (category_expenses / budget.amount * 100) if budget.amount > 0 else 0
        }
        budget_status.append(status)
    
    return render_template(
        'dashboard.html', 
        transactions=transactions, 
        income=income, 
        expenses=expenses,
        budget_status=budget_status
    )
