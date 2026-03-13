from flask import Blueprint, request, jsonify, session
from database import execute_query, execute_one

income_bp = Blueprint('income', __name__)

def uid(): return session.get('user_id')

@income_bp.route('/api/income', methods=['GET'])
def get_income():
    year = request.args.get('year')
    month = request.args.get('month')
    category = request.args.get('category')
    q = "SELECT * FROM income WHERE user_id = %s"
    p = [uid()]
    if year:     q += " AND year_bs = %s";     p.append(year)
    if month:    q += " AND month_num = %s";   p.append(month)
    if category: q += " AND category = %s";    p.append(category)
    q += " ORDER BY date_ad DESC"
    return jsonify(execute_query(q, p))

@income_bp.route('/api/income', methods=['POST'])
def add_income():
    d = request.get_json()
    id_ = execute_query(
        "INSERT INTO income (user_id,date_bs,date_ad,year_bs,month_bs,month_num,category,amount,remarks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (uid(),d['date_bs'],d['date_ad'],d['year_bs'],d['month_bs'],d['month_num'],d['category'],d['amount'],d.get('remarks','')), fetch=False)
    return jsonify({'success': True, 'id': id_})

@income_bp.route('/api/income/<int:id>', methods=['PUT'])
def update_income(id):
    d = request.get_json()
    execute_query(
        "UPDATE income SET date_bs=%s,date_ad=%s,year_bs=%s,month_bs=%s,month_num=%s,category=%s,amount=%s,remarks=%s WHERE id=%s AND user_id=%s",
        (d['date_bs'],d['date_ad'],d['year_bs'],d['month_bs'],d['month_num'],d['category'],d['amount'],d.get('remarks',''),id,uid()), fetch=False)
    return jsonify({'success': True})

@income_bp.route('/api/income/<int:id>', methods=['DELETE'])
def delete_income(id):
    execute_query("DELETE FROM income WHERE id=%s AND user_id=%s", (id, uid()), fetch=False)
    return jsonify({'success': True})

@income_bp.route('/api/income/summary', methods=['GET'])
def income_summary():
    year = request.args.get('year')
    q = "SELECT category, SUM(amount) as total FROM income WHERE user_id=%s"
    p = [uid()]
    if year: q += " AND year_bs=%s"; p.append(year)
    q += " GROUP BY category ORDER BY total DESC"
    return jsonify(execute_query(q, p))
