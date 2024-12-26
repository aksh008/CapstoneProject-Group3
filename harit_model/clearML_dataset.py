from clearml import Dataset

if __name__ == "__main__":
    # Retrieve the dataset by its ID
    dataset_id = '1f56ddcb332245239e926064c409848e'  # Replace with your actual dataset ID
    dataset = Dataset.get(dataset_id=dataset_id)

    # Download the dataset to a local directory
    local_path = dataset.get_local_copy()

    # Now, you can read the dataset's files from the local path
    print("Dataset downloaded to:", local_path)
