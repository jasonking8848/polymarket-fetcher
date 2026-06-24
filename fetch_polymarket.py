"""Polymarket World Cup data fetcher."""
import requests
import json
import os
from datetime import datetime

API = "https://gamma-api.polymarket.com"
OUT_DIR = "data"

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Fetch ALL open markets
    all_markets = []
    for limit in [500]:
        try:
            resp = requests.get(f"{API}/markets", params={"limit": limit, "closed": "false"}, timeout=30)
            data = resp.json()
            all_markets.extend(data)
            print(f"Fetched {len(data)} markets")
        except Exception as e:
            print(f"Fetch error: {e}")
    
    if not all_markets:
        # Fallback: try events endpoint
        try:
            resp = requests.get(f"{API}/events", params={"limit": 100}, timeout=30)
            events = resp.json()
            print(f"Events: {len(events)}")
            # Save events too
            with open(os.path.join(OUT_DIR, f"events_{timestamp}.json"), "w") as f:
                json.dump(events, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Events error: {e}")
    
    # Save all markets
    output = {
        "fetched_at": timestamp,
        "total": len(all_markets),
        "markets": all_markets
    }
    with open(os.path.join(OUT_DIR, "polymarket_latest.json"), "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # Also save timestamped version
    with open(os.path.join(OUT_DIR, f"polymarket_{timestamp}.json"), "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(all_markets)} markets to data/")

if __name__ == "__main__":
    main()
