FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot's code
COPY . .

# Run the bot
CMD ["python", "bot.py"]
