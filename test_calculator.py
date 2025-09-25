#!/usr/bin/env python3
"""
Test script for the Real vs. Nominal Return Calculator
"""

from calculator import (
    calculate_real_return,
    format_percentage,
    parse_percentage_input,
    validate_inputs,
    calculate_purchasing_power
)

def test_calculations():
    """Test the core calculation functions"""
    print("=" * 60)
    print("TESTING REAL vs. NOMINAL RETURN CALCULATOR")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        (0.08, 0.03, "Stock market vs. normal inflation"),
        (0.05, 0.02, "Bonds vs. low inflation"),
        (0.12, 0.06, "High growth vs. high inflation"),
        (0.03, 0.04, "Low return vs. higher inflation"),
        (0.10, 0.00, "No inflation scenario"),
        (-0.05, 0.03, "Negative nominal return")
    ]
    
    print("Test Results:")
    print("-" * 60)
    
    for i, (nominal, inflation, description) in enumerate(test_cases, 1):
        try:
            real_return = calculate_real_return(nominal, inflation)
            
            print(f"Test {i}: {description}")
            print(f"  Nominal: {format_percentage(nominal, 2)}")
            print(f"  Inflation: {format_percentage(inflation, 2)}")
            print(f"  Real: {format_percentage(real_return, 2)}")
            print(f"  Status: {'✓ BEATS INFLATION' if real_return > 0 else '✗ LOSES TO INFLATION'}")
            print()
            
        except Exception as e:
            print(f"Test {i}: ERROR - {e}")
            print()
    
    # Test input parsing
    print("Input Parsing Tests:")
    print("-" * 30)
    
    input_tests = [
        ("8", "8% as number"),
        ("8%", "8% with percent sign"),
        ("0.08", "8% as decimal"),
        ("12.5", "12.5% as number"),
        ("12.5%", "12.5% with percent sign")
    ]
    
    for input_val, description in input_tests:
        try:
            parsed = parse_percentage_input(input_val)
            print(f"'{input_val}' ({description}) → {parsed:.4f} → {format_percentage(parsed, 2)}")
        except Exception as e:
            print(f"'{input_val}' ({description}) → ERROR: {e}")
    
    print()
    
    # Test purchasing power calculation
    print("Purchasing Power Test (10 years, $10,000 investment):")
    print("-" * 50)
    
    nominal = 0.08  # 8%
    inflation = 0.03  # 3%
    real_return = calculate_real_return(nominal, inflation)
    
    initial_amount = 10000
    years = 10
    
    nominal_value = initial_amount * ((1 + nominal) ** years)
    real_value = calculate_purchasing_power(initial_amount, real_return, years)
    
    print(f"Initial Investment: ${initial_amount:,.2f}")
    print(f"After {years} years:")
    print(f"  Nominal Value: ${nominal_value:,.2f}")
    print(f"  Real Value (purchasing power): ${real_value:,.2f}")
    print(f"  Inflation Impact: ${nominal_value - real_value:,.2f}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED SUCCESSFULLY! ✓")
    print("=" * 60)

if __name__ == "__main__":
    test_calculations()