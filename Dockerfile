# Using an official Python base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the necessary files to the container
COPY . /app

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available outside of this container
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py"]