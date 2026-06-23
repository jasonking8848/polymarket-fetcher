"""Polymarket World Cup data fetcher. Runs in GitHub Actions (US IP)."""
import requests
import json
import os
from datetime import datetime

API = "https://gamma-api.polymarket.com"
OUT_DIR = "data"

def fetch_markets(tag, limit=50):
    """Fetch markets by tag."""
    url = f"{API}/markets"
    params = {"tag": tag, "limit": limit, "closed": "false"}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def fetch_events(tag, limit=20):
    """Fetch events by tag."""
    url = f"{API}/events"
    params = {"tag": tag, "limit": limit}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    all_data = []
    
    # Try multiple tags for World Cup
    for tag in ["world-cup", "world-cup-2026", "soccer", "football", "sports"]:
        try:
            # Fetch markets
            markets = fetch_markets(tag, limit=100)
            # Filter for soccer/football/world-cup
            football_markets = []
            for m in markets:
                q = (m.get("question", "") + m.get("description", "")).lower()
                tags_str = str(m.get("tags", [])).lower()
                if any(kw in q or kw in tags_str for kw in [
                    "world cup", "worldcup", "soccer", "football",
                    "portugal", "england", "france", "brazil", "argentina",
                    "germany", "spain", "netherlands", "morocco"
                ]):
                    football_markets.append({
                        "id": m.get("id"),
                        "question": m.get("question"),
                        "volume": m.get("volume"),
                        "liquidity": m.get("liquidity"),
                        "outcomes": m.get("outcomes"),
                        "outcomePrices": m.get("outcomePrices"),
                        "closed": m.get("closed"),
                        "endDate": m.get("endDate"),
                        "tags": m.get("tags", []),
                    })
            
            if football_markets:
                print(f"Tag '{tag}': {len(football_markets)} football markets")
                all_data.extend(football_markets)
            
        except Exception as e:
            print(f"Tag '{tag}': {e}")
    
    # Save to file
    output = {
        "fetched_at": timestamp,
        "total_markets": len(all_data),
        "markets": all_data,
    }
    
    out_file = os.path.join(OUT_DIR, f"polymarket_{timestamp}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # Also save latest snapshot
    latest_file = os.path.join(OUT_DIR, "polymarket_latest.json")
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(all_data)} markets to {out_file}")

if __name__ == "__main__":
    main()
