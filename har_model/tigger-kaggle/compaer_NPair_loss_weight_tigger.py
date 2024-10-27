# import kagglehub
# from kaggle.api.kaggle_api_extended import KaggleApi

# # Authenticate
# kagglehub.login()  # This will prompt you for your credentials.

# # Initialize and authenticate
# api = KaggleApi()
# api.authenticate()

# # List all notebooks in your account
# notebooks = api.kernels_list(mine=True)

# # Print the notebook path and title
# for notebook in notebooks:
#     print(f"Title: {notebook.title}, Path: {notebook.ref}")



from kaggle.api.kaggle_api_extended import KaggleApi
import os
# import kagglehub
import requests

requests.adapters.DEFAULT_RETRIES = 10  # Increase retry attempts


# Authenticate
# kagglehub.login()  # This will prompt you for your credentials.




# Initialize and authenticate Kaggle API
api = KaggleApi()
api.authenticate()

# Define the parameters
epochs = 20
epoch_per_batch_count = 2
weighted_loss_factor = 0.2  # Example value

# Set the environment variables
os.environ["EPOCHS"] = str(epochs)
os.environ["EPOCH_PER_BATCH_COUNT"] = str(epoch_per_batch_count)
os.environ["WEIGHTED_LOSS_FACTOR"] = str(weighted_loss_factor)


notebook_path = "har_model/tigger-kaggle/example"  # Kaggle path

# Push the notebook back to Kaggle
api.kernels_push(notebook_path)
print("New version of the notebook pushed successfully.")



