from flask import Blueprint, request, jsonify
from database import execute_query, execute_one

bike_bp = Blueprint('bike', __name__)

@bike_bp.route('/api/bike', methods=['GET'])
def get_bikes():
    data = execute_query("SELECT * FROM bikes ORDER BY created_at DESC")
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
    execute_query("INSERT INTO bikes (bike_name, bike_number, purchase_price, purchase_date) VALUES (%s,%s,%s,%s)",
        (d['bike_name'], d.get('bike_number',''), float(d.get('purchase_price',0)), d.get('purchase_date', None)), fetch=False)
    return jsonify({'success': True, 'message': 'Bike added'})

@bike_bp.route('/api/bike/<int:id>', methods=['PUT'])
def update_bike(id):
    d = request.get_json()
    execute_query("UPDATE bikes SET bike_name=%s, bike_number=%s, purchase_price=%s, purchase_date=%s WHERE id=%s",
        (d['bike_name'], d.get('bike_number',''), float(d.get('purchase_price',0)), d.get('purchase_date',None), id), fetch=False)
    return jsonify({'success': True, 'message': 'Bike updated'})

@bike_bp.route('/api/bike/<int:id>', methods=['DELETE'])
def delete_bike(id):
    execute_query("DELETE FROM bikes WHERE id=%s", (id,), fetch=False)
    return jsonify({'success': True, 'message': 'Bike deleted'})

@bike_bp.route('/api/bike/expense', methods=['GET'])
def get_bike_expense():
    bike_id = request.args.get('bike_id')
    query = "SELECT * FROM bike_expenditure WHERE 1=1"
    params = []
    if bike_id: query += " AND bike_id=%s"; params.append(bike_id)
    query += " ORDER BY date_ad DESC"
    data = execute_query(query, params)
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
    qty = float(d.get('quantity', 1))
    rate = float(d.get('rate', 0))
    amount = qty * rate
    execute_query("""
        INSERT INTO bike_expenditure (bike_id, bike_name, bike_number, date_bs, date_ad,
        year_bs, month_bs, month_num, particular, quantity, rate, amount, remarks)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (d.get('bike_id'), d.get('bike_name',''), d.get('bike_number',''),
          d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          d.get('particular',''), qty, rate, amount, d.get('remarks','')), fetch=False)
    return jsonify({'success': True, 'message': 'Bike expense added'})

@bike_bp.route('/api/bike/expense/<int:id>', methods=['PUT'])
def update_bike_expense(id):
    d = request.get_json()
    qty = float(d.get('quantity', 1))
    rate = float(d.get('rate', 0))
    amount = qty * rate
    execute_query("""
        UPDATE bike_expenditure SET bike_id=%s, bike_name=%s, bike_number=%s, date_bs=%s, date_ad=%s,
        year_bs=%s, month_bs=%s, month_num=%s, particular=%s, quantity=%s, rate=%s, amount=%s, remarks=%s WHERE id=%s
    """, (d.get('bike_id'), d.get('bike_name',''), d.get('bike_number',''),
          d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          d.get('particular',''), qty, rate, amount, d.get('remarks',''), id), fetch=False)
    return jsonify({'success': True, 'message': 'Bike expense updated'})

@bike_bp.route('/api/bike/expense/<int:id>', methods=['DELETE'])
def delete_bike_expense(id):
    execute_query("DELETE FROM bike_expenditure WHERE id=%s", (id,), fetch=False)
    return jsonify({'success': True, 'message': 'Bike expense deleted'})
