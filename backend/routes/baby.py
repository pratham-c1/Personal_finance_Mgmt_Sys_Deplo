from flask import Blueprint, request, jsonify
from database import execute_query, execute_one

baby_bp = Blueprint('baby', __name__)

@baby_bp.route('/api/baby/expense', methods=['GET'])
def get_baby_expense():
    data = execute_query("SELECT * FROM baby_expenditure ORDER BY date_ad DESC")
    result = []
    for r in data:
        d = dict(r)
        if d.get('date_ad'): d['date_ad'] = str(d['date_ad'])
        d['created_at'] = str(d['created_at'])
        result.append(d)
    return jsonify(result)

@baby_bp.route('/api/baby/expense', methods=['POST'])
def add_baby_expense():
    d = request.get_json()
    execute_query("""
        INSERT INTO baby_expenditure (date_bs, date_ad, year_bs, month_bs, month_num, category, particular, amount, remarks)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          d['category'], d.get('particular',''), float(d['amount']), d.get('remarks','')), fetch=False)
    return jsonify({'success': True, 'message': 'Baby expense added'})

@baby_bp.route('/api/baby/expense/<int:id>', methods=['PUT'])
def update_baby_expense(id):
    d = request.get_json()
    execute_query("""
        UPDATE baby_expenditure SET date_bs=%s, date_ad=%s, year_bs=%s, month_bs=%s, month_num=%s,
        category=%s, particular=%s, amount=%s, remarks=%s WHERE id=%s
    """, (d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          d['category'], d.get('particular',''), float(d['amount']), d.get('remarks',''), id), fetch=False)
    return jsonify({'success': True, 'message': 'Baby expense updated'})

@baby_bp.route('/api/baby/expense/<int:id>', methods=['DELETE'])
def delete_baby_expense(id):
    execute_query("DELETE FROM baby_expenditure WHERE id=%s", (id,), fetch=False)
    return jsonify({'success': True, 'message': 'Baby expense deleted'})

@baby_bp.route('/api/baby/gift', methods=['GET'])
def get_baby_gifts():
    data = execute_query("SELECT * FROM baby_gifts ORDER BY date_ad DESC")
    result = []
    for r in data:
        d = dict(r)
        if d.get('date_ad'): d['date_ad'] = str(d['date_ad'])
        d['created_at'] = str(d['created_at'])
        result.append(d)
    return jsonify(result)

@baby_bp.route('/api/baby/gift', methods=['POST'])
def add_baby_gift():
    d = request.get_json()
    execute_query("""
        INSERT INTO baby_gifts (person_name, amount, date_bs, date_ad, remarks)
        VALUES (%s,%s,%s,%s,%s)
    """, (d['person_name'], float(d['amount']), d.get('date_bs',''), d.get('date_ad', None), d.get('remarks','')), fetch=False)
    return jsonify({'success': True, 'message': 'Gift record added'})

@baby_bp.route('/api/baby/gift/<int:id>', methods=['PUT'])
def update_baby_gift(id):
    d = request.get_json()
    execute_query("UPDATE baby_gifts SET person_name=%s, amount=%s, date_bs=%s, date_ad=%s, remarks=%s WHERE id=%s",
        (d['person_name'], float(d['amount']), d.get('date_bs',''), d.get('date_ad', None), d.get('remarks',''), id), fetch=False)
    return jsonify({'success': True, 'message': 'Gift updated'})

@baby_bp.route('/api/baby/gift/<int:id>', methods=['DELETE'])
def delete_baby_gift(id):
    execute_query("DELETE FROM baby_gifts WHERE id=%s", (id,), fetch=False)
    return jsonify({'success': True, 'message': 'Gift deleted'})
