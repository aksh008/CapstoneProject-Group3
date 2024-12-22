# pull python base image
FROM python:3.10

# copy application files
ADD /harit_model_api /harit_model_api/

# specify working directory
WORKDIR /harit_model_api

# copy the pk file tp App folder
COPY . /trained_models/*.h5 /harit_model_api/app

# update pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# expose port for application
EXPOSE 8000

# start fastapi application
CMD ["chainlit", "run" ,"harit_model/predict.py", "--host", "0.0.0.0"]



