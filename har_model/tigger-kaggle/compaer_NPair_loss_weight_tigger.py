import json
import time
from kaggle.api.kaggle_api_extended import KaggleApi

# Initialize and authenticate Kaggle API
api = KaggleApi()
api.authenticate()


project_path = "har_model/tigger-kaggle/example"
# Path to your Kaggle notebook (make sure the path is correct)
notebook_path = "har_model/tigger-kaggle/example/tigger-using-ku-har-npair-and-softmax-classifier.ipynb"
config_path = "har_model/tigger-kaggle/example/config.json"
kernal = "thanushanth/tigger-using-ku-har-npair-and-softmax-classifier"


def get_version():
    # Read the existing config file
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Access the current version and increment it
    current_version = config.get("version", 1)
    new_version = current_version + 1
    config["version"] = new_version
    name = config.get("name", "Version")
    version_name = f"{name}-{current_version}"

    # Write the updated config back to the config file
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=2)
    
    return version_name

def update_notebook(config):
    # Read the existing notebook
    with open(notebook_path, 'r') as notebook_file:
        notebook_content = json.load(notebook_file)

    # Update the config variable in the notebook
    for cell in notebook_content['cells']:
        if cell['cell_type'] == 'code':
            # Check if the cell has source code
            if cell['source']:
                # Look for the config variable and update it
                if 'config =' in cell['source'][0]:  # Check if this is the config cell
                    # Update the config line
                    cell['source'][0] = "config = None\n"
                    cell['source'][0] = f"config = {json.dumps(config, indent=2)}\n"

    # Write the changes back to the notebook file
    with open(notebook_path, 'w') as notebook_file:
        json.dump(notebook_content, notebook_file)


WEIGHT_NPAIR_LOSS = 0

for i in range (0, 11, 1):
    version = get_version()
    epochs = 100
    epoch_batch_count = 32
        
    config = {
        "EPOCHS": epochs,
        "EPOCH_BATCH_COUNT": epoch_batch_count,
        "WEIGHT_NPAIR_LOSS": WEIGHT_NPAIR_LOSS,
        "NAME" : version
    }
    # Update the notebook with the new config
    update_notebook(config)
    # Push the updated notebook back to Kaggle
    status1 = api.kernels_push(project_path)
    print(f"Updated notebook {version} pushed successfully. Parameters are EPOCHS: {epochs}, EPOCH_BATCH_COUNT: {epoch_batch_count}, WEIGHT_NPAIR_LOSS: {WEIGHT_NPAIR_LOSS}")
    # Wait a few seconds to ensure the push has been processed
    time.sleep(50)

    # Check the status of the notebook version
    status = api.kernels_status(kernal)
    while status.get("status") == "running":
        print(f"Notebook {version} is still in progress.")
        time.sleep(240)
        status = api.kernels_status(kernal)
    print(f"Notebook {version} has been successfully completed.")
    WEIGHT_NPAIR_LOSS += 0.1
