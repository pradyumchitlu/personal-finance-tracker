from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import transactions
from ..models import Transaction, Budget, db
from datetime import datetime
import plotly
import plotly.graph_objs as go
import json

@transactions.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        description = request.form.get('description')
        transaction_type = request.form.get('transaction_type')
        date_str = request.form.get('date')
        
        date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()
        
        new_transaction = Transaction(
            user_id=current_user.id,
            amount=amount,
            category=category,
            description=description,
            transaction_type=transaction_type,
            date=date
        )
        
        db.session.add(new_transaction)
        db.session.commit()
        
        flash('Transaction added successfully!')
        return redirect(url_for('main.dashboard'))
    
    return render_template('add_transaction.html', current_date=datetime.now().strftime('%Y-%m-%d'))

@transactions.route('/set_budget', methods=['GET', 'POST'])
@login_required
def set_budget():
    if request.method == 'POST':
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))
        
        existing_budget = Budget.query.filter_by(
            user_id=current_user.id,
            category=category,
            month=month,
            year=year
        ).first()
        
        if existing_budget:
            existing_budget.amount = amount
        else:
            new_budget = Budget(
                user_id=current_user.id,
                category=category,
                amount=amount,
                month=month,
                year=year
            )
            db.session.add(new_budget)
        
        db.session.commit()
        flash('Budget set successfully!')
        return redirect(url_for('main.dashboard'))
    
    current_date = datetime.now()
    return render_template('set_budget.html',
                         current_month=current_date.month,
                         current_year=current_date.year)

@transactions.route('/reports')
@login_required
def reports():
    transactions = Transaction.query.filter_by(
        user_id=current_user.id,
        transaction_type='expense'
    ).all()
    
    category_totals = {}
    for transaction in transactions:
        category_totals[transaction.category] = category_totals.get(
            transaction.category, 0) + transaction.amount
    
    labels = list(category_totals.keys())
    values = list(category_totals.values())
    
    pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values)])
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('reports.html', pie_chart=pie_chart_json)
