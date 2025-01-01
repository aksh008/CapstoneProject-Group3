
# CapstoneProject-Group3
# Project Name :  Plant Disease Detection
# Harit Bot

Capstone Project for AIMLOps by Group 3 , Plant Disease Detection.
 
### Project Flow
<img width="594" alt="image" src="https://github.com/aksh008/CapstoneProject-Group3/blob/main/pd-7.png">

### High level Architecture

![image](https://github.com/user-attachments/assets/5cff3bb9-7e88-434c-8d6d-2c932fc145d6)

### Model Training Testing Pipeline flow

![image](https://github.com/user-attachments/assets/8ff644f0-50c3-46d4-bde0-c91f45560e1d)


#### Steps to run app on local dev box :
1. create virtual env 
2. install requirement.txt (including .whl file -generated form python build command ran on harit model)
3. create .env and store openai and literalai api key (optionallly pass the varaible in command line only
    Ex: `docker run -e LITERAL_API_KEY='xxxxxxxxx' -e OPENAI_API_KEY='yyyyyy' -it -d -p 8000:8000 aksh008/harit-chainlit`
5. Traverse ot hait_model_api and run the command `python app/main.py` 
6. localhost:8000/chainlit/ (for UI) , localhost:8000/metrics/ (for Prometheus metrics).

###### Note:
 Literal ai to store user feedback (https://www.literalai.com/) 
  - Creds shared on demand 

#### Setting up Clear ML on local dev box
1. Install clear ML
    `pip install clearml`
2. run command
    `clearml-init`
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
##### Steps to get access_key and secret_key from ClearML
1. Log in to your ClearML account at [app.clear.ml.](https://app.clear.ml/)
2. Navigate to Settings > Profile.
3. In the API workspace section, Access Key and secret details should be present if not create new credentials
4. Copy these keys and update configuration mentioned in previous step

##### TODO
1. Think about retraining plan - based on data set changes or user feedback
2. Local language support in UI

#### Steps for setting python 3.11 version on Codespace
https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces
