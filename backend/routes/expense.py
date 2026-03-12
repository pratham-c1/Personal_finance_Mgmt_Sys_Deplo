from flask import Blueprint, request, jsonify
from database import execute_query, execute_one

expense_bp = Blueprint('expense', __name__)

@expense_bp.route('/api/expense', methods=['GET'])
def get_expenses():
    year = request.args.get('year')
    month = request.args.get('month')
    category = request.args.get('category')
    query = "SELECT * FROM expenditure WHERE 1=1"
    params = []
    if year: query += " AND year_bs=%s"; params.append(year)
    if month: query += " AND month_num=%s"; params.append(month)
    if category: query += " AND category=%s"; params.append(category)
    query += " ORDER BY date_ad DESC"
    data = execute_query(query, params)
    result = []
    for r in data:
        d = dict(r)
        d['date_ad'] = str(d['date_ad'])
        d['created_at'] = str(d['created_at'])
        result.append(d)
    return jsonify(result)

@expense_bp.route('/api/expense', methods=['POST'])
def add_expense():
    d = request.get_json()
    qty = float(d.get('quantity', 1))
    rate = float(d.get('rate', 0))
    amount = qty * rate if rate > 0 else float(d.get('amount', 0))
    execute_query("""
        INSERT INTO expenditure (date_bs, date_ad, year_bs, month_bs, month_num, category,
        particular, quantity, rate, amount, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          d['category'], d.get('particular',''), qty, rate, amount, d.get('remarks','')), fetch=False)
    return jsonify({'success': True, 'message': 'Expense added successfully'})

@expense_bp.route('/api/expense/<int:id>', methods=['PUT'])
def update_expense(id):
    d = request.get_json()
    qty = float(d.get('quantity', 1))
    rate = float(d.get('rate', 0))
    amount = qty * rate if rate > 0 else float(d.get('amount', 0))
    execute_query("""
        UPDATE expenditure SET date_bs=%s, date_ad=%s, year_bs=%s, month_bs=%s, month_num=%s,
        category=%s, particular=%s, quantity=%s, rate=%s, amount=%s, remarks=%s WHERE id=%s
    """, (d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          d['category'], d.get('particular',''), qty, rate, amount, d.get('remarks',''), id), fetch=False)
    return jsonify({'success': True, 'message': 'Expense updated successfully'})

@expense_bp.route('/api/expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    execute_query("DELETE FROM expenditure WHERE id=%s", (id,), fetch=False)
    return jsonify({'success': True, 'message': 'Expense deleted successfully'})

@expense_bp.route('/api/expense/summary', methods=['GET'])
def expense_summary():
    data = execute_query("SELECT category, SUM(amount) as total FROM expenditure GROUP BY category ORDER BY total DESC")
    return jsonify([dict(r) for r in data])

@expense_bp.route('/api/expense/monthly', methods=['GET'])
def monthly_expense():
    data = execute_query("""
        SELECT year_bs, month_bs, month_num, SUM(amount) as total
        FROM expenditure GROUP BY year_bs, month_num, month_bs ORDER BY year_bs DESC, month_num DESC
    """)
    return jsonify([dict(r) for r in data])
