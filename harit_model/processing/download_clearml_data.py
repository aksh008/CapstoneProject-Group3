from pathlib import Path
from harit_model import config
import os
from clearml import Dataset

def download_fromclearml(project, dataset, output_dir):
    dataset = Dataset.get(
        dataset_id=None,  
        dataset_project=project,
        dataset_name=dataset,
        # dataset_tags="my tag",
        # dataset_version="1.2",
        only_completed=True, 
        only_published=False,
    )

    # Download the dataset to a local directory
    local_path = dataset.get_mutable_local_copy(
        target_folder=output_dir,
        overwrite=True,
    )
    # Now, you can read the dataset's files from the local path
    print("Dataset successfully downloaded to:", local_path)

def download_dataset():
    
    print ("going to download from clearml")
    clearml_config = config.app_config.clearmlconfig
    project = clearml_config.project
    dataset = clearml_config.dataset
    output_dir = Path(clearml_config.output_dir)
    
    # testing only
    #project = "Harit_CapStone_Project"
    #dataset = "Harit_DataSet"
    #output_dir ="./../haritdataset" 
    
    # Ensure output directory exists
    os.makedirs(output_dir,  exist_ok=True)

    # Download the dataset
    print(f"Downloading dataset from clearml: {dataset} from project:{project}")
    download_fromclearml(project, dataset, output_dir)
    #return path

if __name__ == "__main__":
    download_dataset()