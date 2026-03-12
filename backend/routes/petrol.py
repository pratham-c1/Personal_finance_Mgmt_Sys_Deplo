from flask import Blueprint, request, jsonify
from database import execute_query, execute_one

petrol_bp = Blueprint('petrol', __name__)

@petrol_bp.route('/api/petrol', methods=['GET'])
def get_petrol():
    bike_id = request.args.get('bike_id')
    query = "SELECT * FROM petrol WHERE 1=1"
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

@petrol_bp.route('/api/petrol', methods=['POST'])
def add_petrol():
    d = request.get_json()
    amount_paid = float(d.get('amount_paid', 0))
    price_per_liter = float(d.get('price_per_liter', 1))
    liters = round(amount_paid / price_per_liter, 3) if price_per_liter else 0
    current_km = int(d.get('current_km', 0))
    bike_id = d.get('bike_id')
    # Get previous KM
    prev = None
    if bike_id:
        prev = execute_one("SELECT current_km FROM petrol WHERE bike_id=%s ORDER BY date_ad DESC, id DESC LIMIT 1", (bike_id,))
    previous_km = int(prev['current_km']) if prev else 0
    distance = max(0, current_km - previous_km)
    mileage = round(distance / liters, 2) if liters > 0 else 0
    execute_query("""
        INSERT INTO petrol (bike_id, bike_name, bike_number, date_bs, date_ad, year_bs, month_bs, month_num,
        amount_paid, price_per_liter, liters, current_km, previous_km, distance, mileage, remarks)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (bike_id, d.get('bike_name',''), d.get('bike_number',''),
          d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          amount_paid, price_per_liter, liters, current_km, previous_km, distance, mileage, d.get('remarks','')), fetch=False)
    return jsonify({'success': True, 'message': 'Petrol record added', 'liters': liters, 'mileage': mileage})

@petrol_bp.route('/api/petrol/<int:id>', methods=['PUT'])
def update_petrol(id):
    d = request.get_json()
    amount_paid = float(d.get('amount_paid', 0))
    price_per_liter = float(d.get('price_per_liter', 1))
    liters = round(amount_paid / price_per_liter, 3) if price_per_liter else 0
    current_km = int(d.get('current_km', 0))
    previous_km = int(d.get('previous_km', 0))
    distance = max(0, current_km - previous_km)
    mileage = round(distance / liters, 2) if liters > 0 else 0
    execute_query("""
        UPDATE petrol SET bike_id=%s, bike_name=%s, bike_number=%s, date_bs=%s, date_ad=%s,
        year_bs=%s, month_bs=%s, month_num=%s, amount_paid=%s, price_per_liter=%s, liters=%s,
        current_km=%s, previous_km=%s, distance=%s, mileage=%s, remarks=%s WHERE id=%s
    """, (d.get('bike_id'), d.get('bike_name',''), d.get('bike_number',''),
          d['date_bs'], d['date_ad'], d['year_bs'], d['month_bs'], d['month_num'],
          amount_paid, price_per_liter, liters, current_km, previous_km, distance, mileage, d.get('remarks',''), id), fetch=False)
    return jsonify({'success': True, 'message': 'Petrol record updated'})

@petrol_bp.route('/api/petrol/<int:id>', methods=['DELETE'])
def delete_petrol(id):
    execute_query("DELETE FROM petrol WHERE id=%s", (id,), fetch=False)
    return jsonify({'success': True, 'message': 'Petrol record deleted'})
