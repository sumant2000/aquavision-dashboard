#!/bin/bash

# AWS Deployment Script for Logixon Smart AquaVision
# This script deploys the application to AWS using ECS and ALB

set -e

# Configuration
AWS_REGION=${AWS_REGION:-"us-east-1"}
ECR_REPOSITORY_NAME="logixon-aquavision"
ECS_CLUSTER_NAME="aquavision-cluster"
ECS_SERVICE_NAME="aquavision-service"
ALB_NAME="aquavision-alb"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check AWS CLI
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed"
        exit 1
    fi
    
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS CLI is not configured. Please run 'aws configure'"
        exit 1
    fi
    
    print_success "AWS CLI is configured"
}

# Create ECR repository
create_ecr_repository() {
    print_status "Creating ECR repository..."
    
    aws ecr create-repository \
        --repository-name $ECR_REPOSITORY_NAME \
        --region $AWS_REGION \
        --image-scanning-configuration scanOnPush=true \
        --encryption-configuration encryptionType=AES256 \
        2>/dev/null || print_warning "ECR repository may already exist"
    
    ECR_URI=$(aws ecr describe-repositories \
        --repository-names $ECR_REPOSITORY_NAME \
        --region $AWS_REGION \
        --query 'repositories[0].repositoryUri' \
        --output text)
    
    print_success "ECR repository: $ECR_URI"
}

# Build and push Docker images
build_and_push_images() {
    print_status "Building and pushing Docker images..."
    
    # Login to ECR
    aws ecr get-login-password --region $AWS_REGION | \
        docker login --username AWS --password-stdin $ECR_URI
    
    # Build backend image
    print_status "Building backend image..."
    docker build -t $ECR_REPOSITORY_NAME-backend:latest ./backend/
    docker tag $ECR_REPOSITORY_NAME-backend:latest $ECR_URI:backend-latest
    docker push $ECR_URI:backend-latest
    
    # Build frontend image
    print_status "Building frontend image..."
    docker build -t $ECR_REPOSITORY_NAME-frontend:latest ./frontend/
    docker tag $ECR_REPOSITORY_NAME-frontend:latest $ECR_URI:frontend-latest
    docker push $ECR_URI:frontend-latest
    
    print_success "Images pushed to ECR"
}

# Create ECS cluster
create_ecs_cluster() {
    print_status "Creating ECS cluster..."
    
    aws ecs create-cluster \
        --cluster-name $ECS_CLUSTER_NAME \
        --capacity-providers EC2 FARGATE \
        --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1 \
        --region $AWS_REGION \
        2>/dev/null || print_warning "ECS cluster may already exist"
    
    print_success "ECS cluster created: $ECS_CLUSTER_NAME"
}

# Create task definition
create_task_definition() {
    print_status "Creating ECS task definition..."
    
    cat > task-definition.json << EOF
{
    "family": "aquavision-task",
    "networkMode": "awsvpc",
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "1024",
    "memory": "2048",
    "executionRoleArn": "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/ecsTaskExecutionRole",
    "containerDefinitions": [
        {
            "name": "backend",
            "image": "$ECR_URI:backend-latest",
            "portMappings": [
                {
                    "containerPort": 8000,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/aquavision",
                    "awslogs-region": "$AWS_REGION",
                    "awslogs-stream-prefix": "backend"
                }
            },
            "environment": [
                {
                    "name": "ENVIRONMENT",
                    "value": "production"
                }
            ]
        },
        {
            "name": "frontend",
            "image": "$ECR_URI:frontend-latest",
            "portMappings": [
                {
                    "containerPort": 3000,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/aquavision",
                    "awslogs-region": "$AWS_REGION",
                    "awslogs-stream-prefix": "frontend"
                }
            }
        }
    ]
}
EOF
    
    aws ecs register-task-definition \
        --cli-input-json file://task-definition.json \
        --region $AWS_REGION
    
    rm task-definition.json
    print_success "Task definition registered"
}

# Create CloudWatch log group
create_log_group() {
    print_status "Creating CloudWatch log group..."
    
    aws logs create-log-group \
        --log-group-name "/ecs/aquavision" \
        --region $AWS_REGION \
        2>/dev/null || print_warning "Log group may already exist"
    
    print_success "CloudWatch log group created"
}

