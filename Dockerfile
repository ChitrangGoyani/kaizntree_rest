# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.10

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Get the Real World example app
RUN git clone https://github.com/ChitrangGoyani/kaizntree_rest.git /drf_src

# Set the working directory to /drf
# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.
WORKDIR /drf_src

RUN ls .

# Install any needed packages specified in requirements.txt
# RUN apt update && apt upgrade -y
# RUN add-apt-repository ppa:deadsnakes/ppa -y
# RUN sudo apt update
# RUN apt install python3.8
# RUN python3.8 --version
# RUN python3 -m venv kaizntree
# RUN . kaizntree/bin/activate
# RUN pip3 install --upgrade pip
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

VOLUME /drf_src

EXPOSE 8080

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# CMD ["%%CMD%%"]