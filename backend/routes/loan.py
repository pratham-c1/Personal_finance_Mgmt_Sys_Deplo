from flask import Blueprint, request, jsonify
from database import execute_query, execute_one

loan_bp = Blueprint('loan', __name__)

@loan_bp.route('/api/loan', methods=['GET'])
def get_loans():
    status = request.args.get('status')
    query = "SELECT * FROM loans WHERE 1=1"
    params = []
    if status: query += " AND status=%s"; params.append(status)
    query += " ORDER BY created_at DESC"
    data = execute_query(query, params)
    result = []
    for r in data:
        d = dict(r)
        if d.get('loan_date_ad'): d['loan_date_ad'] = str(d['loan_date_ad'])
        d['created_at'] = str(d['created_at'])
        result.append(d)
    return jsonify(result)

@loan_bp.route('/api/loan', methods=['POST'])
def add_loan():
    d = request.get_json()
    principal = float(d.get('principal', 0))
    rate = float(d.get('interest_rate', 0))
    months = int(d.get('duration_months', 0))
    interest = (principal * rate * months) / (12 * 100) if months and rate else 0
    total = principal + interest
    execute_query("""
        INSERT INTO loans (borrower_name, principal, interest_rate, loan_date_bs, loan_date_ad,
        duration_months, interest_amount, total_payable, status, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (d['borrower_name'], principal, rate, d.get('loan_date_bs',''),
          d.get('loan_date_ad', None), months, interest, total,
          d.get('status', 'active'), d.get('remarks', '')), fetch=False)
    return jsonify({'success': True, 'message': 'Loan added'})

@loan_bp.route('/api/loan/<int:id>', methods=['PUT'])
def update_loan(id):
    d = request.get_json()
    principal = float(d.get('principal', 0))
    rate = float(d.get('interest_rate', 0))
    months = int(d.get('duration_months', 0))
    interest = (principal * rate * months) / (12 * 100) if months and rate else 0
    total = principal + interest
    execute_query("""
        UPDATE loans SET borrower_name=%s, principal=%s, interest_rate=%s, loan_date_bs=%s,
        loan_date_ad=%s, duration_months=%s, interest_amount=%s, total_payable=%s,
        status=%s, remarks=%s WHERE id=%s
    """, (d['borrower_name'], principal, rate, d.get('loan_date_bs',''),
          d.get('loan_date_ad', None), months, interest, total,
          d.get('status','active'), d.get('remarks',''), id), fetch=False)
    return jsonify({'success': True, 'message': 'Loan updated'})

@loan_bp.route('/api/loan/<int:id>', methods=['DELETE'])
def delete_loan(id):
    execute_query("DELETE FROM loans WHERE id=%s", (id,), fetch=False)
    return jsonify({'success': True, 'message': 'Loan deleted'})
