# pull python base image
FROM python:3.10

# copy application files
ADD ./harit_model_api /harit_model_api/

# specify working directory
WORKDIR /harit_model_api

# copy the Trained Model H5 file to App folder
COPY ./harit_model/trained_models/*.h5 /harit_model_api/app/

# update pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# expose port for application
EXPOSE 8001

# start fastapi application
# CMD ["chainlit", "run" ,"app/main.py", "--host", "0.0.0.0"]
CMD ["python", "app/main.py"]
# CMD ["uvicorn", "harit_model_api.app.main:app", "--host", "0.0.0.0", "--port", "8001"]




