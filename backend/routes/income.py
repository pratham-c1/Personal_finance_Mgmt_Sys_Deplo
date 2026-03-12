from flask import Blueprint, request, jsonify
from database import execute_query, execute_one

income_bp = Blueprint('income', __name__)

@income_bp.route('/api/income', methods=['GET'])
def get_income():
    year = request.args.get('year')
    month = request.args.get('month')
    category = request.args.get('category')
    query = "SELECT * FROM income WHERE 1=1"
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

@income_bp.route('/api/income', methods=['POST'])
def add_income():
    d = request.get_json()
    execute_query("""
        INSERT INTO income (date_bs, date_ad, year_bs, month_bs, month_num, category, amount, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          d['category'], d['amount'], d.get('remarks', '')), fetch=False)
    return jsonify({'success': True, 'message': 'Income added successfully'})

@income_bp.route('/api/income/<int:id>', methods=['PUT'])
def update_income(id):
    d = request.get_json()
    execute_query("""
        UPDATE income SET date_bs=%s, date_ad=%s, year_bs=%s, month_bs=%s, month_num=%s,
        category=%s, amount=%s, remarks=%s WHERE id=%s
    """, (d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          d['category'], d['amount'], d.get('remarks', ''), id), fetch=False)
    return jsonify({'success': True, 'message': 'Income updated successfully'})

@income_bp.route('/api/income/<int:id>', methods=['DELETE'])
def delete_income(id):
    execute_query("DELETE FROM income WHERE id=%s", (id,), fetch=False)
    return jsonify({'success': True, 'message': 'Income deleted successfully'})

@income_bp.route('/api/income/summary', methods=['GET'])
def income_summary():
    data = execute_query("SELECT category, SUM(amount) as total FROM income GROUP BY category")
    return jsonify([dict(r) for r in data])
