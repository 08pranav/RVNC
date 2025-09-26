"""
Real vs. Nominal Return Calculator - Flask Web Application
Beautiful UI for calculating inflation-adjusted returns with country-wise inflation and investment types
"""

from flask import Flask, render_template, request, jsonify
import json
from calculator import (
    calculate_real_return,
    format_percentage,
    parse_percentage_input,
    validate_inputs,
    calculate_purchasing_power,
    format_currency,
    calculate_investment_scenarios,
    parse_currency_input,
    calculate_detailed_projections,
    calculate_sip_projections
)
from data_provider import (
    get_country_inflation_rate,
    get_all_countries,
    get_investment_types,
    get_investment_type_return,
    get_investment_categories
)

app = Flask(__name__)

@app.route('/')
def index():
    """Main page with country and investment type data"""
    countries = get_all_countries()
    investment_categories = get_investment_categories()
    return render_template('index.html', countries=countries, investment_categories=investment_categories)

@app.route('/api/countries')
def api_countries():
    """Get all supported countries"""
    return jsonify(get_all_countries())

@app.route('/api/inflation/<country_code>')
def api_inflation(country_code):
    """Get inflation rate for a specific country"""
    inflation_data = get_country_inflation_rate(country_code.upper())
    return jsonify(inflation_data)

@app.route('/api/investment-types')
def api_investment_types():
    """Get all investment types"""
    return jsonify(get_investment_categories())

@app.route('/api/detailed-projections', methods=['POST'])
def api_detailed_projections():
    """Get detailed future value projections"""
    try:
        data = request.get_json()
        
        initial_amount = parse_currency_input(str(data.get('amount', '100000')))
        nominal_return = parse_percentage_input(str(data.get('nominal_return', '8')))
        inflation_rate = parse_percentage_input(str(data.get('inflation_rate', '3')))
        years_list = data.get('years', [1, 2, 3, 5, 7, 10, 15, 20, 25, 30])
        include_monthly = data.get('include_monthly', True)
        
        projections = calculate_detailed_projections(
            initial_amount, nominal_return, inflation_rate, 
            years_list, include_monthly
        )
        
        return jsonify({
            'success': True,
            'projections': projections
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Projection calculation error: {str(e)}'
        })

