# Use the appropriate base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/tmp/huggingface_cache

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Set permissions for the working directory and subdirectories
RUN chmod -R 777 /app

# Set the appropriate ownership (optional but recommended)
RUN chown -R root:root /app

# Expose the port the app will run on (if applicable)
EXPOSE 5000

# Command to run the application (e.g., Flask)
CMD ["flask", "run", "--host=0.0.0.0"]
