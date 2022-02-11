# Download ubuntu from docker hub
FROM ubuntu:latest

# Download updates and install python3, pip and vim
RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install vim -y

# Declaring working directory in our container
WORKDIR /opt/apps/ebay-self-service

# Copy all relevant files to our working dir /opt/apps/flaskap
COPY requirements.txt .

# Install all requrements for our app
RUN pip3 install -r requirements.txt

# Copy source files to $WORKDIR
COPY src . 

# Expose container port to outside host
EXPOSE 5000

# Run the application
CMD [ "python3", "/opt/apps/ebay-self-service/app.py" ]