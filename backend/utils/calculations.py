"""Financial calculation utilities"""

def calculate_loan_interest(principal, rate, months):
    """Simple interest calculation"""
    interest = (principal * rate * months) / (12 * 100)
    total = principal + interest
    return round(interest, 2), round(total, 2)

def calculate_net_worth(bank_balance, cash, share_value, ssf, loan_given, property_value):
    return round(bank_balance + cash + share_value + ssf + loan_given + property_value, 2)

def calculate_savings(total_income, total_expense):
    return round(total_income - total_expense, 2)

def calculate_mileage(distance, liters):
    if liters > 0:
        return round(distance / liters, 2)
    return 0

def calculate_share_pl(qty, purchase_price, current_price):
    investment = qty * purchase_price
    current_value = qty * current_price
    profit_loss = current_value - investment
    return round(investment, 2), round(current_value, 2), round(profit_loss, 2)
