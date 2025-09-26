"""
Data Provider Module
Handles country inflation rates and investment types data
"""

import requests
import json
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Investment types with typical return ranges (in percentage)
INVESTMENT_TYPES = {
    "stocks": {
        "name": "Stocks/Equity",
        "description": "Stock market investments",
        "typical_return": 12.0,
        "risk_level": "High",
        "category": "equity"
    },
    "mutual_funds_equity": {
        "name": "Equity Mutual Funds",
        "description": "Diversified equity mutual funds",
        "typical_return": 11.0,
        "risk_level": "High",
        "category": "mutual_funds"
    },
    "mutual_funds_hybrid": {
        "name": "Hybrid Mutual Funds",
        "description": "Balanced equity and debt funds",
        "typical_return": 9.0,
        "risk_level": "Medium",
        "category": "mutual_funds"
    },
    "mutual_funds_debt": {
        "name": "Debt Mutual Funds",
        "description": "Corporate bond and government securities",
        "typical_return": 7.0,
        "risk_level": "Low",
        "category": "mutual_funds"
    },
    "fixed_deposits": {
        "name": "Fixed Deposits (FD)",
        "description": "Bank fixed deposits",
        "typical_return": 6.5,
        "risk_level": "Very Low",
        "category": "fixed_income"
    },
    "ppf": {
        "name": "Public Provident Fund (PPF)",
        "description": "15-year tax-saving investment",
        "typical_return": 7.1,
        "risk_level": "Very Low",
        "category": "fixed_income"
    },
    "nsc": {
        "name": "National Savings Certificate (NSC)",
        "description": "5-year tax-saving investment",
        "typical_return": 6.8,
        "risk_level": "Very Low",
        "category": "fixed_income"
    },
    "elss": {
        "name": "ELSS (Tax Saving Funds)",
        "description": "Equity Linked Savings Scheme",
        "typical_return": 10.5,
        "risk_level": "High",
        "category": "tax_saving"
    },
    "gold": {
        "name": "Gold",
        "description": "Physical gold or gold ETFs",
        "typical_return": 8.0,
        "risk_level": "Medium",
        "category": "commodities"
    },
    "real_estate": {
        "name": "Real Estate",
        "description": "Property investments",
        "typical_return": 9.0,
        "risk_level": "Medium",
        "category": "real_estate"
    },
    "bonds": {
        "name": "Government Bonds",
        "description": "Government securities",
        "typical_return": 6.0,
        "risk_level": "Very Low",
        "category": "fixed_income"
    },
    "corporate_bonds": {
        "name": "Corporate Bonds",
        "description": "Corporate debt securities",
        "typical_return": 7.5,
        "risk_level": "Low",
        "category": "fixed_income"
    }
}

# Countries with their inflation data sources
COUNTRIES = {
    "IN": {
        "name": "India",
        "currency": "₹",
        "typical_inflation": 4.5,
        "flag": "🇮🇳"
    },
    "US": {
        "name": "United States",
        "currency": "$",
        "typical_inflation": 2.5,
        "flag": "🇺🇸"
    },
    "GB": {
        "name": "United Kingdom",
        "currency": "£",
        "typical_inflation": 2.0,
        "flag": "🇬🇧"
    },
    "JP": {
        "name": "Japan",
        "currency": "¥",
        "typical_inflation": 0.5,
        "flag": "🇯🇵"
    },
    "DE": {
        "name": "Germany",
        "currency": "€",
        "typical_inflation": 1.8,
        "flag": "🇩🇪"
    },
    "FR": {
        "name": "France",
        "currency": "€",
        "typical_inflation": 1.9,
        "flag": "🇫🇷"
    },
    "CA": {
        "name": "Canada",
        "currency": "C$",
        "typical_inflation": 2.2,
        "flag": "🇨🇦"
    },
    "AU": {
        "name": "Australia",
        "currency": "A$",
        "typical_inflation": 2.4,
        "flag": "🇦🇺"
    },
    "CN": {
        "name": "China",
        "currency": "¥",
        "typical_inflation": 2.8,
        "flag": "🇨🇳"
    },
    "BR": {
        "name": "Brazil",
        "currency": "R$",
        "typical_inflation": 4.0,
        "flag": "🇧🇷"
    }
}

