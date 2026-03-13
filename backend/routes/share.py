from flask import Blueprint, request, jsonify, session
from database import execute_query, execute_one
from utils.nepse_api import get_stock_list_for_dropdown

share_bp = Blueprint('share', __name__)

def uid(): return session.get('user_id')

@share_bp.route('/api/share', methods=['GET'])
def get_shares():
    data = execute_query("SELECT * FROM shares WHERE user_id=%s ORDER BY created_at DESC", (uid(),))
    result = []
    for r in data:
        d = dict(r)
        if d.get('purchase_date_ad'): d['purchase_date_ad'] = str(d['purchase_date_ad'])
        d['created_at']  = str(d['created_at'])
        d['updated_at']  = str(d['updated_at'])
        result.append(d)
    return jsonify(result)

@share_bp.route('/api/share', methods=['POST'])
def add_share():
    d = request.get_json()
    qty            = int(d.get('quantity', 0))
    purchase_price = float(d.get('purchase_price', 0))
    current_price  = float(d.get('current_price', purchase_price))
    investment     = qty * purchase_price
    current_value  = qty * current_price
    profit_loss    = current_value - investment
    execute_query("""
        INSERT INTO shares (user_id, stock_symbol, stock_name, quantity, purchase_price,
        current_price, investment, current_value, profit_loss, purchase_date_bs, purchase_date_ad, remarks)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (uid(), d['stock_symbol'], d.get('stock_name',''), qty, purchase_price, current_price,
          investment, current_value, profit_loss,
          d.get('purchase_date_bs',''), d.get('purchase_date_ad', None), d.get('remarks','')), fetch=False)
    return jsonify({'success': True, 'message': 'Share added'})

@share_bp.route('/api/share/<int:id>', methods=['PUT'])
def update_share(id):
    d = request.get_json()
    qty            = int(d.get('quantity', 0))
    purchase_price = float(d.get('purchase_price', 0))
    current_price  = float(d.get('current_price', purchase_price))
    investment     = qty * purchase_price
    current_value  = qty * current_price
    profit_loss    = current_value - investment
    execute_query("""
        UPDATE shares SET stock_symbol=%s, stock_name=%s, quantity=%s, purchase_price=%s,
        current_price=%s, investment=%s, current_value=%s, profit_loss=%s,
        purchase_date_bs=%s, purchase_date_ad=%s, remarks=%s WHERE id=%s AND user_id=%s
    """, (d['stock_symbol'], d.get('stock_name',''), qty, purchase_price, current_price,
          investment, current_value, profit_loss,
          d.get('purchase_date_bs',''), d.get('purchase_date_ad', None),
          d.get('remarks',''), id, uid()), fetch=False)
    return jsonify({'success': True, 'message': 'Share updated'})

@share_bp.route('/api/share/<int:id>', methods=['DELETE'])
def delete_share(id):
    execute_query("DELETE FROM shares WHERE id=%s AND user_id=%s", (id, uid()), fetch=False)
    return jsonify({'success': True, 'message': 'Share deleted'})

@share_bp.route('/api/share/stocks', methods=['GET'])
def get_stocks():
    return jsonify(get_stock_list_for_dropdown())

@share_bp.route('/api/share/summary', methods=['GET'])
def share_summary():
    data = execute_one("""
        SELECT COALESCE(SUM(investment),0) as total_investment,
               COALESCE(SUM(current_value),0) as total_current_value,
               COALESCE(SUM(profit_loss),0) as total_pl FROM shares WHERE user_id=%s
    """, (uid(),))
    return jsonify({k: float(v) for k, v in data.items()})
