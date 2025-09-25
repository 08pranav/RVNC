#!/usr/bin/env python3
"""
Quick demo of the enhanced Real vs. Nominal Return Calculator
Shows the new features with Indian Rupee support and custom amounts
"""

from calculator import (
    calculate_real_return,
    format_percentage,
    format_currency,
    parse_currency_input,
    calculate_investment_scenarios
)

def demo_enhanced_features():
    """Demo the new enhanced features"""
    print("🎉" * 25)
    print("   ENHANCED CALCULATOR DEMO")
    print("🎉" * 25)
    print()
    
    print("🆕 NEW FEATURES:")
    print("✅ Custom investment amounts in Indian Rupees")
    print("✅ Smart currency parsing (50000, 1L, 2.5 lakh, etc.)")
    print("✅ Indian investment scenarios")
    print("✅ Extended time period analysis")
    print("✅ Beautiful Rupee formatting")
    print()
    
    # Demo different investment amounts
    print("💰 DEMO: Different Investment Amounts")
    print("-" * 50)
    
    scenarios = [
        ("Fresh Graduate", "25000", 12, 6),
        ("Middle Class Family", "1L", 10, 6),
        ("Senior Professional", "5L", 8, 6),
        ("HNI Investment", "50L", 15, 6)
    ]
    
    for name, amount_str, nominal, inflation in scenarios:
        amount = parse_currency_input(amount_str)
        real_return = calculate_real_return(nominal/100, inflation/100)
        
        print(f"\n👤 {name}:")
        print(f"   Investment: {format_currency(amount)}")
        print(f"   Nominal Return: {nominal}% | Inflation: {inflation}%")
        print(f"   Real Return: {format_percentage(real_return, 2)}")
        
        # Show 1 year impact
        nominal_1yr = amount * (1 + nominal/100)
        real_1yr = amount * (1 + real_return)
        print(f"   After 1 year: {format_currency(nominal_1yr)} → {format_currency(real_1yr)} (real)")
    
    print()
    print("🌐 WEB INTERFACE ENHANCEMENTS:")
    print("-" * 40)
    print("✅ Investment amount input field added")
    print("✅ Rupee symbol and Indian formatting")
    print("✅ Extended analysis tables (up to 30 years)")
    print("✅ Smart examples with suggested amounts")
    print("✅ Real-time currency formatting")
    
    print()
    print("🖥️ CLI ENHANCEMENTS:")
    print("-" * 25)
    print("✅ Custom amount input with validation")
    print("✅ Multiple format support (50000, 1L, 2.5 lakh)")
    print("✅ Extended analysis periods")
    print("✅ Indian investment examples")
    
    print()
    print("📊 EXAMPLE CALCULATION:")
    print("-" * 30)
    amount = parse_currency_input("75000")
    nominal = 0.12  # 12%
    inflation = 0.06  # 6%
    
    scenarios_data = calculate_investment_scenarios(amount, nominal, inflation, [1, 5, 10, 20])
    
    print(f"Investment: {format_currency(amount)}")
    print(f"Nominal Return: {format_percentage(nominal, 1)}")
    print(f"Inflation: {format_percentage(inflation, 1)}")
    print(f"Real Return: {format_percentage(scenarios_data['real_return'], 2)}")
    print()
    
    for scenario in scenarios_data['scenarios']:
        print(f"Year {scenario['years']:2d}: {scenario['nominal_formatted']} → {scenario['real_formatted']}")
    
    print()
    print("🚀 HOW TO USE:")
    print("-" * 15)
    print("1. Run: python3 launcher.py")
    print("2. Choose option 1 (CLI) or 2 (Web)")
    print("3. Enter your returns and custom amount")
    print("4. See detailed Indian Rupee analysis!")
    
    print()
    print("🎯 Try these amounts:")
    print("• 50000 (fifty thousand)")
    print("• 1L (one lakh)")
    print("• 2.5L (two and half lakh)")
    print("• 1 crore (one crore)")
    print()

if __name__ == "__main__":
    demo_enhanced_features()
