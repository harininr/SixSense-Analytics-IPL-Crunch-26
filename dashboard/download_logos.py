import os, requests, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
LOGOS_DIR = os.path.join(HERE, "logos")
os.makedirs(LOGOS_DIR, exist_ok=True)

LOGO_URLS = {
    "CSK":  "https://upload.wikimedia.org/wikipedia/en/thumb/2/2b/Chennai_Super_Kings_Logo.svg/250px-Chennai_Super_Kings_Logo.svg.png",
    "MI":   "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Mumbai_Indians_Logo.svg/250px-Mumbai_Indians_Logo.svg.png",
    "KKR":  "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Kolkata_Knight_Riders_Logo.svg/250px-Kolkata_Knight_Riders_Logo.svg.png",
    "RCB":  "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Royal_Challengers_Bengaluru_Logo.svg/250px-Royal_Challengers_Bengaluru_Logo.svg.png",
    "SRH":  "https://upload.wikimedia.org/wikipedia/en/thumb/5/51/Sunrisers_Hyderabad_Logo.svg/250px-Sunrisers_Hyderabad_Logo.svg.png",
    "DC":   "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Delhi_Capitals.svg/250px-Delhi_Capitals.svg.png",
    "RR":   "https://upload.wikimedia.org/wikipedia/en/thumb/5/5c/This_is_the_logo_for_Rajasthan_Royals%2C_a_cricket_team_playing_in_the_Indian_Premier_League_%28IPL%29.svg/250px-This_is_the_logo_for_Rajasthan_Royals%2C_a_cricket_team_playing_in_the_Indian_Premier_League_%28IPL%29.svg.png",
    "PBKS": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Punjab_Kings_Logo.svg/250px-Punjab_Kings_Logo.svg.png",
    "GT":   "https://upload.wikimedia.org/wikipedia/en/thumb/0/09/Gujarat_Titans_Logo.svg/250px-Gujarat_Titans_Logo.svg.png",
    "LSG":  "https://upload.wikimedia.org/wikipedia/en/thumb/3/34/Lucknow_Super_Giants_Logo.svg/250px-Lucknow_Super_Giants_Logo.svg.png",
}

HDR = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
}

ok, fail = 0, 0
for team, url in LOGO_URLS.items():
    path = os.path.join(LOGOS_DIR, f"{team}.png")
    # If the file already exists and is non-empty, skip it to save requests
    if os.path.exists(path) and os.path.getsize(path) > 500:
        print(f"  ⏭️  {team}  (already downloaded)")
        ok += 1
        continue
    try:
        r = requests.get(url, headers=HDR, timeout=15)
        if r.status_code == 200 and len(r.content) > 500:
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"  ✅  {team}  ({len(r.content)//1024}KB)")
            ok += 1
        else:
            print(f"  ❌  {team}  HTTP {r.status_code}")
            fail += 1
        time.sleep(2.0)
    except Exception as e:
        print(f"  ❌  {team}  {e}")
        fail += 1
        time.sleep(2.0)

print(f"\n{ok} downloaded/available, {fail} failed → {LOGOS_DIR}")
