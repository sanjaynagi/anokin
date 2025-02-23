from qgis.core import *
from random import uniform, seed
import math


# First, make sure we have the correct layer
input_layer = iface.activeLayer()
if not input_layer:
    print("No active layer selected! Please select a layer in the Layers panel.")
    exit()

print(f"Using layer: {input_layer.name()}")
print(f"Layer CRS: {input_layer.crs().authid()}")

def calculate_distance(point1, point2, crs):
    """Calculate the distance between points respecting the CRS"""
    # Create a distance calculator for the layer's CRS
    distance_calc = QgsDistanceArea()
    distance_calc.setSourceCrs(crs, QgsProject.instance().transformContext())
    distance_calc.setEllipsoid(crs.ellipsoidAcronym())
    
    # Calculate distance in layer units (usually meters)
    distance = distance_calc.measureLine(point1, point2)
    return distance

def generate_two_points_per_segment(layer, min_distance, max_distance):
    all_points = []
    layer_crs = layer.crs()
    
    # Get all polygon geometries
    polygon_geoms = []
    for feat in layer.getFeatures():
        if feat.geometry().isMultipart():
            for part in feat.geometry().asMultiPolygon():
                geom = QgsGeometry.fromPolygonXY(part)
                polygon_geoms.append(geom)
        else:
            geom = feat.geometry()
            polygon_geoms.append(geom)
    
    print(f"Found {len(polygon_geoms)} polygon parts")
    print(f"Using CRS: {layer_crs.authid()}")
    print(f"Distance constraints: min={min_distance}m, max={max_distance}m")
    
    # Generate points for each polygon
    for i, geom in enumerate(polygon_geoms):
        print(f"\nProcessing segment {i+1}")
        extent = geom.boundingBox()
        attempts = 0
        max_attempts = 1000
        first_point = None
        second_point = None
        
        # Generate first point
        while first_point is None and attempts < max_attempts:
            x = uniform(extent.xMinimum(), extent.xMaximum())
            y = uniform(extent.yMinimum(), extent.yMaximum())
            point = QgsPointXY(x, y)
            point_geom = QgsGeometry.fromPointXY(point)
            
            if geom.contains(point_geom):
                first_point = point
                print(f"First point generated in segment {i+1}")
            attempts += 1
        
        # Generate second point
        while second_point is None and attempts < max_attempts:
            x = uniform(extent.xMinimum(), extent.xMaximum())
            y = uniform(extent.yMinimum(), extent.yMaximum())
            point = QgsPointXY(x, y)
            point_geom = QgsGeometry.fromPointXY(point)
            
            if geom.contains(point_geom):
                distance = calculate_distance(first_point, point, layer_crs)
                if min_distance <= distance <= max_distance:  # Check both min and max
                    second_point = point
                    print(f"Second point generated in segment {i+1}")
                    print(f"Distance between points: {distance:.2f}m")
            attempts += 1
            
        if first_point and second_point:
            all_points.extend([first_point, second_point])
            print(f"Successfully generated 2 points for segment {i+1}")
        else:
            print(f"Warning: Could not generate valid points for segment {i+1} after {attempts} attempts")
            print(f"This might be because the segment is too small for the distance constraints")
            
    print(f"\nTotal points generated: {len(all_points)}")
    return all_points


# Set random seed for reproducibility
RANDOM_SEED = 88
seed(RANDOM_SEED)

# Parameters
min_distance = 400    # Minimum distance between points (in meters)
max_distance = 600    # Maximum distance between points (in meters)

# Validate distance parameters
if min_distance >= max_distance:
    print("Error: minimum distance must be less than maximum distance")
    exit()

# Create a new memory layer for the points
point_layer = QgsVectorLayer("Point", f"Random_Points_Seed{RANDOM_SEED}", "memory")
provider = point_layer.dataProvider()

# Set the CRS of the new layer to match the input layer
point_layer.setCrs(input_layer.crs())

# Generate the points
generated_points = generate_two_points_per_segment(input_layer, min_distance, max_distance)

# Add points to the layer
features = []
for point in generated_points:
    feat = QgsFeature()
    feat.setGeometry(QgsGeometry.fromPointXY(point))
    features.append(feat)

provider.addFeatures(features)
point_layer.updateExtents()

# Add layer to map
QgsProject.instance().addMapLayer(point_layer)
