from flask import Blueprint, request, jsonify, session
from database import execute_query, execute_one

bike_bp = Blueprint('bike', __name__)

def uid(): return session.get('user_id')

@bike_bp.route('/api/bike', methods=['GET'])
def get_bikes():
    data = execute_query("SELECT * FROM bikes WHERE user_id=%s ORDER BY created_at DESC", (uid(),))
    result = []
    for r in data:
        d = dict(r)
        if d.get('purchase_date'): d['purchase_date'] = str(d['purchase_date'])
        d['created_at'] = str(d['created_at'])
        result.append(d)
    return jsonify(result)

@bike_bp.route('/api/bike', methods=['POST'])
def add_bike():
    d = request.get_json()
    execute_query(
        "INSERT INTO bikes (user_id, bike_name, bike_number, purchase_price, purchase_date) VALUES (%s,%s,%s,%s,%s)",
        (uid(), d['bike_name'], d.get('bike_number',''), float(d.get('purchase_price',0)), d.get('purchase_date', None)), fetch=False)
    return jsonify({'success': True, 'message': 'Bike added'})

@bike_bp.route('/api/bike/<int:id>', methods=['PUT'])
def update_bike(id):
    d = request.get_json()
    execute_query(
        "UPDATE bikes SET bike_name=%s, bike_number=%s, purchase_price=%s, purchase_date=%s WHERE id=%s AND user_id=%s",
        (d['bike_name'], d.get('bike_number',''), float(d.get('purchase_price',0)), d.get('purchase_date',None), id, uid()), fetch=False)
    return jsonify({'success': True, 'message': 'Bike updated'})

@bike_bp.route('/api/bike/<int:id>', methods=['DELETE'])
def delete_bike(id):
    execute_query("DELETE FROM bikes WHERE id=%s AND user_id=%s", (id, uid()), fetch=False)
    return jsonify({'success': True, 'message': 'Bike deleted'})

@bike_bp.route('/api/bike/expense', methods=['GET'])
def get_bike_expense():
    bike_id = request.args.get('bike_id')
    q = "SELECT * FROM bike_expenditure WHERE user_id=%s"
    p = [uid()]
    if bike_id: q += " AND bike_id=%s"; p.append(bike_id)
    q += " ORDER BY date_ad DESC"
    data = execute_query(q, p)
    result = []
    for r in data:
        d = dict(r)
        if d.get('date_ad'): d['date_ad'] = str(d['date_ad'])
        d['created_at'] = str(d['created_at'])
        result.append(d)
    return jsonify(result)

@bike_bp.route('/api/bike/expense', methods=['POST'])
def add_bike_expense():
    d = request.get_json()
    qty    = float(d.get('quantity', 1))
    rate   = float(d.get('rate', 0))
    amount = qty * rate
    execute_query("""
        INSERT INTO bike_expenditure (user_id, bike_id, bike_name, bike_number, date_bs, date_ad,
        year_bs, month_bs, month_num, particular, quantity, rate, amount, remarks)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (uid(), d.get('bike_id'), d.get('bike_name',''), d.get('bike_number',''),
          d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          d.get('particular',''), qty, rate, amount, d.get('remarks','')), fetch=False)
    return jsonify({'success': True, 'message': 'Bike expense added'})

@bike_bp.route('/api/bike/expense/<int:id>', methods=['PUT'])
def update_bike_expense(id):
    d = request.get_json()
    qty    = float(d.get('quantity', 1))
    rate   = float(d.get('rate', 0))
    amount = qty * rate
    execute_query("""
        UPDATE bike_expenditure SET bike_id=%s, bike_name=%s, bike_number=%s, date_bs=%s, date_ad=%s,
        year_bs=%s, month_bs=%s, month_num=%s, particular=%s, quantity=%s, rate=%s, amount=%s, remarks=%s
        WHERE id=%s AND user_id=%s
    """, (d.get('bike_id'), d.get('bike_name',''), d.get('bike_number',''),
          d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          d.get('particular',''), qty, rate, amount, d.get('remarks',''), id, uid()), fetch=False)
    return jsonify({'success': True, 'message': 'Bike expense updated'})

@bike_bp.route('/api/bike/expense/<int:id>', methods=['DELETE'])
def delete_bike_expense(id):
    execute_query("DELETE FROM bike_expenditure WHERE id=%s AND user_id=%s", (id, uid()), fetch=False)
    return jsonify({'success': True, 'message': 'Bike expense deleted'})
