# 🚀 Amazon Bedrock Prompt Deployment Pipeline
A fully automated pipeline that uses Amazon Bedrock (Claude 3 Sonnet) to generate HTML content from prompt templates and deploys them using GitHub Actions to S3 static websites — with support for beta and production environments.

 ## This pipeline supports:

✅ AI-generated prompts using AWS Bedrock
✅ Dynamic homepage generation listing all outputs
✅ CI/CD via GitHub Actions
✅ S3 bucket hosting for beta and prod environments


## 🧾 Project Overview
This project automates the deployment of AI-generated educational prompts using:

Amazon Bedrock (Anthropic Claude 3 Sonnet)
AWS S3 for static website hosting
GitHub Actions for continuous integration and delivery
IAM roles and secrets management
You can edit prompt templates or variables, open a Pull Request to deploy to beta , and merge to main to deploy to production .

## 🛠 Prerequisites
Before getting started, ensure you have:

📦 An AWS account with access to Bedrock and S3
🔑 AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
🌍 Region set to us-east-1 (required for Bedrock model access)
🧱 Python 3.10+ installed locally
🧪 Git and GitHub CLI (or VS Code) installed
🎯 A GitHub repository initialized and connected to your local project


## 🧩 Folder Structure
``` bash
prompt-deployment-pipeline/
├── .github/
│   └── workflows/
│       ├── on_merge.yml
│       └── on_pull_request.yml
├── beta/
│   └── outputs/
│       ├── welcome_jordan.html
│       └── welcome_sam.html
├── outputs/
│   └── output_list.json
├── prompt_templates/
│   └── welcome_email.txt
├── prompts/
│   └── welcome_prompt.json
├── index.html
├── process_prompt.py
├── README.md
├── requirements.txt
└── .gitignore
```


## 📦 How It Works
You define prompt templates in prompt_templates/.
Configuration files in prompts/ contain variable values and model settings.
When you make a change and open a Pull Request , the on_pull_request.yml workflow runs:
Renders the prompt using Bedrock
Uploads generated .html files to the beta S3 bucket
Updates output_list.json and uploads it to S3
Uploads index.html to the root of the bucket
When you merge to main , the on_merge.yml workflow runs:
Repeats the process but uploads to the prod bucket
Both buckets are configured for static website hosting , and your homepage lists all available .html files using JavaScript and JSON.


## 🧰 Step-by-Step Setup Guide
1. 🔹 Create S3 Buckets
Create two S3 buckets:

pixel-learning-beta
pixel-learning-prod
Make sure both buckets:

Enable Static Website Hosting
Set Index Document to index.html
Allow public read access (via bucket policy)
Example Bucket Policy (for public read):

``` bash
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```


2. 🔹 Configure IAM Role for GitHub Actions
Create an IAM user in AWS with this policy:

``` bash

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::pixel-learning-beta/*",
        "arn:aws:s3:::pixel-learning-prod/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "arn:aws:bedrock:us-east-1:ACCOUNT_ID:model/anthropic.claude-3-sonnet-20240229-v1:0"

    }
  ]
}

```
Attach this policy to your IAM user used by GitHub Actions.

3. 🔹 Request Access to Bedrock Model
Go to the AWS Bedrock Console and request access to:
``` bash
anthropic.claude-3-sonnet-20240229-v1:0
```
Wait for AWS approval before running the script.

4. 🔹 Configure GitHub Secrets
In your GitHub repo → Settings → Secrets and variables → Actions

These allow your GitHub Actions workflows to securely interact with AWS.


5. 🔹 Create Prompt Templates
Prompt templates use placeholders like {name} which are replaced at runtime.

Example Template: prompt_templates/welcome_email.txt
``` bash
Hi {name},

Welcome to Pixel Learning Co! We're excited to have you here.

Here's what we recommend you do next:
- Review your course syllabus
- Set up your learning schedule
- Explore our resources

Best,
Pixel Learning Team

```
6. 🔹 Create Prompt Config Files
Configuration files tell the script which template to use and where to save the output.

Example Config: prompts/welcome_prompt.json

``` bash
{
  "template": "welcome_email.txt",
  "variables": {
    "name": "Jordan"
  },
  "output_file": "welcome_jordan.html",
  "max_tokens": 500
}
```
You can add more .json config files to generate additional prompts.

7. 🔹 Write the Prompt Processing Script
The core logic is in process_prompt.py. Here's a snippit:

``` bash

import boto3
import json
import os

# Load configuration
CONFIG_FILE = "prompts/welcome_prompt.json"
OUTPUT_DIR = "outputs/"

def render_prompt(template_path, variables):
    with open(template_path, 'r') as f:
        template = f.read()
    return template.format(**variables)

def invoke_bedrock_model(prompt):
    client = boto3.client(
        service_name='bedrock',
        region_name='us-east-1'
```
8. 🔁 Create GitHub Actions Workflows on_merge.yml and on_pull_request.yml

   ## 🌐 View Output in S3 Static Websites
   http://pixel-learning-prod.s3-website-us-east-1.amazonaws.com/
   ![image](https://github.com/user-attachments/assets/8f34b1d6-8451-4e28-98b7-0146107f86ac)

   ![image](https://github.com/user-attachments/assets/633f6dc1-7131-49e8-8301-6e32e8c1e7f7)

