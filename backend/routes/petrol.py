from flask import Blueprint, request, jsonify, session
from database import execute_query, execute_one

petrol_bp = Blueprint('petrol', __name__)

def uid(): return session.get('user_id')

def get_prev_entry(bike_id, date_ad, exclude_id=None):
    """Most recent entry for this bike STRICTLY before date_ad."""
    if exclude_id:
        return execute_one(
            """SELECT current_km, remaining_fuel FROM petrol
               WHERE bike_id=%s AND user_id=%s AND date_ad < %s AND id != %s
               ORDER BY date_ad DESC, id DESC LIMIT 1""",
            (bike_id, uid(), date_ad, exclude_id)
        )
    return execute_one(
        """SELECT current_km, remaining_fuel FROM petrol
           WHERE bike_id=%s AND user_id=%s AND date_ad < %s
           ORDER BY date_ad DESC, id DESC LIMIT 1""",
        (bike_id, uid(), date_ad)
    )

@petrol_bp.route('/api/petrol', methods=['GET'])
def get_petrol():
    bike_id = request.args.get('bike_id')
    q = "SELECT * FROM petrol WHERE user_id=%s"
    p = [uid()]
    if bike_id: q += " AND bike_id=%s"; p.append(bike_id)
    q += " ORDER BY date_ad DESC, id DESC"
    data = execute_query(q, p)
    result = []
    for r in data:
        d = dict(r)
        if d.get('date_ad'):    d['date_ad']    = str(d['date_ad'])
        if d.get('created_at'): d['created_at'] = str(d['created_at'])
        result.append(d)
    return jsonify(result)

@petrol_bp.route('/api/petrol/prev-km', methods=['GET'])
def get_prev_km():
    bike_id    = request.args.get('bike_id')
    date_ad    = request.args.get('date_ad')
    exclude_id = request.args.get('exclude_id')
    if not bike_id or not date_ad:
        return jsonify({'previous_km': 0, 'remaining_fuel': 0})
    prev = get_prev_entry(bike_id, date_ad, exclude_id)
    if prev:
        return jsonify({'previous_km': int(prev['current_km'] or 0),
                        'remaining_fuel': float(prev['remaining_fuel'] or 0)})
    return jsonify({'previous_km': 0, 'remaining_fuel': 0})

@petrol_bp.route('/api/petrol', methods=['POST'])
def add_petrol():
    d               = request.get_json()
    amount_paid     = float(d.get('amount_paid', 0))
    price_per_liter = float(d.get('price_per_liter', 1))
    current_km      = int(d.get('current_km', 0))
    remaining_fuel  = float(d.get('remaining_fuel', 0))
    bike_id         = d.get('bike_id')
    date_ad         = d.get('date_ad')

    liters_filled = round(amount_paid / price_per_liter, 3) if price_per_liter else 0
    total_fuel    = round(liters_filled + remaining_fuel, 3)

    prev        = get_prev_entry(bike_id, date_ad) if bike_id else None
    previous_km = int(prev['current_km'] or 0) if prev else 0
    distance    = max(0, current_km - previous_km)
    mileage     = round(distance / total_fuel, 2) if total_fuel > 0 else 0

    execute_query("""
        INSERT INTO petrol (user_id,bike_id,bike_name,bike_number,date_bs,date_ad,year_bs,month_bs,month_num,
        amount_paid,price_per_liter,liters,remaining_fuel,current_km,previous_km,distance,mileage,remarks)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (uid(),bike_id,d.get('bike_name',''),d.get('bike_number',''),
          d.get('date_bs',''),date_ad,d.get('year_bs'),d.get('month_bs',''),d.get('month_num'),
          amount_paid,price_per_liter,liters_filled,remaining_fuel,
          current_km,previous_km,distance,mileage,d.get('remarks','')), fetch=False)

    return jsonify({'success':True,'message':'Petrol record added',
                    'liters_filled':liters_filled,'remaining_fuel':remaining_fuel,
                    'total_fuel':total_fuel,'previous_km':previous_km,
                    'distance':distance,'mileage':mileage})

@petrol_bp.route('/api/petrol/<int:id>', methods=['PUT'])
def update_petrol(id):
    d               = request.get_json()
    amount_paid     = float(d.get('amount_paid', 0))
    price_per_liter = float(d.get('price_per_liter', 1))
    current_km      = int(d.get('current_km', 0))
    remaining_fuel  = float(d.get('remaining_fuel', 0))
    bike_id         = d.get('bike_id')
    date_ad         = d.get('date_ad')

    liters_filled = round(amount_paid / price_per_liter, 3) if price_per_liter else 0
    total_fuel    = round(liters_filled + remaining_fuel, 3)

    prev        = get_prev_entry(bike_id, date_ad, exclude_id=id) if bike_id else None
    previous_km = int(prev['current_km'] or 0) if prev else 0
    distance    = max(0, current_km - previous_km)
    mileage     = round(distance / total_fuel, 2) if total_fuel > 0 else 0

    execute_query("""
        UPDATE petrol SET bike_id=%s,bike_name=%s,bike_number=%s,date_bs=%s,date_ad=%s,
        year_bs=%s,month_bs=%s,month_num=%s,amount_paid=%s,price_per_liter=%s,liters=%s,
        remaining_fuel=%s,current_km=%s,previous_km=%s,distance=%s,mileage=%s,remarks=%s
        WHERE id=%s AND user_id=%s
    """, (bike_id,d.get('bike_name',''),d.get('bike_number',''),
          d.get('date_bs',''),date_ad,d.get('year_bs'),d.get('month_bs',''),d.get('month_num'),
          amount_paid,price_per_liter,liters_filled,remaining_fuel,
          current_km,previous_km,distance,mileage,d.get('remarks',''),id,uid()), fetch=False)

    return jsonify({'success':True,'message':'Petrol record updated',
                    'liters_filled':liters_filled,'remaining_fuel':remaining_fuel,
                    'total_fuel':total_fuel,'previous_km':previous_km,
                    'distance':distance,'mileage':mileage})

@petrol_bp.route('/api/petrol/<int:id>', methods=['DELETE'])
def delete_petrol(id):
    execute_query("DELETE FROM petrol WHERE id=%s AND user_id=%s", (id, uid()), fetch=False)
    return jsonify({'success': True, 'message': 'Petrol record deleted'})
