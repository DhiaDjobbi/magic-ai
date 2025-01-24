# Base image with Python 3.9
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (ffmpeg, and git)
RUN apt-get update && apt-get install -y ffmpeg git

# Copy the application files
COPY main.py requirements.txt ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Set the FLASK_APP environment variable
ENV FLASK_APP=main.py

# Expose the port Flask will run on
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["flask", "run", "--host", "0.0.0.0"]
