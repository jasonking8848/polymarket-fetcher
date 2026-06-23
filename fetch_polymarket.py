"""Polymarket World Cup data fetcher. Runs in GitHub Actions (US IP)."""
import requests
import json
import os
from datetime import datetime

API = "https://gamma-api.polymarket.com"
OUT_DIR = "data"

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    all_data = []
    
    # Try fetching all markets without tag filter, then filter client-side
    url = API + "/markets"
    params = {"limit": 200, "closed": "false"}
    resp = requests.get(url, params=params, timeout=30)
    markets = resp.json()
    
    for m in markets:
        q = str(m.get("question", "")).lower()
        if any(kw in q for kw in ["world cup", "worldcup", "world-cup",
            "world cup 2026", "fifa", "soccer", "football"]):
            all_data.append({
                "id": m.get("id"),
                "question": m.get("question"),
                "volume": m.get("volume"),
                "liquidity": m.get("liquidity"),
                "outcomes": m.get("outcomes"),
                "outcomePrices": m.get("outcomePrices"),
                "closed": m.get("closed"),
            })
    
    # Also save ALL markets for debugging
    output = {"fetched_at": timestamp, "total_markets": len(all_data), "markets": all_data}
    with open(os.path.join(OUT_DIR, "polymarket_latest.json"), "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # Also dump raw count for debugging
    print("Total Polymarket markets:", len(markets))
    print("Football markets found:", len(all_data))

if __name__ == "__main__":
    main()
