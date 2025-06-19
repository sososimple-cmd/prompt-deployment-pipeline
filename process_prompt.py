import json
import os
import boto3

# --- Configuration ---
CONFIG_FILE = "prompts/welcome_prompt.json"
TEMPLATE_DIR = "prompt_templates"
OUTPUT_DIR = "outputs"

# --- Load Config ---
with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)

template_path = os.path.join(TEMPLATE_DIR, config['template'])
with open(template_path, 'r') as f:
    template = f.read()

# --- Fill Template with Variables ---
prompt = template.format(**config['variables'])

# --- Call Amazon Bedrock using Boto3 ---
client = boto3.client(
    service_name='bedrock-runtime',
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": config["max_tokens"],
    "messages": [
        {
            "role": "user",
            "content": f"Human: {prompt}"
        }
    ]
}

response = client.invoke_model(
    modelId="anthropic.claude-3-sonnet-20240229-v1:0",
    contentType="application/json",
    accept="application/json",
    body=json.dumps(body)
)

response_body = json.loads(response.get('body').read())
generated_text = response_body['content'][0]['text']

# --- Save Output ---
output_path = os.path.join(OUTPUT_DIR, config['output_file'])
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(output_path, 'w') as f:
    f.write(generated_text)

print(f"✅ Output saved to {output_path}")