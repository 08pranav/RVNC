"""
Real vs. Nominal Return Calculator - Core Module
Financial Concept: Inflation-adjusted returns calculation
"""

def calculate_real_return(nominal_return, inflation_rate):
    """
    Calculate the real rate of return using the formula:
    Real Return = ((1 + nominal) / (1 + inflation)) - 1
    
    Args:
        nominal_return (float): The nominal return rate (as decimal, e.g., 0.08 for 8%)
        inflation_rate (float): The inflation rate (as decimal, e.g., 0.03 for 3%)
    
    Returns:
        float: The real return rate (as decimal)
    """
    try:
        real_return = ((1 + nominal_return) / (1 + inflation_rate)) - 1
        return real_return
    except ZeroDivisionError:
        raise ValueError("Inflation rate cannot be -100% (which would make 1 + inflation = 0)")
    except Exception as e:
        raise ValueError(f"Error in calculation: {str(e)}")

def format_percentage(decimal_value, decimal_places=4):
    """
    Convert decimal to percentage format for display
    
    Args:
        decimal_value (float): Decimal value to convert
        decimal_places (int): Number of decimal places to show
    
    Returns:
        str: Formatted percentage string
    """
    return f"{decimal_value * 100:.{decimal_places}f}%"

def parse_percentage_input(percentage_str):
    """
    Parse percentage input (handles both decimal and percentage formats)
    
    Args:
        percentage_str (str): Input string (e.g., "8" or "8%" or "0.08")
    
    Returns:
        float: Decimal representation
    """
    percentage_str = percentage_str.strip()
    
    if percentage_str.endswith('%'):
        # Remove % and convert to decimal
        return float(percentage_str[:-1]) / 100
    else:
        value = float(percentage_str)
        # If value is greater than 1, assume it's a percentage
        if value > 1:
            return value / 100
        else:
            return value

def validate_inputs(nominal_return, inflation_rate):
    """
    Validate input values for reasonableness
    
    Args:
        nominal_return (float): Nominal return rate
        inflation_rate (float): Inflation rate
    
    Returns:
        tuple: (is_valid, warning_message)
    """
    warnings = []
    
    # Check for extreme values
    if abs(nominal_return) > 10:  # More than 1000%
        warnings.append(f"Nominal return seems very high: {format_percentage(nominal_return)}")
    
    if abs(inflation_rate) > 1:  # More than 100%
        warnings.append(f"Inflation rate seems very high: {format_percentage(inflation_rate)}")
    
    if inflation_rate <= -1:  # -100% or lower
        warnings.append("Inflation rate of -100% or lower would cause division by zero")
        return False, "; ".join(warnings)
    
    return True, "; ".join(warnings) if warnings else None

def calculate_purchasing_power(initial_amount, real_return, years):
    """
    Calculate the purchasing power after a given number of years
    
    Args:
        initial_amount (float): Initial investment amount
        real_return (float): Real return rate (decimal)
        years (int): Number of years
    
    Returns:
        float: Final purchasing power
    """
    return initial_amount * ((1 + real_return) ** years)

def format_currency(amount, currency="₹", decimal_places=2):
    """
    Format currency amounts with Indian Rupee symbol and proper formatting
    
    Args:
        amount (float): Amount to format
        currency (str): Currency symbol (default: ₹)
        decimal_places (int): Number of decimal places
    
    Returns:
        str: Formatted currency string
    """
    # Indian number formatting with commas
    if amount >= 10000000:  # 1 crore
        return f"{currency}{amount/10000000:.2f} Cr"
    elif amount >= 100000:  # 1 lakh
        return f"{currency}{amount/100000:.2f} L"
    else:
        return f"{currency}{amount:,.{decimal_places}f}"

def calculate_investment_scenarios(initial_amount, nominal_return, inflation_rate, years_list=None):
    """
    Calculate investment scenarios for multiple time periods
    
    Args:
        initial_amount (float): Initial investment amount
        nominal_return (float): Nominal return rate (decimal)
        inflation_rate (float): Inflation rate (decimal)
        years_list (list): List of years to calculate for
    
    Returns:
        dict: Dictionary with calculation results
    """
    if years_list is None:
        years_list = [1, 5, 10, 15, 20, 25, 30]
    
    real_return = calculate_real_return(nominal_return, inflation_rate)
    
    scenarios = []
    for years in years_list:
        nominal_value = initial_amount * ((1 + nominal_return) ** years)
        real_value = calculate_purchasing_power(initial_amount, real_return, years)
        inflation_impact = nominal_value - real_value
        
        scenarios.append({
            'years': years,
            'nominal_value': nominal_value,
            'real_value': real_value,
            'inflation_impact': inflation_impact,
            'nominal_formatted': format_currency(nominal_value),
            'real_formatted': format_currency(real_value),
            'inflation_formatted': format_currency(inflation_impact)
        })
    
    return {
        'initial_amount': initial_amount,
        'nominal_return': nominal_return,
        'inflation_rate': inflation_rate,
        'real_return': real_return,
        'scenarios': scenarios
    }

