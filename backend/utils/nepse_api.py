"""NEPSE stock price fetcher"""
import requests
import logging
import json

logger = logging.getLogger(__name__)

# NEPSE stock symbols list
NEPSE_STOCKS = [
    {"symbol": "ADBL", "name": "Agricultural Development Bank Ltd"},
    {"symbol": "BOKL", "name": "Bank of Kathmandu Ltd"},
    {"symbol": "CHCL", "name": "Chilime Hydropower Co. Ltd"},
    {"symbol": "CZBIL", "name": "Citizen Bank International Ltd"},
    {"symbol": "EBL", "name": "Everest Bank Ltd"},
    {"symbol": "GBIME", "name": "Global IME Bank Ltd"},
    {"symbol": "HBL", "name": "Himalayan Bank Ltd"},
    {"symbol": "HIDCL", "name": "Hydroelectricity Investment & Development Company Ltd"},
    {"symbol": "HNBBL", "name": "Hamro Bikas Bank Ltd"},
    {"symbol": "IFL", "name": "Infrastructure Development Bank Ltd"},
    {"symbol": "JBNL", "name": "Janata Bank Nepal Ltd"},
    {"symbol": "KBL", "name": "Kumari Bank Ltd"},
    {"symbol": "LICN", "name": "Life Insurance Corporation Nepal Ltd"},
    {"symbol": "LBBL", "name": "Lumbini Bikas Bank Ltd"},
    {"symbol": "MBL", "name": "Machhapuchchhre Bank Ltd"},
    {"symbol": "MEGA", "name": "Mega Bank Nepal Ltd"},
    {"symbol": "MLBBL", "name": "Muktinath Bikas Bank Ltd"},
    {"symbol": "NBB", "name": "Nepal Bank Ltd"},
    {"symbol": "NBL", "name": "Nepal Bangladesh Bank Ltd"},
    {"symbol": "NABIL", "name": "Nabil Bank Ltd"},
    {"symbol": "NCC", "name": "Nepal Credit And Commerce Bank Ltd"},
    {"symbol": "NCHL", "name": "Nepal Clearing House Ltd"},
    {"symbol": "NIFRA", "name": "Nepal Infrastructure Bank Ltd"},
    {"symbol": "NIL", "name": "Nepal Insurance Company Ltd"},
    {"symbol": "NLG", "name": "Nepal Life Insurance Company Ltd"},
    {"symbol": "NICA", "name": "NIC Asia Bank Ltd"},
    {"symbol": "NICL", "name": "National Insurance Company Ltd"},
    {"symbol": "NIBL", "name": "Nepal Investment Bank Ltd"},
    {"symbol": "NMB", "name": "NMB Bank Ltd"},
    {"symbol": "NMFBS", "name": "NMB Microfinance Bittiya Sanstha Ltd"},
    {"symbol": "NPCL", "name": "National Power Company Ltd"},
    {"symbol": "NRIC", "name": "Nepal Reinsurance Company Ltd"},
    {"symbol": "NSB", "name": "Nepal SBI Bank Ltd"},
    {"symbol": "NWCFL", "name": "Nepal Water & Energy Development Co. Ltd"},
    {"symbol": "PCBL", "name": "Prime Commercial Bank Ltd"},
    {"symbol": "PHCL", "name": "Pokhara Finance Ltd"},
    {"symbol": "PROFL", "name": "Progressive Finance Ltd"},
    {"symbol": "PRVU", "name": "Prabhu Bank Ltd"},
    {"symbol": "RBBI", "name": "Rastriya Banijya Bank"},
    {"symbol": "RBCL", "name": "Reliance Finance Ltd"},
    {"symbol": "RMDC", "name": "Rural Microfinance Development Centre Ltd"},
    {"symbol": "SABL", "name": "Sanima Bank Ltd"},
    {"symbol": "SBBLJ", "name": "Sindhu Bikas Bank Ltd"},
    {"symbol": "SBIBD", "name": "SBI BD FUND"},
    {"symbol": "SCBL", "name": "Standard Chartered Bank Nepal Ltd"},
    {"symbol": "SEBON", "name": "Securities Board Nepal"},
    {"symbol": "SFCL", "name": "Siddhartha Finance Ltd"},
    {"symbol": "SHL", "name": "Soaltee Hotel Ltd"},
    {"symbol": "SIBL", "name": "Siddhartha Bank Ltd"},
    {"symbol": "SLBS", "name": "Sunrise First Mutual Fund"},
    {"symbol": "SLICL", "name": "Surya Life Insurance Company Ltd"},
    {"symbol": "SMATA", "name": "Swabhiman Laghubitta Bittiya Sanstha Ltd"},
    {"symbol": "SMFBS", "name": "Saptakoshi Development Bank Ltd"},
    {"symbol": "STC", "name": "Salt Trading Corporation Ltd"},
    {"symbol": "SUNSL", "name": "Sunrise Bank Ltd"},
    {"symbol": "TRH", "name": "Taragaon Regency Hotels Ltd"},
    {"symbol": "UAIL", "name": "United Ajod Insurance Ltd"},
    {"symbol": "UCBL", "name": "United Commercial Bank Ltd"},
    {"symbol": "UFL", "name": "United Finance Ltd"},
]

def get_stock_price(symbol):
    """Attempt to fetch current NEPSE stock price"""
    try:
        # Try nepse.com API
        url = f"https://www.nepalipaisa.com/api/stocks/{symbol}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('lastTradedPrice', 0)
    except:
        pass
    return None

def get_all_stocks():
    """Return list of all NEPSE stocks"""
    return NEPSE_STOCKS

def get_stock_list_for_dropdown():
    """Return formatted list for dropdown"""
    return [{"value": s["symbol"], "label": f"{s['symbol']} - {s['name']}"} for s in NEPSE_STOCKS]
