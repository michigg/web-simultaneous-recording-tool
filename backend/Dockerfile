# Using python 3.7 in Alpine
FROM python:3-alpine

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY main.py /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

# Tell the port number the container should expose
EXPOSE 5000

# Run the command
CMD ["python3", "main.py"]
