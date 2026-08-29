import sys
import os
import json
from collections import OrderedDict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import LineString, mapping
from shapely.ops import transform
import pyproj

from app.db.database import SessionLocal
from app.models.road import RoadSegment

# Function to convert Shapely geometry to length in meters
def compute_length_meters(geom):
    # GeoJSON is in EPSG:4326 (lat/lon); we need a projection for meters.
    # Use a local UTM projection (zone 46N for Assam/Meghalaya region)
    transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32646", always_xy=True)
    geom_proj = transform(transformer.transform, geom)
    return geom_proj.length

def main(geojson_path):
    with open(geojson_path, 'r') as f:
        data = json.load(f)

    features = data.get('features', [])
    print(f"Found {len(features)} features in GeoJSON.")

    # First pass: collect all unique endpoints (first and last coordinate) to assign node IDs
    node_id_map = OrderedDict()
    next_node_id = 1

    def get_node_id(coord):
        nonlocal next_node_id
        # Round coordinates to avoid floating point mismatch
        key = (round(coord[0], 6), round(coord[1], 6))
        if key not in node_id_map:
            node_id_map[key] = next_node_id
            next_node_id += 1
        return node_id_map[key]

    # Prepare list to store segments
    segments_to_insert = []

    for feature in features:
        geom = feature.get('geometry')
        if geom is None or geom['type'] != 'LineString':
            continue

        coords = geom['coordinates']
        if len(coords) < 2:
            continue

        # Extract properties
        props = feature.get('properties', {})
        osm_id = props.get('@id') or props.get('osm_id') or str(abs(hash(str(coords))))[:10]
        name = props.get('name', None)
        highway = props.get('highway', 'unclassified')

        # Get node IDs for start and end
        start_coord = coords[0]
        end_coord = coords[-1]
        from_node = get_node_id(start_coord)
        to_node = get_node_id(end_coord)

        # Create Shapely LineString
        line = LineString(coords)
        # Compute length in meters
        length_m = compute_length_meters(line)

        segments_to_insert.append({
            'osm_id': str(osm_id),
            'name': name,
            'road_type': highway,
            'length_m': length_m,
            'slope': 0.0,
            'elevation': 0.0,
            'from_node': from_node,
            'to_node': to_node,
            'geometry': line
        })

    print(f"Prepared {len(segments_to_insert)} road segments.")
    print(f"Assigned {len(node_id_map)} unique nodes.")

    # Insert into database
    db = SessionLocal()
    try:
        count = 0
        for seg in segments_to_insert:
            road = RoadSegment(
                osm_id=seg['osm_id'],
                name=seg['name'],
                road_type=seg['road_type'],
                length_m=seg['length_m'],
                slope=seg['slope'],
                elevation=seg['elevation'],
                from_node=seg['from_node'],
                to_node=seg['to_node'],
                geometry=from_shape(seg['geometry'], srid=4326)
            )
            db.add(road)
            count += 1
            if count % 100 == 0:
                print(f"Inserted {count} segments...")
        db.commit()
        print(f"Successfully inserted {count} road segments into the database.")
    except Exception as e:
        db.rollback()
        print(f"Error during insertion: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/load_geojson_roads.py <path_to_geojson_file>")
        sys.exit(1)
    path = sys.argv[1]
    main(path)