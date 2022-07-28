# Here we get the basic templates so that Docker can process the project.
# Python image is enough for us, because we will get other images in docker-compose.yaml.
FROM python:latest

# We set these environmental settings for the Docker so that the Docker does not do extra work.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# In the operating system that Docker builds for us, we design a main place to execute our own code.
# This environment is called a WORKDIR or workspace directory. Docker now knows where to run our code on its OS.
WORKDIR /code

# The Docker is told to transfer the file containing the information of the required packages to its operating system.
ADD requirements.txt /code/

# Docker is told to update the pip first to ensure that the setup procedure is standard.
RUN pip install --upgrade pip

# Docker is told to install the required packages on its operating system through the requirements.txt file that was
# transferred in the previous steps.
RUN pip install -r requirements.txt

# Docker is told to transfer all current project data to WORKDIR and its operating system.
ADD . /code/

# Finally, Docker presents our personal image and is ready to run.
