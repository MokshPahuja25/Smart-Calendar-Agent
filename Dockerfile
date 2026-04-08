# 1. Use a lightweight Python environment
FROM python:3.12-slim

# 2. Set the working directory inside the cloud computer
WORKDIR /app

# 3. Copy your project files into the cloud computer
COPY . /app

# 4. Install the exact requirements
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tell the cloud computer we are using port 8080
EXPOSE 8080

# 6. The foolproof startup command (relying on your main.py code from last night)
CMD ["python", "main.py"]