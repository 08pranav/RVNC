#!/usr/bin/env python3
"""
Advanced RVNC Demo - Detailed Projections
Shows exact money values after X years and Y months
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from calculator import (
    calculate_detailed_projections, 
    calculate_sip_projections,
    parse_currency_input,
    format_currency
)
from data_provider import get_country_inflation_rate, get_investment_type_return

def demo_real_numbers():
    """Show REAL MONEY projections - exactly what the user wanted!"""
    print("💰 REAL MONEY PROJECTIONS - Your Investment's Future Value")
    print("=" * 70)
    
    # Sample scenarios
    scenarios = [
        {
            'name': '🏦 Conservative FD Investment',
            'amount': 500000,  # 5 lakh
            'investment': 'fixed_deposits',
            'country': 'IN'
        },
        {
            'name': '📈 Aggressive Stock Investment', 
            'amount': 1000000,  # 10 lakh
            'investment': 'stocks',
            'country': 'IN'
        },
        {
            'name': '🌍 US Stock Market Investment',
            'amount': 1000000,  # 10 lakh equivalent
            'investment': 'stocks', 
            'country': 'US'
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['name']}")
        print("-" * 50)
        
        # Get data
        inflation_data = get_country_inflation_rate(scenario['country'])
        nominal_return = get_investment_type_return(scenario['investment'])
        inflation_rate = inflation_data['rate'] / 100
        
        print(f"💵 Initial Investment: {format_currency(scenario['amount'])}")
        print(f"📊 Investment Type: {scenario['investment'].replace('_', ' ').title()}")
        print(f"🌍 Country: {inflation_data['flag']} {inflation_data['country']}")
        print(f"📈 Expected Return: {nominal_return*100:.1f}% per year")
        print(f"📉 Inflation Rate: {inflation_data['rate']:.2f}% per year")
        print()
        
        # Calculate projections
        projections = calculate_detailed_projections(
            scenario['amount'], nominal_return, inflation_rate,
            [1, 2, 3, 5, 7, 10, 15, 20, 25, 30], include_monthly=True
        )
        
        print("🎯 YEAR-BY-YEAR PROJECTIONS:")
        print(f"{'Years':<6} {'Nominal Value':<15} {'Real Value':<15} {'Real Gain':<15} {'Status'}")
        print("-" * 70)
        
        for proj in projections['yearly_projections']:
            status = "🎉 Excellent" if proj['real_gain_percentage'] > 50 else \
                    "✅ Good" if proj['real_gain_percentage'] > 0 else \
                    "❌ Loss"
            
            print(f"{proj['years']:<6} "
                  f"{proj['formatted']['nominal_value']:<15} "
                  f"{proj['formatted']['real_value']:<15} "
                  f"{proj['real_gain_percentage']:>6.1f}%{'':<8} "
                  f"{status}")
        
        # Show specific year examples
        print(f"\n🔍 SPECIFIC EXAMPLES:")
        for proj in projections['yearly_projections']:
            if proj['years'] in [5, 10, 20]:
                print(f"After {proj['years']} years: Your {format_currency(scenario['amount'])} becomes "
                      f"{proj['formatted']['real_value']} (real purchasing power)")
        
        # Show monthly progression for first year
        if projections['monthly_projections']:
            first_year = projections['monthly_projections'][0]
            print(f"\n📅 MONTHLY BREAKDOWN (First Year):")
            print(f"{'Month':<6} {'Real Value':<15} {'Real Gain':<15}")
            print("-" * 40)
            
            for i, month in enumerate(first_year['monthly_breakdown'][:12], 1):
                if i % 3 == 0:  # Show every 3rd month
                    print(f"{i:<6} "
                          f"{month['formatted']['real_value']:<15} "
                          f"{format_currency(month['real_gain']):<15}")
        
        print("\n" + "="*70)

def demo_sip_real_numbers():
    """Show SIP (monthly investment) real projections"""
    print("\n💳 SIP (MONTHLY INVESTMENT) PROJECTIONS")
    print("=" * 70)
    
    sip_scenarios = [
        {'monthly': 10000, 'investment': 'mutual_funds_equity', 'name': '🎯 Equity Mutual Fund SIP'},
        {'monthly': 25000, 'investment': 'stocks', 'name': '📈 Direct Stock SIP'},
        {'monthly': 5000, 'investment': 'elss', 'name': '💰 Tax Saving ELSS SIP'},
    ]
    
    for scenario in sip_scenarios:
        print(f"\n{scenario['name']}")
        print("-" * 50)
        
        # Get Indian data
        inflation_data = get_country_inflation_rate('IN')
        nominal_return = get_investment_type_return(scenario['investment'])
        inflation_rate = inflation_data['rate'] / 100
        
        print(f"💳 Monthly SIP: {format_currency(scenario['monthly'])}")
        print(f"📊 Annual Investment: {format_currency(scenario['monthly'] * 12)}")
        print(f"📈 Expected Return: {nominal_return*100:.1f}% per year")
        print(f"📉 Inflation: {inflation_data['rate']:.2f}% per year")
        print()
        
        # Calculate SIP projections
        sip_data = calculate_sip_projections(
            scenario['monthly'], nominal_return, inflation_rate,
            [1, 2, 3, 5, 7, 10, 15, 20, 25, 30]
        )
        
        print("🎯 SIP PROJECTIONS:")
        print(f"{'Years':<6} {'Invested':<12} {'Real Value':<15} {'Real Gain':<12} {'Gain %'}")
        print("-" * 65)
        
        for proj in sip_data['sip_projections']:
            print(f"{proj['years']:<6} "
                  f"{proj['formatted']['total_invested']:<12} "
                  f"{proj['formatted']['real_value']:<15} "
                  f"{proj['formatted']['real_gain']:<12} "
                  f"{proj['real_gain_percentage']:>6.1f}%")
        
        # Highlight key milestones
        print(f"\n🏆 KEY MILESTONES:")
        for proj in sip_data['sip_projections']:
            if proj['years'] in [10, 20, 30]:
                total_invested = proj['total_invested']
                real_value = proj['real_value']
                multiplier = real_value / total_invested if total_invested > 0 else 0
                
                print(f"• After {proj['years']} years: Invested {proj['formatted']['total_invested']}, "
                      f"Got {proj['formatted']['real_value']} (real value)")
                print(f"  💡 Your money grew {multiplier:.1f}x in real terms!")
        
        print("\n" + "="*70)

def demo_specific_questions():
    """Answer specific user questions about projections"""
    print("\n❓ ANSWERING YOUR SPECIFIC QUESTIONS")
    print("=" * 70)
    
    # Example: ₹5 lakh in stocks for different time periods
    amount = 500000
    investment = 'stocks'
    country = 'IN'
    
    inflation_data = get_country_inflation_rate(country)
    nominal_return = get_investment_type_return(investment)
    inflation_rate = inflation_data['rate'] / 100
    
    projections = calculate_detailed_projections(
        amount, nominal_return, inflation_rate,
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], include_monthly=True
    )
    
    print(f"🎯 SCENARIO: {format_currency(amount)} invested in stocks")
    print(f"📈 Expected return: {nominal_return*100:.1f}% per year")
    print(f"📉 India inflation: {inflation_data['rate']:.2f}% per year")
    print()
    
    print("📊 EXACT ANSWERS TO 'HOW MUCH AFTER X YEARS?':")
    for proj in projections['yearly_projections']:
        real_gain = proj['real_value'] - amount
        print(f"• After {proj['years']} year{'s' if proj['years'] > 1 else ''}: "
              f"{proj['formatted']['real_value']} "
              f"(gain: {format_currency(real_gain)}, "
              f"{proj['real_gain_percentage']:.1f}%)")
    
    # Monthly breakdown for first 2 years
    if projections['monthly_projections']:
        print(f"\n📅 MONTHLY PROGRESS (First 24 months):")
        first_year_data = projections['monthly_projections'][0]['monthly_breakdown']
        
        for month in first_year_data[:24]:
            if month['month'] % 6 == 0:  # Every 6 months
                years = month['month'] / 12
                real_gain = month['real_value'] - amount
                print(f"• After {month['month']} months ({years:.1f} years): "
                      f"{month['formatted']['real_value']} "
                      f"(gain: {format_currency(real_gain)})")

def main():
    """Run all advanced demos"""
    print("🚀 ADVANCED RVNC CALCULATOR - REAL MONEY PROJECTIONS")
    print("   See EXACTLY how much money you'll have after X years!")
    print("=" * 75)
    
    demo_real_numbers()
    demo_sip_real_numbers() 
    demo_specific_questions()
    
    print(f"\n🎉 SUMMARY:")
    print("✅ Added detailed year-by-year projections")
    print("✅ Added month-by-month tracking")
    print("✅ Added SIP (monthly investment) calculations")
    print("✅ Shows REAL money values, not just percentages")
    print("✅ Country-specific inflation rates included")
    print("✅ Investment-type specific returns included")
    print()
    print("🌐 Enhanced Web Interface: http://127.0.0.1:5000")
    print("📈 Now shows detailed projections with exact rupee amounts!")
    print("💰 Perfect for financial planning and goal setting!")

if __name__ == "__main__":
    main()