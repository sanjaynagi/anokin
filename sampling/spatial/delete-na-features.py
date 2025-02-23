from qgis.core import *

# Get the active layer
layer = iface.activeLayer()
if not layer:
    print("No layer selected!")
    exit()

# Start editing session
layer.startEditing()

# Create list of features to delete
features_to_delete = []
for feature in layer.getFeatures():
    if feature['day'] == 'NA':
        features_to_delete.append(feature.id())

# Delete the features
layer.deleteFeatures(features_to_delete)

# Commit the changes
layer.commitChanges()

# Print summary
print(f"Deleted {len(features_to_delete)} features with day = 'NA'")
