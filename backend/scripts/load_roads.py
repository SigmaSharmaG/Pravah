import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
import osmnx as ox

import osmnx as ox

# Use the official, high-capacity private.coffee mirror
# Note: Ensure NO trailing slash at the end of the URL string
ox.settings.overpass_url = "https://overpass.private.coffee/api"

# Configure the request timeout window to prevent early dropouts
ox.settings.timeout = 300

# Provide a structured user agent identity to prevent bot bans
ox.settings.user_agent = "PravahLogisticsEngine/1.0 (harsh@BugCoder)"

# Disable rate limit pings to bypass proxy checks
ox.settings.overpass_rate_limit = False




import geopandas as gpd
from geoalchemy2.shape import from_shape

from app.db.database import SessionLocal
from app.models.road import RoadSegment

def main():
    # Define bounding box for Guwahati–Shillong corridor
    north = 26.3
    south = 25.4
    east = 92.1
    west = 91.5

    print("Downloading road network from OpenStreetMap...")
    # Download only major roads to keep data small
    G = ox.graph_from_bbox(
        bbox=(north, south, east, west),
        network_type='drive',
        custom_filter='["highway"~"motorway|trunk|primary|secondary|tertiary"]'
    )
    print(f"Downloaded graph with {len(G.nodes)} nodes and {len(G.edges)} edges")

    # Convert to GeoDataFrames (nodes and edges)
    nodes, edges = ox.graph_to_gdfs(G)
    print(f"Edges GeoDataFrame has {len(edges)} rows")

    # Open a database session
    db = SessionLocal()
    try:
        count = 0
        # Iterate over each edge (road segment)
        for idx, row in edges.iterrows():
            u, v, key = idx  # from_node, to_node, edge key

            # Extract geometry as a Shapely LineString
            geom = row['geometry']

            # Create a RoadSegment record
            segment = RoadSegment(
                osm_id=str(row.get('osmid', '')),   # OSM way ID (non‑unique)
                name=row.get('name', None),
                road_type=row.get('highway', 'unclassified'),
                length_m=float(row['length']),
                slope=0.0,        # we'll compute later if needed
                elevation=0.0,
                from_node=u,
                to_node=v,
                geometry=from_shape(geom, srid=4326)  # convert Shapely geom to WKB
            )
            db.add(segment)
            count += 1
            if count % 100 == 0:
                print(f"Added {count} segments...")

        db.commit()
        print(f"Successfully inserted {count} road segments into the database.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()