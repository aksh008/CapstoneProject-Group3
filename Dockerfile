# pull python base image
FROM python:3.10


# specify working directory
WORKDIR /capstone

# copy application files
ADD . /capstone


# update pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# RUN pip install chainlit
# expose port for application chainlit running on 8000
EXPOSE 8000

#start chainlit app
CMD ["chainlit", "run" ,"harit_model/predict.py", "--host", "0.0.0.0"]