@app.route('/api/sip-projections', methods=['POST'])
def api_sip_projections():
    """Get SIP (Systematic Investment Plan) projections"""
    try:
        data = request.get_json()
        
        monthly_amount = parse_currency_input(str(data.get('monthly_amount', '10000')))
        nominal_return = parse_percentage_input(str(data.get('nominal_return', '12')))
        inflation_rate = parse_percentage_input(str(data.get('inflation_rate', '4')))
        years_list = data.get('years', [1, 2, 3, 5, 7, 10, 15, 20, 25, 30])
        
        projections = calculate_sip_projections(
            monthly_amount, nominal_return, inflation_rate, years_list
        )
        
        return jsonify({
            'success': True,
            'sip_projections': projections
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'SIP projection calculation error: {str(e)}'
        })

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate real return via API with enhanced features"""
    try:
        data = request.get_json()
        
        # Handle country selection and inflation rate
        country_code = data.get('country', 'IN')
        use_country_inflation = data.get('use_country_inflation', False)
        
        if use_country_inflation:
            country_inflation_data = get_country_inflation_rate(country_code)
            inflation_rate = country_inflation_data['rate'] / 100  # Convert to decimal
            inflation_source = country_inflation_data
        else:
            inflation_rate = parse_percentage_input(str(data.get('inflation_rate', 0)))
            inflation_source = {'source': 'manual', 'rate': inflation_rate * 100}
        
        # Handle investment type selection
        investment_type = data.get('investment_type', None)
        use_investment_type = data.get('use_investment_type', False)
        
        if use_investment_type and investment_type:
            nominal_return = get_investment_type_return(investment_type)
            investment_info = get_investment_types().get(investment_type, {})
        else:
            nominal_return = parse_percentage_input(str(data.get('nominal_return', 0)))
            investment_info = {'source': 'manual', 'name': 'Custom Return'}
        
        # Parse custom investment amount
        custom_amount_str = str(data.get('investment_amount', '100000'))
        try:
            if custom_amount_str.strip() == '' or custom_amount_str == 'None':
                investment_amount = 100000  # Default ₹1,00,000 (1 Lakh)
            else:
                investment_amount = parse_currency_input(custom_amount_str)
        except ValueError:
            investment_amount = 100000  # Default on error
        
        # Validate inputs
        is_valid, warning = validate_inputs(nominal_return, inflation_rate)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': warning
            })
        
        # Calculate real return
        real_return = calculate_real_return(nominal_return, inflation_rate)
        
        # Calculate detailed projections
        detailed_projections = calculate_detailed_projections(
            investment_amount, nominal_return, inflation_rate, 
            [1, 2, 3, 5, 7, 10, 15, 20, 25, 30], include_monthly=True
        )
        
        # Calculate SIP projections (assuming monthly SIP of 1/12th of lump sum)
        monthly_sip_amount = investment_amount / 120  # Assume 10-year SIP equivalent
        sip_projections = calculate_sip_projections(
            monthly_sip_amount, nominal_return, inflation_rate,
            [1, 2, 3, 5, 7, 10, 15, 20, 25, 30]
        )
        
        # Legacy format for backward compatibility
        purchasing_power_data = []
        for proj in detailed_projections['yearly_projections'][:7]:  # First 7 years
            purchasing_power_data.append({
                'years': proj['years'],
                'nominal_value': round(proj['nominal_value'], 2),
                'real_value': round(proj['real_value'], 2),
                'inflation_impact': round(proj['inflation_impact'], 2),
                'nominal_formatted': proj['formatted']['nominal_value'],
                'real_formatted': proj['formatted']['real_value'],
                'inflation_formatted': proj['formatted']['inflation_impact']
            })
        
        # Determine investment assessment
        if real_return > 0.03:
            assessment = {
                'level': 'excellent',
                'message': 'Excellent! Your investment significantly beats inflation.',
                'icon': '🎉'
            }
        elif real_return > 0:
            assessment = {
                'level': 'good',
                'message': 'Good! Your investment beats inflation.',
                'icon': '✅'
            }
        elif real_return == 0:
            assessment = {
                'level': 'neutral',
                'message': 'Your investment exactly matches inflation.',
                'icon': '⚠️'
            }
        else:
            assessment = {
                'level': 'poor',
                'message': 'Warning! Your investment loses to inflation.',
                'icon': '❌'
            }
        
        return jsonify({
            'success': True,
            'results': {
                'nominal_return': format_percentage(nominal_return, 2),
                'inflation_rate': format_percentage(inflation_rate, 2),
                'real_return': format_percentage(real_return, 2),
                'real_return_decimal': real_return,
                'calculation_steps': {
                    'step1': f"(1 + {nominal_return:.4f}) = {1 + nominal_return:.4f}",
                    'step2': f"(1 + {inflation_rate:.4f}) = {1 + inflation_rate:.4f}",
                    'step3': f"{1 + nominal_return:.4f} ÷ {1 + inflation_rate:.4f} = {(1 + nominal_return) / (1 + inflation_rate):.6f}",
                    'step4': f"{(1 + nominal_return) / (1 + inflation_rate):.6f} - 1 = {real_return:.6f}"
                },
                'purchasing_power_data': purchasing_power_data,  # Legacy compatibility
                'detailed_projections': detailed_projections,    # NEW: Detailed year-by-year projections
                'sip_projections': sip_projections,             # NEW: SIP calculations
                'assessment': assessment,
                'investment_amount': investment_amount,
                'investment_amount_formatted': format_currency(investment_amount),
                'inflation_source': inflation_source,
                'investment_info': investment_info,
                'country_code': country_code
            },
            'warning': warning
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Calculation error: {str(e)}'
        })

@app.route('/examples')
def examples():
    """Get example calculations"""
    examples = [
        {
            'name': 'Stock Market Investment',
            'description': 'Typical stock market return vs. normal inflation',
            'nominal': 8,
            'inflation': 3,
            'scenario': 'bull_market'
        },
        {
            'name': 'Government Bonds',
            'description': 'Conservative bond investment',
            'nominal': 5,
            'inflation': 2,
            'scenario': 'conservative'
        },
        {
            'name': 'High Growth Stock',
            'description': 'Growth stock in high inflation period',
            'nominal': 12,
            'inflation': 6,
            'scenario': 'high_growth'
        },
        {
            'name': 'Savings Account',
            'description': 'Low-yield savings during inflation',
            'nominal': 1,
            'inflation': 4,
            'scenario': 'savings_loss'
        },
        {
            'name': 'Real Estate',
            'description': 'Real estate investment return',
            'nominal': 7,
            'inflation': 3.5,
            'scenario': 'real_estate'
        }
    ]
    
    # Calculate real returns for each example
    for example in examples:
        nominal = example['nominal'] / 100
        inflation = example['inflation'] / 100
        real = calculate_real_return(nominal, inflation)
        example['real_return'] = format_percentage(real, 2)
        example['real_return_decimal'] = real
    
    return jsonify(examples)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)