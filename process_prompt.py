import json
import os
import boto3
from anthropic import AnthropicBedrock

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

# --- Call Amazon Bedrock ---
client = AnthropicBedrock(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_region=os.getenv("AWS_REGION")
)

response = client.messages.create(
    model="anthropic.claude-3-sonnet-20240229-v1:0",
    max_tokens=config["max_tokens"],
    messages=[
        {
            "role": "user",
            "content": f"Human: {prompt}"
        }
    ],
    anthropic_version="bedrock-2023-05-31"
)

generated_text = response.content[0].text

# --- Save Output ---
output_path = os.path.join(OUTPUT_DIR, config['output_file'])
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(output_path, 'w') as f:
    f.write(generated_text)

print(f"✅ Output saved to {output_path}")