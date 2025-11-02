# Use lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency file and install (cache-friendly)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 5000

# Run app with Gunicorn WSGI server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]




# Use lightweight base image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install only what’s needed
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port
EXPOSE 5000

# Use Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