def get_country_inflation_rate(country_code: str) -> Dict:
    """
    Get inflation rate for a specific country
    Falls back to typical inflation if API is unavailable
    
    Args:
        country_code (str): ISO country code (e.g., 'IN', 'US')
    
    Returns:
        dict: Inflation data with rate, source, and metadata
    """
    if country_code not in COUNTRIES:
        return {
            "rate": 3.0,
            "source": "default",
            "error": f"Country code {country_code} not supported"
        }
    
    country_info = COUNTRIES[country_code]
    
    try:
        # Try to get real-time data from World Bank API
        # Note: This is a simplified implementation. In production, you might want to use
        # paid APIs like FRED (Federal Reserve Economic Data) or Trading Economics
        
        # For demo purposes, we'll use the World Bank API with some sample logic
        # In a real implementation, you'd parse the actual API response
        
        # Simulating API call with typical values + some variation
        import random
        base_rate = country_info["typical_inflation"]
        # Add some realistic variation (-1% to +1%)
        variation = random.uniform(-1.0, 1.0)
        current_rate = max(0, base_rate + variation)
        
        return {
            "rate": round(current_rate, 2),
            "source": "api_simulation",
            "country": country_info["name"],
            "currency": country_info["currency"],
            "flag": country_info["flag"],
            "last_updated": "2024-01-01",  # In production, use actual timestamp
            "success": True
        }
        
    except Exception as e:
        logger.warning(f"Failed to get real-time inflation for {country_code}: {e}")
        # Fallback to typical inflation rate
        return {
            "rate": country_info["typical_inflation"],
            "source": "fallback",
            "country": country_info["name"],
            "currency": country_info["currency"],
            "flag": country_info["flag"],
            "last_updated": "fallback",
            "success": True,
            "note": "Using typical inflation rate (API unavailable)"
        }

def get_all_countries() -> Dict:
    """Get all supported countries"""
    return COUNTRIES

def get_investment_types() -> Dict:
    """Get all investment types"""
    return INVESTMENT_TYPES

def get_investment_type_return(investment_type: str) -> float:
    """
    Get typical return rate for an investment type
    
    Args:
        investment_type (str): Investment type key
        
    Returns:
        float: Return rate as decimal (e.g., 0.12 for 12%)
    """
    if investment_type in INVESTMENT_TYPES:
        return INVESTMENT_TYPES[investment_type]["typical_return"] / 100
    return 0.08  # Default 8% return

def get_investment_categories() -> Dict:
    """Get investment types grouped by category"""
    categories = {}
    for key, investment in INVESTMENT_TYPES.items():
        category = investment["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append({
            "key": key,
            "name": investment["name"],
            "description": investment["description"],
            "typical_return": investment["typical_return"],
            "risk_level": investment["risk_level"]
        })
    return categories

# Future enhancement: Real API integration
def fetch_real_time_inflation(country_code: str) -> Optional[float]:
    """
    Fetch real-time inflation data from external APIs
    This is a placeholder for future enhancement
    
    APIs to consider:
    - World Bank API (free but limited)
    - FRED API (Federal Reserve Economic Data)
    - Trading Economics API
    - OECD API
    """
    # Placeholder for real API integration
    try:
        # Example: World Bank API call
        # url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/FP.CPI.TOTL.ZG"
        # response = requests.get(url, params={"format": "json", "date": "2023:2024"})
        # ... parse response
        pass
    except Exception as e:
        logger.error(f"Failed to fetch real-time inflation: {e}")
        return None
    
    return None