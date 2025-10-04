#!/bin/bash

# Deployment script for Nepal Legal Chatbot to AWS Lambda
# Make sure to have AWS CLI configured and Docker installed

set -e

# Configuration
ECR_REPOSITORY_NAME="nepal-legal-chatbot"
LAMBDA_FUNCTION_NAME="nepal-legal-chatbot-streamlit"
AWS_REGION="us-east-1"
MEMORY_SIZE="3008"  # Maximum memory for Lambda
TIMEOUT="900"       # Maximum timeout for Lambda (15 minutes)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if AWS CLI is installed and configured
if ! command -v aws &> /dev/null; then
    echo_error "AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo_error "Docker is not installed. Please install it first."
    exit 1
fi

# Get AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
if [ $? -ne 0 ]; then
    echo_error "Failed to get AWS account ID. Please check your AWS CLI configuration."
    exit 1
fi

ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}"

echo_info "Starting deployment process..."
echo_info "AWS Account ID: ${AWS_ACCOUNT_ID}"
echo_info "ECR Repository: ${ECR_URI}"
echo_info "Lambda Function: ${LAMBDA_FUNCTION_NAME}"

# Step 1: Create ECR repository if it doesn't exist
echo_info "Creating ECR repository if it doesn't exist..."
aws ecr describe-repositories --repository-names ${ECR_REPOSITORY_NAME} --region ${AWS_REGION} &> /dev/null || \
aws ecr create-repository --repository-name ${ECR_REPOSITORY_NAME} --region ${AWS_REGION}

# Step 2: Login to ECR
echo_info "Logging in to ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URI}

# Step 3: Build Docker image
echo_info "Building Docker image..."
docker build -t ${ECR_REPOSITORY_NAME} .

# Step 4: Tag image for ECR
echo_info "Tagging image for ECR..."
docker tag ${ECR_REPOSITORY_NAME}:latest ${ECR_URI}:latest

# Step 5: Push image to ECR
echo_info "Pushing image to ECR..."
docker push ${ECR_URI}:latest

# Step 6: Create or update Lambda function
echo_info "Creating or updating Lambda function..."

# Check if function exists
if aws lambda get-function --function-name ${LAMBDA_FUNCTION_NAME} --region ${AWS_REGION} &> /dev/null; then
    echo_info "Updating existing Lambda function..."
    aws lambda update-function-code \
        --function-name ${LAMBDA_FUNCTION_NAME} \
        --image-uri ${ECR_URI}:latest \
        --region ${AWS_REGION}
    
    # Update function configuration
    aws lambda update-function-configuration \
        --function-name ${LAMBDA_FUNCTION_NAME} \
        --timeout ${TIMEOUT} \
        --memory-size ${MEMORY_SIZE} \
        --region ${AWS_REGION}
else
    echo_info "Creating new Lambda function..."
    
    # Create execution role if it doesn't exist
    ROLE_NAME="nepal-legal-chatbot-lambda-role"
    ROLE_ARN=$(aws iam get-role --role-name ${ROLE_NAME} --query 'Role.Arn' --output text 2>/dev/null || echo "")
    
    if [ -z "$ROLE_ARN" ]; then
        echo_info "Creating IAM role for Lambda..."
        
        # Create trust policy
        cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
        
        # Create role
        aws iam create-role \
            --role-name ${ROLE_NAME} \
            --assume-role-policy-document file://trust-policy.json
        
        # Attach basic execution policy
        aws iam attach-role-policy \
            --role-name ${ROLE_NAME} \
            --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
        
        # Wait for role to be created
        sleep 10
        
        ROLE_ARN=$(aws iam get-role --role-name ${ROLE_NAME} --query 'Role.Arn' --output text)
        
        # Clean up
        rm trust-policy.json
    fi
    
    # Create Lambda function
    aws lambda create-function \
        --function-name ${LAMBDA_FUNCTION_NAME} \
        --role ${ROLE_ARN} \
        --code ImageUri=${ECR_URI}:latest \
        --package-type Image \
        --timeout ${TIMEOUT} \
        --memory-size ${MEMORY_SIZE} \
        --region ${AWS_REGION}
fi

# Step 7: Create Function URL (for HTTP access)
echo_info "Creating or updating Function URL..."
aws lambda create-function-url-config \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --auth-type NONE \
    --cors '{
        "AllowCredentials": false,
        "AllowHeaders": ["*"],
        "AllowMethods": ["*"],
        "AllowOrigins": ["*"],
        "ExposeHeaders": ["*"],
        "MaxAge": 86400
    }' \
    --region ${AWS_REGION} 2>/dev/null || \

aws lambda update-function-url-config \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --auth-type NONE \
    --cors '{
        "AllowCredentials": false,
        "AllowHeaders": ["*"],
        "AllowMethods": ["*"],
        "AllowOrigins": ["*"],
        "ExposeHeaders": ["*"],
        "MaxAge": 86400
    }' \
    --region ${AWS_REGION}

# Get the Function URL
FUNCTION_URL=$(aws lambda get-function-url-config --function-name ${LAMBDA_FUNCTION_NAME} --region ${AWS_REGION} --query 'FunctionUrl' --output text)

echo_info "Deployment completed successfully!"
echo_info "Function URL: ${FUNCTION_URL}"
echo_warn "Note: It may take a few minutes for the function to be ready."
echo_warn "Make sure to set up environment variables in the Lambda console:"
echo_warn "  - GEMINI_API_KEY"
echo_warn "  - PINECONE_API_KEY"
echo_warn "  - COHERE_API_KEY"
echo_warn "  - Database connection variables (if using external DB)"