#!/usr/bin/env python3
"""
Real vs. Nominal Return Calculator - Command Line Interface
Financial Concept: Calculating inflation-adjusted returns
"""

import sys
import os
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

def print_header():
    """Print the application header"""
    print("=" * 60)
    print("    REAL vs. NOMINAL RETURN CALCULATOR")
    print("=" * 60)
    print("Financial Concept: Inflation-adjusted return calculation")
    print("Formula: Real Return = ((1 + nominal) / (1 + inflation)) - 1")
    print("=" * 60)

def print_help():
    """Print help information"""
    print("\nHOW TO USE:")
    print("• Enter returns as percentages (e.g., '8' for 8% or '8%')")
    print("• Or as decimals (e.g., '0.08' for 8%)")
    print("• Type 'quit' or 'exit' to stop")
    print("• Type 'help' for this message")
    print("• Type 'example' for sample calculations")

def print_examples():
    """Print example calculations"""
    print("\nEXAMPLE CALCULATIONS:")
    print("-" * 40)
    
    examples = [
        (0.08, 0.03, "Stock market return vs. typical inflation"),
        (0.05, 0.02, "Bond return vs. low inflation"),
        (0.12, 0.06, "High growth investment vs. high inflation"),
        (0.03, 0.04, "Low return vs. higher inflation (negative real return)")
    ]
    
    for nominal, inflation, description in examples:
        real = calculate_real_return(nominal, inflation)
        print(f"• {description}")
        print(f"  Nominal: {format_percentage(nominal, 2)}, "
              f"Inflation: {format_percentage(inflation, 2)} → "
              f"Real: {format_percentage(real, 2)}")
    print()

def get_user_input(prompt, input_type="percentage"):
    """Get and validate user input"""
    while True:
        try:
            user_input = input(prompt).strip().lower()
            
            if user_input in ['quit', 'exit', 'q']:
                return 'quit'
            elif user_input == 'help':
                print_help()
                continue
            elif user_input == 'example':
                print_examples()
                continue
            elif user_input == '':
                print("Please enter a value.")
                continue
            
            if input_type == "percentage":
                return parse_percentage_input(user_input)
            elif input_type == "number":
                return float(user_input)
            elif input_type == "integer":
                return int(user_input)
                
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            return 'quit'

def advanced_analysis(nominal_return, inflation_rate, real_return, custom_amount=None):
    """Provide additional analysis and insights"""
    print("\n" + "=" * 50)
    print("DETAILED ANALYSIS")
    print("=" * 50)
    
    # Use custom amount if provided, otherwise default
    if custom_amount is None:
        initial_amount = 100000  # Default ₹1,00,000
        print(f"PURCHASING POWER IMPACT (on {format_currency(initial_amount)} investment):")
    else:
        initial_amount = custom_amount
        print(f"PURCHASING POWER IMPACT (on {format_currency(initial_amount)} investment):")
    
    print("-" * 60)
    
    # Calculate scenarios
    scenarios_data = calculate_investment_scenarios(
        initial_amount, nominal_return, inflation_rate, 
        [1, 5, 10, 15, 20, 25, 30]
    )
    
    for scenario in scenarios_data['scenarios']:
        years = scenario['years']
        print(f"After {years:2d} years:")
        print(f"  Nominal value:   {scenario['nominal_formatted']}")
        print(f"  Real value:      {scenario['real_formatted']}")
        print(f"  Inflation cost:  {scenario['inflation_formatted']}")
        
        # Show percentage growth
        nominal_growth = ((scenario['nominal_value'] / initial_amount) - 1) * 100
        real_growth = ((scenario['real_value'] / initial_amount) - 1) * 100
        print(f"  Nominal growth:  {nominal_growth:.1f}%")
        print(f"  Real growth:     {real_growth:.1f}%")
        print()
    
    # Provide insights
    print("INVESTMENT INSIGHTS:")
    print("-" * 30)
    
    if real_return > 0:
        print(f"✓ Your investment beats inflation by {format_percentage(real_return, 2)}")
        print("✓ Your purchasing power increases over time")
    elif real_return == 0:
        print("⚠ Your investment exactly matches inflation")
        print("⚠ Your purchasing power remains constant")
    else:
        print(f"✗ Your investment loses to inflation by {format_percentage(abs(real_return), 2)}")
        print("✗ Your purchasing power decreases over time")
    
    # Risk assessment
    inflation_buffer = real_return * 100
    if inflation_buffer > 3:
        risk_level = "Low"
        risk_msg = "Good buffer against inflation variations"
    elif inflation_buffer > 0:
        risk_level = "Medium"
        risk_msg = "Small buffer against inflation increases"
    else:
        risk_level = "High"
        risk_msg = "Vulnerable to inflation increases"
    
    print(f"\nInflation Risk Level: {risk_level}")
    print(f"Assessment: {risk_msg}")

