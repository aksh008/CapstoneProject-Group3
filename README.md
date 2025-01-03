
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
3. create new file by name `.env` and store openai and literalai api key as key value pair (optionallly pass key values in command line) 
    Ex:
5. Traverse to hait_model_api folder and run command `python app/main.py` 
6. localhost:8000/chainlit/ (for UI) , localhost:8000/metrics/ (for Prometheus metrics).
7. Docker steps after model is trained and h5 file is copied from trained model to api folder
   
   a. ` docker build -t harit_model_api .`
    
   b. to pull existing trained model from docker repo ` docker pull aksh008/harit-chainlit`
   
   c. Run docker image pulled from repo -  `docker run -e LITERAL_API_KEY='xxxxxxxxx' -e OPENAI_API_KEY='yyyyyy' -it -d -p 8000:8000 aksh008/harit-chainlit`
   

###### Note:
 Literal ai to store user feedback (https://www.literalai.com/) 
  - Creds shared on demand 

## Clear ML Related
#### Setting up on local dev box
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
##### Steps to get access_key and secret_key 
1. Log in to your ClearML account at [app.clear.ml.](https://app.clear.ml/)
2. Navigate to Settings > Profile.
3. In the API workspace section, Access Key and secret details should be present if not create new credentials
4. Copy these keys and update configuration mentioned in previous step

##### Create a new dataset add files through commands 
1. Create project and dataset `clearml-data create --project "Harit_CapStone_Project" --name "Harit_DataSet"`
2. Add files from local to clearml ` clearml-data add --files <dataset>`  <dataset denotes absolute loction on local dev box>
3. Complete data upload `clearml-data close`

##### TODO
1. Think about retraining plan - based on data set changes or user feedback
2. Local language support in UI

##### Steps for setting python 3.11 version on Codespace
https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces

