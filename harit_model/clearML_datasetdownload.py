from clearml import Dataset

if __name__ == "__main__":
    # Retrieve the dataset by its ID
    # dataset_id = '1f56ddcb332245239e926064c409848e'  # Replace with your actual dataset ID
    # dataset = Dataset.get(dataset_id=dataset_id)

    dataset = Dataset.get(
        dataset_id=None,  
        dataset_project="Harit_CapStone_Project",
        dataset_name="Harit_DataSet",
        # dataset_tags="my tag",
        # dataset_version="1.2",
        only_completed=True, 
        only_published=False,
)

    # Download the dataset to a local directory
    local_path = dataset.get_mutable_local_copy(
        target_folder=r"/Users/hemanth/Downloads/Capstonedata",
        overwrite=True,
    )

    # dataset.sync_folder(
    #     local_path=r"C:\Akshay\AIMLOps24\Capstone Project\akshay_25dec\CapstoneProject-Group3\Newdata\train",
    #     verbose=True,      
    # )
    # Now, you can read the dataset's files from the local path
    print("Dataset successfully downloaded to:", local_path)
    # Dataset.finalize()  # Finalize the dataset to make it immutable
