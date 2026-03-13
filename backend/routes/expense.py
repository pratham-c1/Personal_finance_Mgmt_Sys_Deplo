from flask import Blueprint, request, jsonify, session
from database import execute_query, execute_one

expense_bp = Blueprint('expense', __name__)
def uid(): return session.get('user_id')

@expense_bp.route('/api/expense', methods=['GET'])
def get_expense():
    year = request.args.get('year')
    month = request.args.get('month')
    category = request.args.get('category')
    q = "SELECT * FROM expenditure WHERE user_id=%s"
    p = [uid()]
    if year:     q += " AND year_bs=%s";     p.append(year)
    if month:    q += " AND month_num=%s";   p.append(month)
    if category: q += " AND category=%s";    p.append(category)
    q += " ORDER BY date_ad DESC"
    return jsonify(execute_query(q, p))

@expense_bp.route('/api/expense', methods=['POST'])
def add_expense():
    d = request.get_json()
    id_ = execute_query(
        "INSERT INTO expenditure (user_id,date_bs,date_ad,year_bs,month_bs,month_num,category,particular,quantity,rate,amount,remarks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (uid(),d['date_bs'],d['date_ad'],d['year_bs'],d['month_bs'],d['month_num'],d['category'],d.get('particular',''),d.get('quantity',1),d.get('rate',0),d['amount'],d.get('remarks','')), fetch=False)
    return jsonify({'success': True, 'id': id_})

@expense_bp.route('/api/expense/<int:id>', methods=['PUT'])
def update_expense(id):
    d = request.get_json()
    execute_query(
        "UPDATE expenditure SET date_bs=%s,date_ad=%s,year_bs=%s,month_bs=%s,month_num=%s,category=%s,particular=%s,quantity=%s,rate=%s,amount=%s,remarks=%s WHERE id=%s AND user_id=%s",
        (d['date_bs'],d['date_ad'],d['year_bs'],d['month_bs'],d['month_num'],d['category'],d.get('particular',''),d.get('quantity',1),d.get('rate',0),d['amount'],d.get('remarks',''),id,uid()), fetch=False)
    return jsonify({'success': True})

@expense_bp.route('/api/expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    execute_query("DELETE FROM expenditure WHERE id=%s AND user_id=%s", (id, uid()), fetch=False)
    return jsonify({'success': True})

@expense_bp.route('/api/expense/summary', methods=['GET'])
def expense_summary():
    year = request.args.get('year')
    q = "SELECT category, SUM(amount) as total FROM expenditure WHERE user_id=%s"
    p = [uid()]
    if year: q += " AND year_bs=%s"; p.append(year)
    q += " GROUP BY category ORDER BY total DESC"
    return jsonify(execute_query(q, p))

@expense_bp.route('/api/expense/monthly', methods=['GET'])
def monthly_expense():
    year = request.args.get('year')
    q = "SELECT month_num, month_bs, SUM(amount) as total FROM expenditure WHERE user_id=%s"
    p = [uid()]
    if year: q += " AND year_bs=%s"; p.append(year)
    q += " GROUP BY month_num, month_bs ORDER BY month_num"
    return jsonify(execute_query(q, p))
