from flask import Blueprint, jsonify, session
from database import execute_one, execute_query

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/summary', methods=['GET'])
def get_summary():
    # Total income
    income = execute_one("SELECT COALESCE(SUM(amount),0) as total FROM income")
    # Total expense
    expense = execute_one("SELECT COALESCE(SUM(amount),0) as total FROM expenditure")
    # Latest net worth
    nw = execute_one("SELECT net_worth FROM net_worth ORDER BY date_ad DESC LIMIT 1")
    # Active loans total
    loans = execute_one("SELECT COALESCE(SUM(principal),0) as total FROM loans WHERE status='active'")
    # Share portfolio value
    shares = execute_one("SELECT COALESCE(SUM(current_value),0) as total FROM shares")
    
    total_income = float(income['total']) if income else 0
    total_expense = float(expense['total']) if expense else 0
    savings = total_income - total_expense
    net_worth = float(nw['net_worth']) if nw else 0
    loan_amount = float(loans['total']) if loans else 0
    share_value = float(shares['total']) if shares else 0
    
    return jsonify({
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': savings,
        'net_worth': net_worth,
        'loan_amount': loan_amount,
        'share_value': share_value
    })

@dashboard_bp.route('/api/dashboard/monthly-income', methods=['GET'])
def monthly_income():
    data = execute_query("""
        SELECT month_bs, month_num, year_bs, SUM(amount) as total
        FROM income GROUP BY year_bs, month_num, month_bs ORDER BY year_bs, month_num DESC LIMIT 12
    """)
    return jsonify([dict(r) for r in data])

@dashboard_bp.route('/api/dashboard/monthly-expense', methods=['GET'])
def monthly_expense():
    data = execute_query("""
        SELECT month_bs, month_num, year_bs, SUM(amount) as total
        FROM expenditure GROUP BY year_bs, month_num, month_bs ORDER BY year_bs, month_num DESC LIMIT 12
    """)
    return jsonify([dict(r) for r in data])

@dashboard_bp.route('/api/dashboard/expense-categories', methods=['GET'])
def expense_categories():
    data = execute_query("""
        SELECT category, SUM(amount) as total FROM expenditure GROUP BY category ORDER BY total DESC
    """)
    return jsonify([dict(r) for r in data])

@dashboard_bp.route('/api/dashboard/networth-trend', methods=['GET'])
def networth_trend():
    data = execute_query("""
        SELECT date_ad, net_worth FROM net_worth ORDER BY date_ad DESC LIMIT 30
    """)
    result = []
    for r in data:
        d = dict(r)
        d['date_ad'] = str(d['date_ad'])
        result.append(d)
    return jsonify(result)
