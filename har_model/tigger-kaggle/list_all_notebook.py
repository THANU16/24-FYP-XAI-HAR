from kaggle.api.kaggle_api_extended import KaggleApi

# Initialize and authenticate
api = KaggleApi()
api.authenticate()

# List all notebooks in your account
notebooks = api.kernels_list(mine=True)

# Print the notebook path and title
for notebook in notebooks:
    print(f"Title: {notebook.title}, Path: {notebook.ref}")