def parse_currency_input(amount_str):
    """
    Parse currency input handling various formats
    
    Args:
        amount_str (str): Input string (e.g., "1000", "1,000", "₹1000", "1L", "1 lakh")
    
    Returns:
        float: Parsed amount
    """
    if not amount_str or amount_str.strip() == '':
        return 100000  # Default 1 lakh
        
    amount_str = str(amount_str).strip().upper()
    
    # Remove currency symbols and spaces
    amount_str = amount_str.replace('₹', '').replace('RS', '').replace('INR', '')
    amount_str = amount_str.replace(',', '').replace(' ', '').strip()
    
    # Handle Indian number formats
    if 'CRORE' in amount_str or 'CR' in amount_str:
        number_part = amount_str.replace('CRORE', '').replace('CR', '').strip()
        number = float(number_part) if number_part else 1
        return number * 10000000  # 1 crore = 10 million
    elif 'LAKH' in amount_str:
        number_part = amount_str.replace('LAKH', '').strip()
        number = float(number_part) if number_part else 1
        return number * 100000  # 1 lakh = 100 thousand
    elif amount_str.endswith('L') and len(amount_str) > 1:
        number_part = amount_str[:-1].strip()
        number = float(number_part) if number_part else 1
        return number * 100000  # 1 lakh = 100 thousand
    elif 'K' in amount_str:
        number_part = amount_str.replace('K', '').strip()
        number = float(number_part) if number_part else 1
        return number * 1000  # 1K = 1000
    else:
        try:
            return float(amount_str)
        except ValueError:
            raise ValueError(f"Cannot parse amount: {amount_str}. Use formats like '50000', '1L', '2.5 lakh', etc.")

def calculate_detailed_projections(initial_amount, nominal_return, inflation_rate, years_list=None, include_monthly=True):
    """
    Calculate detailed future value projections with monthly and yearly breakdowns
    
    Args:
        initial_amount (float): Initial investment amount
        nominal_return (float): Nominal return rate (decimal)
        inflation_rate (float): Inflation rate (decimal)
        years_list (list): List of years to calculate for
        include_monthly (bool): Whether to include monthly breakdowns
    
    Returns:
        dict: Detailed projection data
    """
    if years_list is None:
        years_list = [1, 2, 3, 5, 7, 10, 15, 20, 25, 30]
    
    real_return = calculate_real_return(nominal_return, inflation_rate)
    
    projections = {
        'initial_amount': initial_amount,
        'nominal_return_annual': nominal_return,
        'inflation_rate_annual': inflation_rate,
        'real_return_annual': real_return,
        'yearly_projections': [],
        'monthly_projections': [] if include_monthly else None,
        'summary': {
            'best_year': None,
            'worst_year': None,
            'breakeven_years': None
        }
    }
    
    # Calculate yearly projections
    for years in years_list:
        nominal_value = initial_amount * ((1 + nominal_return) ** years)
        real_value = initial_amount * ((1 + real_return) ** years)
        inflation_impact = nominal_value - real_value
        
        # Calculate gains
        nominal_gain = nominal_value - initial_amount
        real_gain = real_value - initial_amount
        
        # Calculate effective rates
        effective_nominal_rate = (nominal_value / initial_amount) ** (1/years) - 1
        effective_real_rate = (real_value / initial_amount) ** (1/years) - 1
        
        yearly_data = {
            'years': years,
            'nominal_value': nominal_value,
            'real_value': real_value,
            'inflation_impact': inflation_impact,
            'nominal_gain': nominal_gain,
            'real_gain': real_gain,
            'nominal_gain_percentage': (nominal_gain / initial_amount) * 100,
            'real_gain_percentage': (real_gain / initial_amount) * 100,
            'effective_nominal_rate': effective_nominal_rate,
            'effective_real_rate': effective_real_rate,
            'purchasing_power_ratio': real_value / nominal_value,
            'formatted': {
                'nominal_value': format_currency(nominal_value),
                'real_value': format_currency(real_value),
                'inflation_impact': format_currency(inflation_impact),
                'nominal_gain': format_currency(nominal_gain),
                'real_gain': format_currency(real_gain)
            }
        }
        
        projections['yearly_projections'].append(yearly_data)
    
    # Calculate monthly projections for first few years if requested
    if include_monthly:
        monthly_nominal_rate = (1 + nominal_return) ** (1/12) - 1
        monthly_real_rate = (1 + real_return) ** (1/12) - 1
        
        for years in [1, 2, 3, 5]:
            if years <= max(years_list):
                months_total = years * 12
                monthly_data = []
                
                for month in range(1, months_total + 1):
                    months_elapsed = month
                    years_elapsed = months_elapsed / 12
                    
                    nominal_value = initial_amount * ((1 + monthly_nominal_rate) ** months_elapsed)
                    real_value = initial_amount * ((1 + monthly_real_rate) ** months_elapsed)
                    
                    monthly_entry = {
                        'month': month,
                        'years': years_elapsed,
                        'nominal_value': nominal_value,
                        'real_value': real_value,
                        'nominal_gain': nominal_value - initial_amount,
                        'real_gain': real_value - initial_amount,
                        'formatted': {
                            'nominal_value': format_currency(nominal_value),
                            'real_value': format_currency(real_value)
                        }
                    }
                    monthly_data.append(monthly_entry)
                
                projections['monthly_projections'].append({
                    'target_years': years,
                    'monthly_breakdown': monthly_data
                })
    
    # Calculate summary statistics
    if projections['yearly_projections']:
        best_year = max(projections['yearly_projections'], key=lambda x: x['real_gain_percentage'])
        worst_year = min(projections['yearly_projections'], key=lambda x: x['real_gain_percentage'])
        
        projections['summary']['best_year'] = best_year['years']
        projections['summary']['worst_year'] = worst_year['years'] if worst_year['real_gain'] < 0 else None
        
        # Find breakeven point (where real gain becomes positive)
        for proj in projections['yearly_projections']:
            if proj['real_gain'] > 0:
                projections['summary']['breakeven_years'] = proj['years']
                break
    
    return projections

