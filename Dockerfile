# Use the official AWS Lambda Python 3.12 runtime as a parent image
FROM public.ecr.aws/lambda/python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Install system dependencies
RUN yum update -y && \
    yum install -y gcc gcc-c++ make git && \
    yum clean all

# Copy requirements first for better caching
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ${LAMBDA_TASK_ROOT}/

# Create necessary directories
RUN mkdir -p ${LAMBDA_TASK_ROOT}/.streamlit

# Create Streamlit config
RUN echo '[server]\nport = 8501\naddress = "0.0.0.0"\nheadless = true\n\n[browser]\ngatherUsageStats = false\n\n[theme]\nbase = "light"' > ${LAMBDA_TASK_ROOT}/.streamlit/config.toml

# Set the CMD to your handler (this will be the entry point for Lambda)
CMD ["lambda_handler.handler"]