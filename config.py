# scraper header
HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/149.0.0.0 Safari/537.36",
    "accept": "application/json",
    "x-requested-with": "XMLHttpRequest",
    "referer": "https://www.starbucks.com/store-locator",
}

API_URL = "https://www.starbucks.com/apiproxy/v1/locations"

# file name
INPUT_COORDS = "data/postal-codes-canada.csv"
GEOJSON = "data/canada.geojson"

STORES_CSV = "output/starbucks_Canada_final.csv"
MAP_HTML = "output/Canada_map.html"
HIST_PNG = "output/CAclosest_dist_hist.png"

# cities coordinates

MEGA_CITIES = [
    (43.6532, -79.3832),   # Toronto
    (49.2827, -123.1207),  # Vancouver
    (51.0447, -114.0719),  # Calgary
    (53.5461, -113.4938),  # Edmonton
]

BIG_CITIES = [
    (45.5019, -73.5674),   # Montreal
    (45.4215, -75.6972),   # Ottawa
    (43.2557, -79.8711),   # Hamilton
    (48.4284, -123.3656),  # Victoria
    (49.8951, -97.1384),   # Winnipeg
    (44.6488, -63.5752),   # Halifax
    (43.4516, -80.4925),   # Kitchener-Waterloo
    (42.9849, -81.2453),   # London ON
    (43.5890, -79.6441),   # Mississauga
    (50.4452, -104.6189),  # Regina
    (52.1332, -106.6700),  # Saskatoon
]


STADIA_KEY = "9f6672f0-ce1f-4ca2-99be-9ac2e4042ce4" 