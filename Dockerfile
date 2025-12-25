# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy agent code
COPY jbits_agent.py /app/

# Install dependencies
RUN pip install --no-cache-dir web3

# Expose nothing (standalone agent), but you can expose ports if needed later
# ENV variables are set via docker-compose or .env
CMD ["python", "jbits_agent.py"]