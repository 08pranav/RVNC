#!/usr/bin/env python3
"""
Real vs. Nominal Return Calculator - Indian Investment Examples
Demonstrates various Indian investment scenarios with Rupee amounts
"""

from calculator import (
    calculate_real_return, 
    format_percentage, 
    format_currency,
    calculate_investment_scenarios
)

def show_indian_examples():
    """Display various Indian investment scenarios"""
    print("=" * 80)
    print("    INDIAN INVESTMENT SCENARIOS - Real vs. Nominal Returns")
    print("=" * 80)
    print("Understanding how inflation affects your Indian investments")
    print("All amounts in Indian Rupees (₹)")
    print("=" * 80)
    
    scenarios = [
        {
            'name': '📈 Nifty 50 Index Fund',
            'description': 'Long-term Indian stock market performance',
            'nominal': 0.12,  # 12%
            'inflation': 0.06,  # 6%
            'amount': 100000,  # ₹1 Lakh
            'explanation': 'Indian stock market has historically provided good returns'
        },
        {
            'name': '🏦 Fixed Deposit (FD)',
            'description': 'Traditional bank fixed deposit',
            'nominal': 0.06,  # 6%
            'inflation': 0.06,  # 6%
            'amount': 500000,  # ₹5 Lakh
            'explanation': 'Safe but often barely beats inflation'
        },
        {
            'name': '💰 Post Office Savings',
            'description': 'Government Post Office Savings Account',
            'nominal': 0.04,  # 4%
            'inflation': 0.06,  # 6%
            'amount': 50000,  # ₹50,000
            'explanation': 'Very safe but loses to inflation in recent years'
        },
        {
            'name': '🏠 Real Estate Mumbai',
            'description': 'Mumbai real estate investment',
            'nominal': 0.08,  # 8%
            'inflation': 0.06,  # 6%
            'amount': 5000000,  # ₹50 Lakh
            'explanation': 'Real estate in metros can provide inflation protection'
        },
        {
            'name': '🌟 ELSS Mutual Funds',
            'description': 'Equity Linked Savings Scheme (Tax Saving)',
            'nominal': 0.14,  # 14%
            'inflation': 0.06,  # 6%
            'amount': 150000,  # ₹1.5 Lakh (80C limit)
            'explanation': 'Tax-saving equity funds with good long-term potential'
        },
        {
            'name': '💎 Gold Investment',
            'description': 'Gold ETF or Digital Gold',
            'nominal': 0.09,  # 9%
            'inflation': 0.06,  # 6%
            'amount': 200000,  # ₹2 Lakh
            'explanation': 'Traditional inflation hedge in Indian context'
        },
        {
            'name': '⚡ Startup Investment',
            'description': 'Early-stage startup equity',
            'nominal': 0.25,  # 25% (high risk)
            'inflation': 0.06,  # 6%
            'amount': 100000,  # ₹1 Lakh
            'explanation': 'High-risk, high-reward investment option'
        },
        {
            'name': '📉 High Inflation Period (2010-2012)',
            'description': 'Investment during high inflation period',
            'nominal': 0.08,  # 8%
            'inflation': 0.10,  # 10%
            'amount': 300000,  # ₹3 Lakh
            'explanation': 'Even decent returns can lose to high inflation'
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print("-" * 70)
        print(f"Investment Amount: {format_currency(scenario['amount'])}")
        print(f"Scenario: {scenario['description']}")
        print(f"Context: {scenario['explanation']}")
        
        # Calculate scenarios for this investment
        scenarios_data = calculate_investment_scenarios(
            scenario['amount'], scenario['nominal'], scenario['inflation'],
            [1, 5, 10, 15, 20]
        )
        
        real_return = scenarios_data['real_return']
        
        print(f"\n📊 Financial Analysis:")
        print(f"   Nominal Return:  {format_percentage(scenario['nominal'], 1)}")
        print(f"   Inflation Rate:  {format_percentage(scenario['inflation'], 1)}")
        print(f"   Real Return:     {format_percentage(real_return, 2)}")
        
        # Determine assessment
        if real_return > 0.08:  # > 8%
            status = "🎉 OUTSTANDING - Excellent wealth building!"
            color = "green"
        elif real_return > 0.05:  # > 5%
            status = "✅ EXCELLENT - Strong real growth"
            color = "blue"
        elif real_return > 0.02:  # > 2%
            status = "👍 GOOD - Beats inflation comfortably"
            color = "green"
        elif real_return > 0:  # > 0%
            status = "⚠️ MODEST - Barely beats inflation"
            color = "yellow"
        else:  # <= 0%
            status = "❌ POOR - Loses purchasing power"
            color = "red"
        
        print(f"   Assessment:      {status}")
        
        # Show key time periods
        print(f"\n💡 Investment Growth Over Time:")
        key_periods = [1, 5, 10, 20]
        for scenario_data in scenarios_data['scenarios']:
            if scenario_data['years'] in key_periods:
                years = scenario_data['years']
                print(f"   After {years:2d} years: {scenario_data['nominal_formatted']} → {scenario_data['real_formatted']} (real value)")
        
        # Calculate monthly SIP equivalent
        if scenario['amount'] >= 12000:  # If amount allows monthly SIP
            monthly_sip = scenario['amount'] // 12
            print(f"\n💳 Monthly SIP Equivalent: {format_currency(monthly_sip)}/month for 1 year")
        
        if i < len(scenarios):
            print("\n" + "="*80)
    
    print(f"\n🎓 KEY INSIGHTS FOR INDIAN INVESTORS:")
    print("-" * 40)
    print("• Indian inflation averages 4-7% historically")
    print("• Equity investments typically outpace inflation over long term")
    print("• Fixed deposits often struggle against inflation")
    print("• Real estate and gold provide some inflation protection")
    print("• Tax-saving investments (ELSS) offer dual benefits")
    print("• Diversification across asset classes is crucial")
    print("• SIP in equity funds helps rupee cost averaging")
    
    print(f"\n💭 REMEMBER:")
    print("In India, aim for real returns of 3-5% minimum to build wealth!")
    print("Even 'safe' investments can be risky if they lose to inflation!")
    
    print("=" * 80)

def show_sip_calculator():
    """Show SIP (Systematic Investment Plan) examples"""
    print("\n" + "=" * 60)
    print("    SIP CALCULATOR - Monthly Investment Impact")
    print("=" * 60)
    
    sip_scenarios = [
        {'name': 'Conservative SIP', 'monthly': 5000, 'return': 0.10, 'inflation': 0.06},
        {'name': 'Moderate SIP', 'monthly': 10000, 'return': 0.12, 'inflation': 0.06},
        {'name': 'Aggressive SIP', 'monthly': 15000, 'return': 0.15, 'inflation': 0.06},
    ]
    
    for scenario in sip_scenarios:
        print(f"\n📊 {scenario['name']}:")
        print(f"Monthly Investment: {format_currency(scenario['monthly'])}")
        
        years_list = [5, 10, 15, 20]
        for years in years_list:
            # Calculate SIP future value
            monthly_return = scenario['return'] / 12
            months = years * 12
            
            # SIP Future Value Formula
            future_value = scenario['monthly'] * (((1 + monthly_return) ** months - 1) / monthly_return) * (1 + monthly_return)
            total_invested = scenario['monthly'] * months
            
            # Calculate real value
            real_return = calculate_real_return(scenario['return'], scenario['inflation'])
            monthly_real_return = real_return / 12
            real_future_value = scenario['monthly'] * (((1 + monthly_real_return) ** months - 1) / monthly_real_return) * (1 + monthly_real_return)
            
            print(f"  {years} years: Invested {format_currency(total_invested)} → "
                  f"Nominal {format_currency(future_value)} → "
                  f"Real {format_currency(real_future_value)}")

if __name__ == "__main__":
    show_indian_examples()
    
    print("\n" + "🔸" * 40)
    show_sip_calculator()
    
    print(f"\n🚀 Want to calculate your own scenario?")
    print("Run: python3 cli_calculator.py")
    print("Or: python3 app.py (for web interface)")