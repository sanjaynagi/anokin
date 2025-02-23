from qgis.core import *
import processing
from qgis.PyQt.QtWidgets import QFileDialog
import os

def export_points_by_day():
    # Get the point layer
    point_layer = iface.activeLayer()
    if not point_layer:
        print("No active layer selected! Please select your points layer.")
        return
    
    # Verify the day field exists
    field_names = [field.name() for field in point_layer.fields()]
    day_field = 'day'  # Field name
    if day_field not in field_names:
        print(f"Error: Field '{day_field}' not found in layer.")
        print(f"Available fields: {field_names}")
        return
    
    # Get the output folder
    output_folder = QFileDialog.getExistingDirectory(None, "Select Output Folder")
    if not output_folder:
        print("No output folder selected. Operation cancelled.")
        return
    
    # Get unique days
    days = set()
    for feature in point_layer.getFeatures():
        day = feature[day_field]
        if day:  # Only add non-null values
            days.add(day)
    
    days = sorted(list(days))  # Convert to sorted list
    print(f"Found points for days: {days}")
    
    # Export each day as separate KML
    for day in days:
        if day == 'NA':  # Skip NA values if you want
            continue
            
        # Create file name
        safe_day = day.replace(' ', '_').lower()
        output_file = os.path.join(output_folder, f"points_{safe_day}.kml")
        
        try:
            # Create a temporary layer with only the points for this day
            exp = QgsExpression(f"\"{day_field}\" = '{day}'")
            request = QgsFeatureRequest(exp)
            
            # Create temporary layer
            temp_layer = QgsVectorLayer("Point", "temp", "memory")
            temp_layer.setCrs(point_layer.crs())
            
            # Copy fields from original layer
            temp_layer.startEditing()
            temp_layer.dataProvider().addAttributes(point_layer.fields())
            temp_layer.updateFields()
            
            # Add filtered features
            features = []
            for feature in point_layer.getFeatures(request):
                features.append(feature)
            
            temp_layer.dataProvider().addFeatures(features)
            temp_layer.commitChanges()
            
            # Export to KML
            processing.run("native:savefeatures", {
                'INPUT': temp_layer,
                'OUTPUT': output_file,
                'DATASOURCE_OPTIONS': '',
                'LAYER_OPTIONS': ''
            })
            
            print(f"Exported points for {day} to {output_file}")
            
        except Exception as e:
            print(f"Error exporting {day}: {str(e)}")
    
    print("\nExport complete!")
    print(f"Files saved to: {output_folder}")

# Run the function
export_points_by_day()
