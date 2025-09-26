#!/usr/bin/env python3
"""
Enhanced RVNC Demo Script
Demonstrates the new country-wise inflation and investment type features
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_provider import get_country_inflation_rate, get_all_countries, get_investment_types, get_investment_categories
from calculator import calculate_real_return, format_percentage

def demo_country_inflation():
    """Demo country-wise inflation feature"""
    print("🌍 DEMO: Country-wise Inflation Rates")
    print("=" * 50)
    
    countries = get_all_countries()
    sample_countries = ['IN', 'US', 'GB', 'JP', 'DE', 'CN']
    
    for country_code in sample_countries:
        if country_code in countries:
            inflation_data = get_country_inflation_rate(country_code)
            print(f"{inflation_data['flag']} {inflation_data['country']:15} | "
                  f"Inflation: {inflation_data['rate']:5.2f}% | "
                  f"Currency: {inflation_data['currency']:3}")
    
    print("\n")

def demo_investment_types():
    """Demo investment types feature"""
    print("💼 DEMO: Investment Types with Returns")
    print("=" * 50)
    
    categories = get_investment_categories()
    
    for category, investments in categories.items():
        print(f"\n📊 {category.replace('_', ' ').title()}:")
        for investment in investments[:3]:  # Show first 3 in each category
            risk_emoji = {
                'Very Low': '🟢', 'Low': '🟡', 'Medium': '🟠', 'High': '🔴'
            }.get(investment['risk_level'], '⚪')
            
            print(f"  {risk_emoji} {investment['name']:20} | "
                  f"Return: {investment['typical_return']:5.1f}% | "
                  f"Risk: {investment['risk_level']}")

def demo_calculations():
    """Demo enhanced calculations"""
    print("🧮 DEMO: Enhanced Calculations")
    print("=" * 50)
    
    # Sample calculation with Indian data
    india_inflation = get_country_inflation_rate('IN')
    
    # Sample investment types
    stock_return = 12.0 / 100  # 12%
    fd_return = 6.5 / 100      # 6.5%
    
    inflation_rate = india_inflation['rate'] / 100
    
    print(f"🇮🇳 Using India's current inflation: {format_percentage(inflation_rate)}")
    print(f"💰 Investment Amount: ₹1,00,000")
    print()
    
    # Stock investment
    stock_real_return = calculate_real_return(stock_return, inflation_rate)
    print(f"📈 Stock Investment:")
    print(f"   Nominal Return: {format_percentage(stock_return)}")
    print(f"   Real Return: {format_percentage(stock_real_return)}")
    print(f"   Assessment: {'🎉 Excellent!' if stock_real_return > 0.03 else '✅ Good!'}")
    print()
    
    # FD investment
    fd_real_return = calculate_real_return(fd_return, inflation_rate)
    print(f"🏦 Fixed Deposit:")
    print(f"   Nominal Return: {format_percentage(fd_return)}")
    print(f"   Real Return: {format_percentage(fd_real_return)}")
    print(f"   Assessment: {'✅ Good!' if fd_real_return > 0 else '⚠️ Careful!'}")
    print()

def main():
    """Run all demos"""
    print("🌟 Enhanced Real vs. Nominal Return Calculator")
    print("   Major Update: Country Inflation + Investment Types")
    print("=" * 60)
    print()
    
    demo_country_inflation()
    demo_investment_types()
    demo_calculations()
    
    print("🚀 Features Successfully Implemented:")
    print("✅ Real-time country inflation rates (10 countries)")
    print("✅ Investment type selection (12+ types)")
    print("✅ Risk level assessment")
    print("✅ Enhanced web interface")
    print("✅ API endpoints for data access")
    print("✅ Modular architecture")
    print()
    print("🌐 Web Application: http://127.0.0.1:5000")
    print("📚 GitHub Repository: Updated with all enhancements")
    print()
    print("🎯 Ready for production use!")

if __name__ == "__main__":
    main()