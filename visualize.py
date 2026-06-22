# Build the Folium map (points + nearest-neighbor lines) and the distance histogram
import numpy as np
import json
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import config
from record_time import timer
from distance import load_stores, compute_distances

@timer
def make_map(df, closest_locs, closest_dists):
    locs = list(zip(df["latitude"], df["longitude"]))

    # Load Canada boundary
    with open(config.GEOJSON) as f:
        on_area = json.load(f)

    # Initialize the map centered on Ontario (Stamen Toner tiles via Stadia)
    m = folium.Map(
        location=[44.5, -79.5], zoom_start=9,
        tiles=f"https://tiles.stadiamaps.com/tiles/stamen_toner/{{z}}/{{x}}/{{y}}{{r}}.png?api_key={config.STADIA_KEY}",
        attr="© Stadia Maps © Stamen Design © OpenStreetMap",
    )
    folium.GeoJson(on_area).add_to(m)

    # Plot every store as a point
    for lat, lng in locs:
        folium.CircleMarker((lat, lng), radius=4, weight=2,
                            color="red", fill_color="green", fill_opacity=.5).add_to(m)

    # Find the closest pair and the most isolated store
    min_idx, max_idx = np.argmin(closest_dists), np.argmax(closest_dists)
    nearest_of_min = closest_locs[min_idx]

    # Draw a line from each store to its nearest neighbor
    for i1, s1 in enumerate(locs):
        s2 = locs[closest_locs[i1]]
        d = round(closest_dists[i1], 0)
        if i1 == min_idx:                       # closest pair -> orange
            folium.PolyLine([s1, s2], color="orange", weight=5,
                            popup=f"Closest: {d} m").add_to(m)
        elif i1 == max_idx:                     # most isolated store -> blue
            folium.PolyLine([s1, s2], color="blue", weight=5,
                            popup=f"Farthest: {d/1000:.1f} km").add_to(m)
        else:
            folium.PolyLine([s1, s2], color="black", weight=2,
                            popup=f"{d} m").add_to(m)

    # Highlight the closest pair with bigger orange markers
    for idx in [min_idx, nearest_of_min]:
        lat, lng = locs[idx]
        folium.CircleMarker((lat, lng), radius=8, weight=3,
                            color="orange", fill_color="orange", fill_opacity=.9,
                            popup=f"{df.iloc[idx]['name']}").add_to(m)

    m.save(config.MAP_HTML)
    print(f"Map saved: {config.MAP_HTML}")


def make_histogram(closest_dists):
    # Histogram of nearest-neighbor distances (zoom in on stores within 5 km)
    plt.figure(figsize=(12, 5))
    data_main = closest_dists[closest_dists <= 5000]
    sns.histplot(data_main, kde=True, line_kws={"linewidth": 3}, stat="density", bins=40)
    plt.xlabel("Meters to closest Starbucks (within 5km)", fontsize=16)
    plt.ylabel("Density", fontsize=16)
    # Use median instead of mean (the long tail skews the mean)
    plt.axvline(np.median(closest_dists), color="k", linestyle="--", linewidth=2.5,
                label=f"Median: {np.median(closest_dists):.0f} m")
    plt.legend(fontsize=14)
    plt.savefig(config.HIST_PNG, bbox_inches="tight")
    plt.show()

def main():
    df = load_stores()
    closest_locs, closest_dists = compute_distances(df)
    make_map(df, closest_locs, closest_dists)
    make_histogram(closest_dists)


if __name__ == "__main__":
    main()