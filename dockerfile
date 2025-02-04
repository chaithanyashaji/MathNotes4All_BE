# Use the Python 3 alpine official image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy local code to the container image
COPY . .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app will listen on
EXPOSE 8000

# Run the web service on container startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
