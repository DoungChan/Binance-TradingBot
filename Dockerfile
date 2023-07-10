# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip&&pip install -r requirements.txt

# Copy the rest of the code to the container
COPY . .

# Run the code
CMD ["python", "trading-bot.py"]
