from clearml import Dataset

if __name__ == "__main__":
    # Retrieve the dataset by its ID
    # dataset_id = '1f56ddcb332245239e926064c409848e'  # Replace with your actual dataset ID
    # parent_dataset = Dataset.get(dataset_id=dataset_id)
    parent_datasets = Dataset.get(dataset_name="Harit_Kaggledata", dataset_project="Harit_project_23Dec")
    print(parent_datasets.id)
    # parent_dataset = Dataset.get(dataset_name="existing_dataset_name", project_name="your_project_name")
    dataset = Dataset.create(
        dataset_name="Harit_Kaggledata_new",
        parent_datasets=[parent_datasets.id],
        dataset_version="1.0.1"
    )
    # Add files to the dataset
    dataset.add_files(r"C:\Akshay\AIMLOps24\Capstone Project\akshay_25dec\CapstoneProject-Group3\Newdata\leaf.jpg")

    # Upload the dataset to ClearML
    dataset.upload()  # Use upload to add the files to the ClearML server
    dataset.finalize()  # Finalize the dataset to make it immutable

    print(f"Dataset '{dataset_name}' version uploaded successfully.")
