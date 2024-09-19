# Use the official Python image as base
FROM python:3.8-slim

# Set the working directory in the container
RUN mkdir searchapp
WORKDIR searchapp

# Copy the backend files to the container
COPY . .

# Install web dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt
# Install es dependencies
RUN pip install --no-cache-dir -r es/requirements.txt

# Expose the port the backend runs on
EXPOSE 5000

# Command to run the backend
CMD ["python", "-m", "meow", "limit=20"]