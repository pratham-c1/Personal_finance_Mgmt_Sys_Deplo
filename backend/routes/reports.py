from flask import Blueprint, request, jsonify, send_file, make_response
from datetime import datetime
from database import execute_query, execute_one

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/api/reports/monthly', methods=['GET'])
def monthly_report():
    year = request.args.get('year')
    month = request.args.get('month')
    params = []
    y_cond = " AND year_bs=%s" if year else ""
    m_cond = " AND month_num=%s" if month else ""
    if year: params.append(year)
    if month: params.append(month)
    
    income = execute_query(f"SELECT category, SUM(amount) as total FROM income WHERE 1=1{y_cond}{m_cond} GROUP BY category", params)
    expense = execute_query(f"SELECT category, SUM(amount) as total FROM expenditure WHERE 1=1{y_cond}{m_cond} GROUP BY category", params)
    total_income = sum(float(r['total']) for r in income)
    total_expense = sum(float(r['total']) for r in expense)
    
    return jsonify({
        'income_breakdown': [dict(r) for r in income],
        'expense_breakdown': [dict(r) for r in expense],
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': total_income - total_expense
    })

@reports_bp.route('/api/reports/export/excel', methods=['GET'])
def export_excel():
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
        
        wb = openpyxl.Workbook()
        
        # Style helpers
        header_fill = PatternFill(start_color="1a1a2e", end_color="1a1a2e", fill_type="solid")
        header_font = Font(color="FFFFFF", bold=True, size=11)
        alt_fill = PatternFill(start_color="f0f4ff", end_color="f0f4ff", fill_type="solid")
        
        def style_header_row(ws, row, cols):
            for col in range(1, cols+1):
                cell = ws.cell(row=row, column=col)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center')
        
        # === INCOME SHEET ===
        ws = wb.active
        ws.title = "Income"
        headers = ['ID', 'Date BS', 'Date AD', 'Year', 'Month', 'Category', 'Amount', 'Remarks']
        ws.append(headers)
        style_header_row(ws, 1, len(headers))
        data = execute_query("SELECT id, date_bs, date_ad, year_bs, month_bs, category, amount, remarks FROM income ORDER BY date_ad DESC")
        for i, r in enumerate(data):
            ws.append([r['id'], r['date_bs'], str(r['date_ad']), r['year_bs'], r['month_bs'], r['category'], float(r['amount']), r.get('remarks','')])
            if i % 2 == 0:
                for col in range(1, len(headers)+1):
                    ws.cell(row=i+2, column=col).fill = alt_fill
        for col in range(1, len(headers)+1):
            ws.column_dimensions[get_column_letter(col)].width = 15
        
        # === EXPENSE SHEET ===
        ws2 = wb.create_sheet("Expenses")
        headers2 = ['ID', 'Date BS', 'Date AD', 'Category', 'Particular', 'Qty', 'Rate', 'Amount', 'Remarks']
        ws2.append(headers2)
        style_header_row(ws2, 1, len(headers2))
        data2 = execute_query("SELECT id, date_bs, date_ad, category, particular, quantity, rate, amount, remarks FROM expenditure ORDER BY date_ad DESC")
        for i, r in enumerate(data2):
            ws2.append([r['id'], r['date_bs'], str(r['date_ad']), r['category'], r.get('particular',''), float(r.get('quantity',1)), float(r.get('rate',0)), float(r['amount']), r.get('remarks','')])
            if i % 2 == 0:
                for col in range(1, len(headers2)+1):
                    ws2.cell(row=i+2, column=col).fill = alt_fill
        for col in range(1, len(headers2)+1):
            ws2.column_dimensions[get_column_letter(col)].width = 15
        
        # === NET WORTH SHEET ===
        ws3 = wb.create_sheet("Net Worth")
        headers3 = ['Date BS', 'Date AD', 'Bank', 'Cash', 'Shares', 'SSF', 'Loan Given', 'Property', 'Net Worth']
        ws3.append(headers3)
        style_header_row(ws3, 1, len(headers3))
        data3 = execute_query("SELECT date_bs, date_ad, bank_balance, cash, share_value, ssf, loan_given, property_value, net_worth FROM net_worth ORDER BY date_ad DESC")
        for i, r in enumerate(data3):
            ws3.append([r['date_bs'], str(r['date_ad']), float(r['bank_balance']), float(r['cash']), float(r['share_value']), float(r['ssf']), float(r['loan_given']), float(r['property_value']), float(r['net_worth'])])
            if i % 2 == 0:
                for col in range(1, len(headers3)+1):
                    ws3.cell(row=i+2, column=col).fill = alt_fill
        for col in range(1, len(headers3)+1):
            ws3.column_dimensions[get_column_letter(col)].width = 15
        
        # === SHARES SHEET ===
        ws4 = wb.create_sheet("Shares")
        headers4 = ['Symbol', 'Name', 'Qty', 'Purchase Price', 'Current Price', 'Investment', 'Current Value', 'P/L']
        ws4.append(headers4)
        style_header_row(ws4, 1, len(headers4))
        data4 = execute_query("SELECT stock_symbol, stock_name, quantity, purchase_price, current_price, investment, current_value, profit_loss FROM shares")
        for i, r in enumerate(data4):
            ws4.append([r['stock_symbol'], r.get('stock_name',''), r['quantity'], float(r['purchase_price']), float(r['current_price']), float(r['investment']), float(r['current_value']), float(r['profit_loss'])])
        for col in range(1, len(headers4)+1):
            ws4.column_dimensions[get_column_letter(col)].width = 18
        
        # === LOANS SHEET ===
        ws5 = wb.create_sheet("Loans")
        headers5 = ['Borrower', 'Principal', 'Rate%', 'Duration(M)', 'Interest', 'Total Payable', 'Status']
        ws5.append(headers5)
        style_header_row(ws5, 1, len(headers5))
        data5 = execute_query("SELECT borrower_name, principal, interest_rate, duration_months, interest_amount, total_payable, status FROM loans")
        for i, r in enumerate(data5):
            ws5.append([r['borrower_name'], float(r['principal']), float(r['interest_rate']), r['duration_months'], float(r['interest_amount']), float(r['total_payable']), r['status']])
        for col in range(1, len(headers5)+1):
            ws5.column_dimensions[get_column_letter(col)].width = 18
        
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        return send_file(buf, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         as_attachment=True, download_name=f'finance_report_{datetime.now().strftime("%Y%m%d")}.xlsx')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/api/reports/export/pdf', methods=['GET'])
def export_pdf():
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm,
                                leftMargin=1.5*cm, rightMargin=1.5*cm)
        styles = getSampleStyleSheet()
        story = []
        
        title_style = ParagraphStyle('title', fontSize=20, fontName='Helvetica-Bold',
                                      textColor=colors.HexColor('#1a1a2e'), spaceAfter=6, alignment=1)
        h2_style = ParagraphStyle('h2', fontSize=13, fontName='Helvetica-Bold',
                                   textColor=colors.HexColor('#16213e'), spaceAfter=4, spaceBefore=14)
        normal_style = ParagraphStyle('normal', fontSize=9, fontName='Helvetica',
                                       textColor=colors.HexColor('#333333'))
        
        header_color = colors.HexColor('#1a1a2e')
        alt_color = colors.HexColor('#f0f4ff')
        
        story.append(Paragraph("Personal Finance Report", title_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#e94560')))
        story.append(Spacer(1, 0.3*cm))
        
        # Summary
        income_sum = execute_one("SELECT COALESCE(SUM(amount),0) as t FROM income")
        expense_sum = execute_one("SELECT COALESCE(SUM(amount),0) as t FROM expenditure")
        nw = execute_one("SELECT net_worth FROM net_worth ORDER BY date_ad DESC LIMIT 1")
        total_income = float(income_sum['t'])
        total_expense = float(expense_sum['t'])
        savings = total_income - total_expense
        net_worth_val = float(nw['net_worth']) if nw else 0
        
        summary_data = [
            ['Metric', 'Amount (NPR)'],
            ['Total Income', f"Rs. {total_income:,.2f}"],
            ['Total Expense', f"Rs. {total_expense:,.2f}"],
            ['Savings', f"Rs. {savings:,.2f}"],
            ['Net Worth', f"Rs. {net_worth_val:,.2f}"],
        ]
        
        story.append(Paragraph("Financial Summary", h2_style))
        t = Table(summary_data, colWidths=[8*cm, 8*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), header_color),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, alt_color]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.5*cm))
        
        # Income breakdown
        income_cat = execute_query("SELECT category, SUM(amount) as total FROM income GROUP BY category ORDER BY total DESC")
        if income_cat:
            story.append(Paragraph("Income Breakdown", h2_style))
            idata = [['Category', 'Amount (NPR)']] + [[r['category'], f"Rs. {float(r['total']):,.2f}"] for r in income_cat]
            it = Table(idata, colWidths=[8*cm, 8*cm])
            it.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), header_color),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 9),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, alt_color]),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
                ('ALIGN', (1,0), (1,-1), 'RIGHT'),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(it)
            story.append(Spacer(1, 0.5*cm))
        
        # Expense breakdown
        expense_cat = execute_query("SELECT category, SUM(amount) as total FROM expenditure GROUP BY category ORDER BY total DESC")
        if expense_cat:
            story.append(Paragraph("Expense Breakdown", h2_style))
            edata = [['Category', 'Amount (NPR)']] + [[r['category'], f"Rs. {float(r['total']):,.2f}"] for r in expense_cat]
            et = Table(edata, colWidths=[8*cm, 8*cm])
            et.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), header_color),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 9),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, alt_color]),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
                ('ALIGN', (1,0), (1,-1), 'RIGHT'),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(et)
        
        # Share portfolio
        shares = execute_query("SELECT stock_symbol, quantity, purchase_price, current_price, investment, current_value, profit_loss FROM shares")
        if shares:
            story.append(Spacer(1, 0.5*cm))
            story.append(Paragraph("Share Portfolio", h2_style))
            sdata = [['Symbol', 'Qty', 'Buy Price', 'Curr Price', 'Investment', 'Curr Value', 'P/L']]
            for r in shares:
                pl = float(r['profit_loss'])
                sdata.append([r['stock_symbol'], r['quantity'], f"Rs.{float(r['purchase_price']):,.0f}", 
                              f"Rs.{float(r['current_price']):,.0f}", f"Rs.{float(r['investment']):,.0f}",
                              f"Rs.{float(r['current_value']):,.0f}", f"Rs.{pl:,.0f}"])
            st = Table(sdata, colWidths=[2.3*cm]*7)
            st.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), header_color),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, alt_color]),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
                ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(st)
        
        doc.build(story)
        buf.seek(0)
        return send_file(buf, mimetype='application/pdf', as_attachment=True,
                         download_name=f'finance_report_{datetime.now().strftime("%Y%m%d")}.pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
