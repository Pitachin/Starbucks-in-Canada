import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree
import geopy.distance
import config
from record_time import timer

# Since it is great-circle distance, we use Haversine Formula. And balltree

EARTH_RADIUS_M = 6_371_000

@timer
def compute_distances(df):
    """Find each store's nearest neighbor and the distance to it (meters)."""

    # Haversine requires coordinates in radians
    coors = np.radians(df[["latitude", "longitude"]].values)

    tree = BallTree(coors, metric="haversine")

    dists, indices = tree.query(coors, k=2) # since the closest is itself, we choose k = 2.
    
    closest_dists = dists[:, 1] * EARTH_RADIUS_M
    closest_locs = indices[:, 1]
    return closest_locs, closest_dists

@timer
def compute_distances_2(df):
    """O(n²) double loop + geodesic"""
    locs = list(zip(df["latitude"], df["longitude"]))
    n = len(locs)
    dist_matrix = np.full((n, n), np.inf)
    for i1, s1 in enumerate(locs):
        for i2, s2 in enumerate(locs):
            if i1 < i2:
                d = geopy.distance.geodesic(s1, s2).m
                dist_matrix[i1, i2] = d
                dist_matrix[i2, i1] = d
    return dist_matrix.min(axis=1)


def load_stores():
    """Load all Canada stores from CSV."""
    df = pd.read_csv(config.STORES_CSV)
    df = df.reset_index(drop=True)
    return df

if __name__ == '__main__':
    df = load_stores()
    closest_locs, closest_dists = compute_distances(df)
    print(f"Average nearest-neighbor distance: {closest_dists.mean():.0f} m")
    print(f"Closest: {closest_dists.min():.0f} m, "
          f"Farthest: {closest_dists.max() / 1000:.1f} km")
    
    """

    Time Test

    # Method 1
    nearest_neighbors_bruteforce = compute_distances_2
    closest_dists = nearest_neighbors_bruteforce(df)
    print(f"Average nearest-neighbor distance: {closest_dists.mean():.0f} m")
    print(f"Closest: {closest_dists.min():.0f} m, "
          f"Farthest: {closest_dists.max() / 1000:.1f} km")

    print('='*50)

    # Method 2
    nearest_neighbors_balltree = compute_distances
    closest_locs, closest_dists = nearest_neighbors_balltree(df)
    print(f"Average nearest-neighbor distance: {closest_dists.mean():.0f} m")
    print(f"Closest: {closest_dists.min():.0f} m, "
          f"Farthest: {closest_dists.max() / 1000:.1f} km")

    """