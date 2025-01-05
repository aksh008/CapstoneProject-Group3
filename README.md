
# CapstoneProject-Group3
# Project Name :  Plant Disease Detection
Capstone Project for AIMLOps by Group 3 , this is for plant desease detection.
 

# Project Flow

![plantE2E-7](https://github.com/user-attachments/assets/367e6609-35e9-49aa-8465-d8db0b50be44)

# High level Architecture

![image](https://github.com/user-attachments/assets/5cff3bb9-7e88-434c-8d6d-2c932fc145d6)

# Model Training Testing Pipeline flow

![image](https://github.com/user-attachments/assets/8ff644f0-50c3-46d4-bde0-c91f45560e1d)


Steps to run the app:
in local :
1. create virtual env 
2. install requirement.txt (including .whl file)
3. create .env and store openai and literalai api key
4. python app/main.py (path for main.py)
5.localhost:8000/chainlit/ (for UI) , .localhost:8000/metrics/ (for Prometheus metrics).

we are using literal ai to store feedback (https://www.literalai.com/)

# Clear ML setup steps: 
1. Install clear ML
    pip install clearml
2. run command
    clearml-init
3. Add configurations as follow: 
    api {
        web_server: https://app.clear.ml/
        api_server: https://api.clear.ml
        files_server: https://files.clear.ml
        credentials {
            "access_key" = "XXX" 
            "secret_key" = "XXX"
        }
    }
Steps to get access_key and secret_key:
1. Log in to your ClearML account at app.clear.ml.
2. Navigate to Settings > Profile.
3. In the API Credentials section, you'll see your Access Key and Secret Key.
4. Copy these keys and note the server URL as https://api.clear.ml.

TODO
1. Think about retraining plan
2. 

Codespace - setting python 3.11 version 
https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces
