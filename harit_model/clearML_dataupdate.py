from clearml import Dataset

if __name__ == "__main__":
    # Retrieve the dataset by its ID
    dataset_id = '1f56ddcb332245239e926064c409848e'  # Replace with your actual dataset ID
    dataset = Dataset.get(dataset_id=dataset_id)

    # the dataset to a local directory
    local_path = r'C:\Akshay\AIMLOps24\Capstone Project\akshay_25dec\CapstoneProject-Group3\Newdata\leaf.jpg'

    # Add files to the dataset
    dataset.add_files(local_path)

    # Optionally, you can also add tags or comments
    dataset.add_tags(["new_version", "updated"])
    
