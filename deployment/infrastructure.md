# Infrastructure Deployment Guide

This document outlines how to deploy the 60 Days of Madonna serverless application to AWS.

## Prerequisites

- AWS CLI configured with appropriate permissions
- Python 3.9+ installed
- Domain name with DNS management access

## AWS Services Required

### Core Services
- **S3**: Website hosting bucket
- **CloudFront**: CDN and HTTPS delivery
- **Route53**: DNS management
- **ACM**: SSL certificates
- **API Gateway**: REST API
- **Lambda**: Serverless functions
- **DynamoDB**: User data storage
- **IAM**: Roles and permissions

## Deployment Steps

### 1. Set Up Domain and SSL

```bash
# Request SSL certificate (must be in us-east-1 for CloudFront)
aws acm request-certificate \
  --domain-name yourdomain.com \
  --subject-alternative-names www.yourdomain.com api.yourdomain.com \
  --validation-method DNS \
  --region us-east-1

# Add DNS validation records to your hosted zone
# (AWS will provide the CNAME records to add)
```

### 2. Create DynamoDB Table

```bash
aws dynamodb create-table \
  --table-name previousSongs \
  --attribute-definitions \
    AttributeName=userID,AttributeType=S \
  --key-schema \
    AttributeName=userID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region eu-west-2
```

### 3. Create S3 Bucket for Website

```bash
# Create bucket
aws s3 mb s3://yourdomain.com --region eu-west-2

# Enable website hosting
aws s3 website s3://yourdomain.com \
  --index-document index.html \
  --error-document error.html

# Set public access policy
aws s3api put-bucket-policy \
  --bucket yourdomain.com \
  --policy file://s3-policy.json
```

### 4. Deploy Lambda Functions

```bash
# Create IAM role for Lambda
aws iam create-role \
  --role-name madz_lambda_role \
  --assume-role-policy-document file://lambda-trust-policy.json

# Attach DynamoDB permissions
aws iam attach-role-policy \
  --role-name madz_lambda_role \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

# Package and deploy each Lambda function
for func in madz_get_a_song madz_get_all_songs madz_get_all_my_songs madz_get_my_day_count madz_reset_my_songs madz_create_new_user; do
  zip ${func}.zip ${func}_lambda.py
  
  aws lambda create-function \
    --function-name $func \
    --runtime python3.9 \
    --role arn:aws:iam::YOUR_ACCOUNT:role/madz_lambda_role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://${func}.zip \
    --environment Variables='{ENV=aws}' \
    --region eu-west-2
done
```

### 5. Set Up API Gateway

```bash
# Create API Gateway
aws apigateway create-rest-api \
  --name MadzServerless-API \
  --region eu-west-2

# Import API configuration (update account IDs first)
sed 's/{ACCOUNT_ID}/YOUR_ACCOUNT_ID/g; s/{REGION}/eu-west-2/g' \
  config/api-gateway-template.json > config/api-gateway-deployment.json

aws apigateway put-rest-api \
  --rest-api-id YOUR_API_ID \
  --body file://config/api-gateway-deployment.json \
  --region eu-west-2

# Deploy to production
aws apigateway create-deployment \
  --rest-api-id YOUR_API_ID \
  --stage-name prod \
  --region eu-west-2
```

### 6. Set Up Custom Domain for API

```bash
# Create custom domain (after SSL cert is validated)
aws apigateway create-domain-name \
  --domain-name api.yourdomain.com \
  --certificate-arn arn:aws:acm:eu-west-2:YOUR_ACCOUNT:certificate/CERT_ID \
  --security-policy TLS_1_2 \
  --region eu-west-2

# Create base path mapping
aws apigateway create-base-path-mapping \
  --domain-name api.yourdomain.com \
  --rest-api-id YOUR_API_ID \
  --stage prod \
  --region eu-west-2
```

### 7. Set Up CloudFront Distribution

```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
  --distribution-config file://cloudfront-config.json

# Update DNS to point to CloudFront
aws route53 change-resource-record-sets \
  --hosted-zone-id YOUR_ZONE_ID \
  --change-batch file://dns-records.json
```

### 8. Upload Website Files

```bash
# Upload website files to S3
aws s3 sync s3/ s3://yourdomain.com/

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

## Configuration Files Needed

### s3-policy.json
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::yourdomain.com/*"
        }
    ]
}
```

### lambda-trust-policy.json
```json
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
```

## Environment Variables

- `ENV`: Set to "aws" for production, "local" for development

## Security Considerations

- All Lambda functions use IAM roles with minimal required permissions
- API Gateway has CORS properly configured
- S3 bucket only allows public read access to website files
- SSL certificates ensure all traffic is encrypted
- DynamoDB access is restricted to Lambda functions only

## Monitoring and Logging

- CloudWatch logs are automatically enabled for Lambda functions
- API Gateway access logs can be enabled for debugging
- CloudFront access logs can be configured for analytics

## Cost Optimization

- Lambda functions use minimal memory allocation
- DynamoDB uses on-demand billing
- CloudFront is configured for optimal caching
- S3 uses standard storage class for infrequent access

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure API Gateway CORS headers match website domain
2. **Certificate Validation**: DNS records must be added for ACM validation
3. **Lambda Permissions**: Ensure proper IAM roles are attached
4. **S3 Access**: Verify bucket policy allows public read access

### Useful Commands

```bash
# Check Lambda function logs
aws logs tail /aws/lambda/madz_get_a_song --follow

# Test API endpoint
curl https://api.yourdomain.com/prod/madz_get_all_songs

# Check certificate status
aws acm describe-certificate --certificate-arn YOUR_CERT_ARN --region us-east-1
```

## Backup and Recovery

- DynamoDB data should be backed up regularly
- Lambda function code is stored in this repository
- S3 website files can be restored from this repository
- Infrastructure can be rebuilt using these deployment scripts