"""
Real vs. Nominal Return Calculator - Flask Web Application
Beautiful UI for calculating inflation-adjusted returns
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
    parse_currency_input
)

app = Flask(__name__)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate real return via API"""
    try:
        data = request.get_json()
        
        # Parse inputs
        nominal_return = parse_percentage_input(str(data.get('nominal_return', 0)))
        inflation_rate = parse_percentage_input(str(data.get('inflation_rate', 0)))
        
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
        
        # Calculate investment scenarios with custom amount
        scenarios_data = calculate_investment_scenarios(
            investment_amount, nominal_return, inflation_rate, 
            [1, 5, 10, 15, 20, 25, 30]
        )
        
        # Format purchasing power data for JSON response
        purchasing_power_data = []
        for scenario in scenarios_data['scenarios']:
            purchasing_power_data.append({
                'years': scenario['years'],
                'nominal_value': round(scenario['nominal_value'], 2),
                'real_value': round(scenario['real_value'], 2),
                'inflation_impact': round(scenario['inflation_impact'], 2),
                'nominal_formatted': scenario['nominal_formatted'],
                'real_formatted': scenario['real_formatted'],
                'inflation_formatted': scenario['inflation_formatted']
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
                'purchasing_power_data': purchasing_power_data,
                'assessment': assessment,
                'investment_amount': investment_amount,
                'investment_amount_formatted': format_currency(investment_amount)
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