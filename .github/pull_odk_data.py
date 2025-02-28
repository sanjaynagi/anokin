import os
import requests
import pandas as pd
import json
import zipfile
import io

# Get credentials from environment variables
email = os.environ.get('ODK_EMAIL')
password = os.environ.get('ODK_PASSWORD')
odk_server = "https://odkcentral.lstmed.ac.uk"
project_id = 37
morph_form_id = 'ckmr_morpho_id'
uvlt_form_id = 'ckmr_uvlt'
asp_form_id = 'ckmr_sampling'


print(f"Connecting to ODK server: {odk_server}")

# Step 1: Authenticate with ODK Central to get a session token
session = requests.Session()
try:
    auth_response = session.post(
        f"{odk_server}/v1/sessions",
        json={
            "email": email,
            "password": password
        }
    )
    auth_response.raise_for_status()
    
    # Extract the token from the response
    token = auth_response.json().get('token')
    if not token:
        raise Exception("Failed to get authentication token")
        
    print("Successfully authenticated with ODK Central")
    
    # Step 2: Use the token for subsequent requests
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Create the data directory
    data_dir = "docs/anokin-site/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. Download and extract morphological ID form data (with repeat groups)
    print(f"Fetching data for project {project_id}, form {morph_form_id}")
    
    morph_response = session.get(
        f"{odk_server}/v1/projects/{project_id}/forms/{morph_form_id}/submissions.csv.zip?attachments=false",
        headers=headers
    )
    morph_response.raise_for_status()
    
    # Create a BytesIO object from the response content
    zip_content = io.BytesIO(morph_response.content)
    
    # Extract the ZIP file
    with zipfile.ZipFile(zip_content) as zip_ref:
        # List all files in the ZIP
        print("Files in the morphological ID ZIP archive:")
        for file_info in zip_ref.infolist():
            print(f" - {file_info.filename}")
        
        # Extract all files to the data directory
        zip_ref.extractall(data_dir)
    
    print("Morphological ID data successfully downloaded and extracted")
    
    # 2. Download UVLT form data (no repeat groups)
    print(f"Fetching data for project {project_id}, form {uvlt_form_id}")
    
    uvlt_response = session.get(
        f"{odk_server}/v1/projects/{project_id}/forms/{uvlt_form_id}/submissions.csv",
        headers=headers
    )
    uvlt_response.raise_for_status()
    
    # Save the UVLT data
    with open(os.path.join(data_dir, f"{uvlt_form_id}.csv"), "wb") as f:
        f.write(uvlt_response.content)
    
    print("UVLT data successfully downloaded")
    
    # 3. Download Indoor Sampling form data (no repeat groups)
    print(f"Fetching data for project {project_id}, form {asp_form_id}")
    
    asp_response = session.get(
        f"{odk_server}/v1/projects/{project_id}/forms/{asp_form_id}/submissions.csv",
        headers=headers
    )
    asp_response.raise_for_status()
    
    # Save the Indoor Sampling data
    with open(os.path.join(data_dir, f"{asp_form_id}.csv"), "wb") as f:
        f.write(asp_response.content)
    
    print("Indoor Sampling data successfully downloaded")
    
    # Optional: Log out / end the session
    logout_response = session.delete(
        f"{odk_server}/v1/sessions/{token}",
        headers=headers
    )
    logout_response.raise_for_status()
    print("Successfully logged out")
    
except requests.exceptions.RequestException as e:
    print(f"Error during ODK API request: {e}")
    if hasattr(e, 'response') and e.response:
        print(f"Response status code: {e.response.status_code}")
        print(f"Response text: {e.response.text}")
    raise
except Exception as e:
    print(f"Unexpected error: {e}")
    raise