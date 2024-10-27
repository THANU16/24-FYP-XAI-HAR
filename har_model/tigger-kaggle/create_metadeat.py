import json

# Modified metadata
metadata = {
    "id": "thanushanth/using-ku-har-npair-and-softmax-classifier",
    "title": "Using ku-har - NPair and softmax classifier",
    "code_file": "using-ku-har-npair-and-softmax-classifier.ipynb",
    "language": "python",
    "kernel_type": "notebook",
    "is_private": False,
    "tags": [
        "Machine Learning",
        "Deep Learning",
        "Kaggle"
    ],
    "datasets": [
        {
            "path": "/kaggle/input/3.Time_domain_subsamples/KU-HAR_time_domain_subsamples_20750x300.csv",
            "description": "Time domain subsamples dataset for human activity recognition."
        }
    ]
}

# Save to a JSON file
with open('har_model/tigger-kaggle/example/kernel-metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)

print("Modified metadata saved successfully.")