def main():
    """Main application loop"""
    print_header()
    print_help()
    
    while True:
        print("\n" + "-" * 60)
        print("NEW CALCULATION")
        print("-" * 60)
        
        # Get nominal return
        nominal_return = get_user_input(
            "Enter nominal return rate (e.g., '8' for 8%): "
        )
        if nominal_return == 'quit':
            break
        
        # Get inflation rate
        inflation_rate = get_user_input(
            "Enter inflation rate (e.g., '3' for 3%): "
        )
        if inflation_rate == 'quit':
            break
        
        # Ask for custom investment amount
        print("\n💰 INVESTMENT AMOUNT:")
        print("Default: ₹1,00,000 (1 Lakh) or enter your own amount")
        custom_amount_input = input("Enter investment amount (e.g., '50000', '2L', '1.5 lakh') or press Enter for default: ").strip()
        
        if custom_amount_input.lower() in ['quit', 'exit', 'q']:
            break
        elif custom_amount_input == '':
            custom_amount = 100000  # Default 1 lakh
            print(f"✅ Using default amount: {format_currency(custom_amount)}")
        else:
            try:
                custom_amount = parse_currency_input(custom_amount_input)
                print(f"✅ Using investment amount: {format_currency(custom_amount)}")
            except ValueError as e:
                print(f"❌ Invalid amount format: {e}. Using default ₹1,00,000")
                custom_amount = 100000
        
        try:
            # Validate inputs
            is_valid, warning = validate_inputs(nominal_return, inflation_rate)
            
            if not is_valid:
                print(f"❌ Error: {warning}")
                continue
            
            if warning:
                print(f"⚠️  Warning: {warning}")
                proceed = get_user_input("Continue anyway? (y/n): ", "text")
                if proceed == 'quit' or (proceed and proceed[0].lower() != 'y'):
                    continue
            
            # Calculate real return
            real_return = calculate_real_return(nominal_return, inflation_rate)
            
            # Display results
            print("\n" + "=" * 60)
            print("CALCULATION RESULTS")
            print("=" * 60)
            print(f"Nominal Return:    {format_percentage(nominal_return, 4)}")
            print(f"Inflation Rate:    {format_percentage(inflation_rate, 4)}")
            print(f"Real Return:       {format_percentage(real_return, 4)}")
            
            # Show the calculation
            print(f"\nCalculation:")
            print(f"Real Return = ((1 + {nominal_return:.4f}) / (1 + {inflation_rate:.4f})) - 1")
            print(f"            = ({1 + nominal_return:.4f} / {1 + inflation_rate:.4f}) - 1")
            print(f"            = {(1 + nominal_return) / (1 + inflation_rate):.6f} - 1")
            print(f"            = {real_return:.6f}")
            print(f"            = {format_percentage(real_return, 4)}")
            
            # Show investment amount impact
            print(f"\n💡 INVESTMENT IMPACT:")
            print(f"Your {format_currency(custom_amount)} investment:")
            one_year_nominal = custom_amount * (1 + nominal_return)
            one_year_real = custom_amount * (1 + real_return)
            print(f"• After 1 year (nominal): {format_currency(one_year_nominal)}")
            print(f"• After 1 year (real):    {format_currency(one_year_real)}")
            print(f"• Inflation cost:         {format_currency(one_year_nominal - one_year_real)}")
            
            # Ask for advanced analysis
            advanced = get_user_input("\nShow detailed analysis with multiple time periods? (y/n): ", "text")
            if advanced and advanced[0].lower() == 'y':
                advanced_analysis(nominal_return, inflation_rate, real_return, custom_amount)
            
        except Exception as e:
            print(f"❌ Calculation error: {e}")
        
        # Ask if user wants to continue
        print("\n" + "-" * 60)
        continue_calc = get_user_input("Calculate another? (y/n): ", "text")
        if continue_calc == 'quit' or (continue_calc and continue_calc[0].lower() != 'y'):
            break
    
    print("\n" + "=" * 60)
    print("Thank you for using the Real vs. Nominal Return Calculator!")
    print("Understanding inflation impact is crucial for investment planning.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)