from flask import Blueprint, request, jsonify
from database import execute_query, execute_one

networth_bp = Blueprint('networth', __name__)

@networth_bp.route('/api/networth', methods=['GET'])
def get_networth():
    data = execute_query("SELECT * FROM net_worth ORDER BY date_ad DESC")
    result = []
    for r in data:
        d = dict(r)
        d['date_ad'] = str(d['date_ad'])
        d['created_at'] = str(d['created_at'])
        result.append(d)
    return jsonify(result)

@networth_bp.route('/api/networth', methods=['POST'])
def add_networth():
    d = request.get_json()
    bank = float(d.get('bank_balance', 0))
    cash = float(d.get('cash', 0))
    share = float(d.get('share_value', 0))
    ssf = float(d.get('ssf', 0))
    loan = float(d.get('loan_given', 0))
    prop = float(d.get('property_value', 0))
    nw = bank + cash + share + ssf + loan + prop
    execute_query("""
        INSERT INTO net_worth (date_bs, date_ad, bank_balance, cash, share_value, ssf,
        loan_given, property_value, savings, earned, payout_amount, net_worth, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (d['date_bs'], d['date_ad'], bank, cash, share, ssf, loan, prop,
          float(d.get('savings', 0)), float(d.get('earned', 0)),
          float(d.get('payout_amount', 0)), nw, d.get('remarks', '')), fetch=False)
    return jsonify({'success': True, 'message': 'Net worth saved', 'net_worth': nw})

@networth_bp.route('/api/networth/<int:id>', methods=['PUT'])
def update_networth(id):
    d = request.get_json()
    bank = float(d.get('bank_balance', 0))
    cash = float(d.get('cash', 0))
    share = float(d.get('share_value', 0))
    ssf = float(d.get('ssf', 0))
    loan = float(d.get('loan_given', 0))
    prop = float(d.get('property_value', 0))
    nw = bank + cash + share + ssf + loan + prop
    execute_query("""
        UPDATE net_worth SET date_bs=%s, date_ad=%s, bank_balance=%s, cash=%s, share_value=%s,
        ssf=%s, loan_given=%s, property_value=%s, savings=%s, earned=%s, payout_amount=%s,
        net_worth=%s, remarks=%s WHERE id=%s
    """, (d['date_bs'], d['date_ad'], bank, cash, share, ssf, loan, prop,
          float(d.get('savings', 0)), float(d.get('earned', 0)),
          float(d.get('payout_amount', 0)), nw, d.get('remarks', ''), id), fetch=False)
    return jsonify({'success': True, 'message': 'Net worth updated'})

@networth_bp.route('/api/networth/<int:id>', methods=['DELETE'])
def delete_networth(id):
    execute_query("DELETE FROM net_worth WHERE id=%s", (id,), fetch=False)
    return jsonify({'success': True, 'message': 'Record deleted'})

@networth_bp.route('/api/networth/latest', methods=['GET'])
def latest_networth():
    data = execute_one("SELECT * FROM net_worth ORDER BY date_ad DESC LIMIT 1")
    if data:
        data['date_ad'] = str(data['date_ad'])
        data['created_at'] = str(data['created_at'])
    return jsonify(data or {})
