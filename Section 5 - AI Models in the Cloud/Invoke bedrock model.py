import boto3
import json

# Create a session using your profile and region
session = boto3.Session(profile_name="robbarto", region_name="us-east-1")
bedrock_runtime = session.client("bedrock-runtime")

# Llama 3.3 70B requires an inference profile (not the raw foundation model ID)
model_id = "us.meta.llama3-3-70b-instruct-v1:0"

user_message = "explain where the hubble space telescope is located."

# Llama 3 prompt format for Bedrock
prompt = {
    "prompt": (
        "<|begin_of_text|>"
        "<|start_header_id|>user<|end_header_id|>\n\n"
        f"{user_message}<|eot_id|>"
        "<|start_header_id|>assistant<|end_header_id|>\n\n"
    ),
    "max_gen_len": 512,
    "temperature": 0.7,
}

try:
    invoke_kwargs = {
        "modelId": model_id,
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps(prompt),
    }
    response = bedrock_runtime.invoke_model(**invoke_kwargs)

    result = json.loads(response["body"].read())
    print("✅ Response from Llama 3.3 70B Instruct:\n")
    print(result["generation"])

except Exception as e:
    print("❌ Error invoking model:", e)