def calculate_sip_projections(monthly_amount, nominal_return, inflation_rate, years_list=None):
    """
    Calculate SIP (Systematic Investment Plan) projections
    
    Args:
        monthly_amount (float): Monthly SIP amount
        nominal_return (float): Annual nominal return rate (decimal)
        inflation_rate (float): Annual inflation rate (decimal)
        years_list (list): List of years to calculate for
    
    Returns:
        dict: SIP projection data
    """
    if years_list is None:
        years_list = [1, 2, 3, 5, 7, 10, 15, 20, 25, 30]
    
    monthly_nominal_rate = (1 + nominal_return) ** (1/12) - 1
    real_return = calculate_real_return(nominal_return, inflation_rate)
    monthly_real_rate = (1 + real_return) ** (1/12) - 1
    
    projections = {
        'monthly_amount': monthly_amount,
        'annual_investment': monthly_amount * 12,
        'nominal_return_annual': nominal_return,
        'inflation_rate_annual': inflation_rate,
        'real_return_annual': real_return,
        'sip_projections': []
    }
    
    for years in years_list:
        months = years * 12
        total_invested = monthly_amount * months
        
        # Future Value of SIP (ordinary annuity)
        if monthly_nominal_rate > 0:
            nominal_value = monthly_amount * (((1 + monthly_nominal_rate) ** months - 1) / monthly_nominal_rate)
        else:
            nominal_value = monthly_amount * months
            
        if monthly_real_rate > 0:
            real_value = monthly_amount * (((1 + monthly_real_rate) ** months - 1) / monthly_real_rate)
        else:
            real_value = monthly_amount * months
        
        nominal_gain = nominal_value - total_invested
        real_gain = real_value - total_invested
        
        sip_data = {
            'years': years,
            'months': months,
            'total_invested': total_invested,
            'nominal_value': nominal_value,
            'real_value': real_value,
            'nominal_gain': nominal_gain,
            'real_gain': real_gain,
            'nominal_gain_percentage': (nominal_gain / total_invested) * 100 if total_invested > 0 else 0,
            'real_gain_percentage': (real_gain / total_invested) * 100 if total_invested > 0 else 0,
            'formatted': {
                'total_invested': format_currency(total_invested),
                'nominal_value': format_currency(nominal_value),
                'real_value': format_currency(real_value),
                'nominal_gain': format_currency(nominal_gain),
                'real_gain': format_currency(real_gain)
            }
        }
        
        projections['sip_projections'].append(sip_data)
    
    return projections