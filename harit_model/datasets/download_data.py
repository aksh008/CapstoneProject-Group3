import kagglehub

# Specify the output path for the dataset
output_path = r"C:\Akshay\AIMLOps24\Capstone Project\CapstoneProject-Group3\harit_model\datasets"

try:
    # Attempt to download the dataset
    path = kagglehub.dataset_download("vipoooool/new-plant-diseases-dataset")
    print("Dataset downloaded successfully to:", path)
except Exception as e:
    print("Error downloading dataset:", str(e))