# Create ECS service
create_ecs_service() {
    print_status "Creating ECS service..."
    
    # Get default VPC and subnets
    VPC_ID=$(aws ec2 describe-vpcs \
        --filters "Name=isDefault,Values=true" \
        --query 'Vpcs[0].VpcId' \
        --output text \
        --region $AWS_REGION)
    
    SUBNET_IDS=$(aws ec2 describe-subnets \
        --filters "Name=vpc-id,Values=$VPC_ID" \
        --query 'Subnets[*].SubnetId' \
        --output text \
        --region $AWS_REGION)
    
    SUBNET_LIST=$(echo $SUBNET_IDS | tr ' ' ',')
    
    # Create security group
    SECURITY_GROUP_ID=$(aws ec2 create-security-group \
        --group-name aquavision-sg \
        --description "Security group for Logixon AquaVision" \
        --vpc-id $VPC_ID \
        --region $AWS_REGION \
        --query 'GroupId' \
        --output text 2>/dev/null || \
        aws ec2 describe-security-groups \
        --group-names aquavision-sg \
        --query 'SecurityGroups[0].GroupId' \
        --output text \
        --region $AWS_REGION)
    
    # Add security group rules
    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp \
        --port 80 \
        --cidr 0.0.0.0/0 \
        --region $AWS_REGION \
        2>/dev/null || true
    
    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp \
        --port 3000 \
        --cidr 0.0.0.0/0 \
        --region $AWS_REGION \
        2>/dev/null || true
    
    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp \
        --port 8000 \
        --cidr 0.0.0.0/0 \
        --region $AWS_REGION \
        2>/dev/null || true
    
    # Create ECS service
    aws ecs create-service \
        --cluster $ECS_CLUSTER_NAME \
        --service-name $ECS_SERVICE_NAME \
        --task-definition aquavision-task \
        --desired-count 1 \
        --launch-type FARGATE \
        --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_LIST],securityGroups=[$SECURITY_GROUP_ID],assignPublicIp=ENABLED}" \
        --region $AWS_REGION \
        2>/dev/null || print_warning "ECS service may already exist"
    
    print_success "ECS service created: $ECS_SERVICE_NAME"
}

# Wait for service to be stable
wait_for_service() {
    print_status "Waiting for service to be stable..."
    
    aws ecs wait services-stable \
        --cluster $ECS_CLUSTER_NAME \
        --services $ECS_SERVICE_NAME \
        --region $AWS_REGION
    
    print_success "Service is stable"
}

# Get service endpoints
get_endpoints() {
    print_status "Getting service endpoints..."
    
    TASK_ARN=$(aws ecs list-tasks \
        --cluster $ECS_CLUSTER_NAME \
        --service-name $ECS_SERVICE_NAME \
        --query 'taskArns[0]' \
        --output text \
        --region $AWS_REGION)
    
    if [ "$TASK_ARN" != "None" ] && [ "$TASK_ARN" != "" ]; then
        PUBLIC_IP=$(aws ecs describe-tasks \
            --cluster $ECS_CLUSTER_NAME \
            --tasks $TASK_ARN \
            --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' \
            --output text \
            --region $AWS_REGION | \
            xargs -I {} aws ec2 describe-network-interfaces \
            --network-interface-ids {} \
            --query 'NetworkInterfaces[0].Association.PublicIp' \
            --output text \
            --region $AWS_REGION)
        
        print_success "🎉 Deployment completed!"
        echo
        echo "Application endpoints:"
        echo "  Frontend: http://$PUBLIC_IP:3000"
        echo "  Backend API: http://$PUBLIC_IP:8000"
        echo "  API Documentation: http://$PUBLIC_IP:8000/docs"
        echo
    else
        print_error "Could not retrieve task information"
    fi
}

# Main deployment function
main() {
    echo "🚀 Deploying Logixon Smart AquaVision to AWS"
    echo "============================================="
    echo
    
    check_aws_cli
    create_ecr_repository
    build_and_push_images
    create_log_group
    create_ecs_cluster
    create_task_definition
    create_ecs_service
    wait_for_service
    get_endpoints
    
    print_success "🎉 Deployment completed successfully!"
}

# Run main function
main "$@"