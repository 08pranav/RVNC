#!/usr/bin/env python3
"""
Real vs. Nominal Return Calculator - Quick Examples
Demonstrates various financial scenarios
"""

from calculator import calculate_real_return, format_percentage

def show_examples():
    """Display various real-world investment scenarios"""
    print("=" * 80)
    print("    REAL vs. NOMINAL RETURN CALCULATOR - EXAMPLES")
    print("=" * 80)
    print("Understanding how inflation affects your investment returns")
    print("Formula: Real Return = ((1 + Nominal) ÷ (1 + Inflation)) - 1")
    print("=" * 80)
    
    scenarios = [
        {
            'name': '📈 S&P 500 Stock Index (Historical Average)',
            'description': 'Long-term stock market performance vs typical inflation',
            'nominal': 0.10,  # 10%
            'inflation': 0.03,  # 3%
            'explanation': 'Historically, the S&P 500 has averaged ~10% nominal returns'
        },
        {
            'name': '🏛️ Government Treasury Bonds',
            'description': 'Conservative government bonds during low inflation',
            'nominal': 0.04,  # 4%
            'inflation': 0.02,  # 2%
            'explanation': 'Safe government bonds typically offer lower but stable returns'
        },
        {
            'name': '🏠 Real Estate Investment',
            'description': 'Real estate investment in growing market',
            'nominal': 0.07,  # 7%
            'inflation': 0.035,  # 3.5%
            'explanation': 'Real estate often provides inflation hedge but varies by location'
        },
        {
            'name': '💰 High-Yield Savings Account',
            'description': 'Bank savings account during moderate inflation',
            'nominal': 0.015,  # 1.5%
            'inflation': 0.04,  # 4%
            'explanation': 'Savings accounts often lose purchasing power during inflation'
        },
        {
            'name': '🚀 Growth Tech Stock',
            'description': 'High-growth technology stock',
            'nominal': 0.15,  # 15%
            'inflation': 0.03,  # 3%
            'explanation': 'Growth stocks can provide excellent real returns but with higher risk'
        },
        {
            'name': '⚠️ 1970s High Inflation Period',
            'description': 'Investment during high inflation era',
            'nominal': 0.08,  # 8%
            'inflation': 0.10,  # 10%
            'explanation': 'High inflation periods can erode investment returns significantly'
        },
        {
            'name': '💎 Commodities (Gold)',
            'description': 'Gold investment as inflation hedge',
            'nominal': 0.06,  # 6%
            'inflation': 0.05,  # 5%
            'explanation': 'Commodities like gold are often bought as inflation protection'
        },
        {
            'name': '🌍 Emerging Market Stock',
            'description': 'Emerging market with higher inflation',
            'nominal': 0.12,  # 12%
            'inflation': 0.07,  # 7%
            'explanation': 'Emerging markets often have higher returns but also higher inflation'
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print("-" * 60)
        print(f"Scenario: {scenario['description']}")
        print(f"Context: {scenario['explanation']}")
        
        real_return = calculate_real_return(scenario['nominal'], scenario['inflation'])
        
        print(f"\n📊 Financial Analysis:")
        print(f"   Nominal Return:  {format_percentage(scenario['nominal'], 2)}")
        print(f"   Inflation Rate:  {format_percentage(scenario['inflation'], 2)}")
        print(f"   Real Return:     {format_percentage(real_return, 2)}")
        
        # Calculate the difference
        difference = real_return
        if difference > 0.05:  # > 5%
            status = "🎉 EXCELLENT - Strong real growth!"
            color = "green"
        elif difference > 0.02:  # > 2%
            status = "✅ GOOD - Beats inflation well"
            color = "blue"
        elif difference > 0:  # > 0%
            status = "⚠️ MODEST - Barely beats inflation"
            color = "yellow"
        else:  # <= 0%
            status = "❌ POOR - Loses purchasing power"
            color = "red"
        
        print(f"   Assessment:      {status}")
        
        # Show purchasing power impact over 10 years on $10,000
        initial = 10000
        years = 10
        nominal_value = initial * ((1 + scenario['nominal']) ** years)
        real_value = initial * ((1 + real_return) ** years)
        
        print(f"\n💡 10-Year Impact on $10,000 investment:")
        print(f"   Nominal Value:   ${nominal_value:,.0f}")
        print(f"   Real Value:      ${real_value:,.0f} (in today's purchasing power)")
        print(f"   Inflation Cost:  ${nominal_value - real_value:,.0f}")
        
        if i < len(scenarios):
            print("\n" + "="*80)
    
    print(f"\n🎓 KEY LEARNING POINTS:")
    print("-" * 30)
    print("• Nominal returns don't tell the whole story")
    print("• Inflation can significantly erode investment gains")
    print("• Real returns show true purchasing power growth")
    print("• Diversification across asset classes is important")
    print("• Higher nominal returns often come with higher risks")
    print("• Even 'safe' investments can lose to inflation")
    
    print(f"\n💭 REMEMBER:")
    print("The formula Real Return = ((1 + Nominal) ÷ (1 + Inflation)) - 1")
    print("helps you understand what your investments are REALLY earning!")
    
    print("=" * 80)

if __name__ == "__main__":
    show_examples()