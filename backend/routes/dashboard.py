from flask import Blueprint, jsonify, session
from database import execute_one, execute_query

dashboard_bp = Blueprint('dashboard', __name__)

def uid(): return session.get('user_id')

@dashboard_bp.route('/api/dashboard/summary', methods=['GET'])
def get_summary():
    u = uid()
    income  = execute_one("SELECT COALESCE(SUM(amount),0) as total FROM income WHERE user_id=%s", (u,))
    expense = execute_one("SELECT COALESCE(SUM(amount),0) as total FROM expenditure WHERE user_id=%s", (u,))
    nw      = execute_one("SELECT net_worth FROM net_worth WHERE user_id=%s ORDER BY date_ad DESC LIMIT 1", (u,))
    loans   = execute_one("SELECT COALESCE(SUM(principal),0) as total FROM loans WHERE user_id=%s AND status='active'", (u,))
    shares  = execute_one("SELECT COALESCE(SUM(current_value),0) as total FROM shares WHERE user_id=%s", (u,))
    total_income  = float(income['total'])  if income  else 0
    total_expense = float(expense['total']) if expense else 0
    return jsonify({
        'total_income':  total_income,
        'total_expense': total_expense,
        'savings':       total_income - total_expense,
        'net_worth':     float(nw['net_worth']) if nw else 0,
        'loan_amount':   float(loans['total'])  if loans else 0,
        'share_value':   float(shares['total']) if shares else 0,
    })

@dashboard_bp.route('/api/dashboard/monthly-income', methods=['GET'])
def monthly_income():
    data = execute_query("""
        SELECT month_bs, month_num, year_bs, SUM(amount) as total
        FROM income WHERE user_id=%s
        GROUP BY year_bs, month_num, month_bs
        ORDER BY year_bs DESC, month_num DESC LIMIT 12
    """, (uid(),))
    return jsonify([dict(r) for r in data])

@dashboard_bp.route('/api/dashboard/monthly-expense', methods=['GET'])
def monthly_expense():
    data = execute_query("""
        SELECT month_bs, month_num, year_bs, SUM(amount) as total
        FROM expenditure WHERE user_id=%s
        GROUP BY year_bs, month_num, month_bs
        ORDER BY year_bs DESC, month_num DESC LIMIT 12
    """, (uid(),))
    return jsonify([dict(r) for r in data])

@dashboard_bp.route('/api/dashboard/expense-categories', methods=['GET'])
def expense_categories():
    data = execute_query("""
        SELECT category, SUM(amount) as total
        FROM expenditure WHERE user_id=%s
        GROUP BY category ORDER BY total DESC
    """, (uid(),))
    return jsonify([dict(r) for r in data])

@dashboard_bp.route('/api/dashboard/networth-trend', methods=['GET'])
def networth_trend():
    data = execute_query("""
        SELECT date_ad, net_worth FROM net_worth
        WHERE user_id=%s ORDER BY date_ad DESC LIMIT 30
    """, (uid(),))
    result = []
    for r in data:
        d = dict(r)
        d['date_ad'] = str(d['date_ad'])
        result.append(d)
    return jsonify(result)
