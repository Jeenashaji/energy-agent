# Deploying the API on AWS (App Runner)

Template for the deployment step. AWS consoles change — follow the current AWS docs alongside it.
Delete the resources afterwards to avoid costs.

1. Build and test the container locally
   ```bash
   docker build -t energy-agent .
   docker run -p 8000:8000 --env-file .env energy-agent
   # open http://127.0.0.1:8000/docs
   ```
2. Create an ECR repository (Elastic Container Registry) and push the image
   ```bash
   aws ecr create-repository --repository-name energy-agent
   aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
   docker tag energy-agent <account>.dkr.ecr.<region>.amazonaws.com/energy-agent:latest
   docker push <account>.dkr.ecr.<region>.amazonaws.com/energy-agent:latest
   ```
3. Create an App Runner service from that image, port 8000.
   Store `GOOGLE_API_KEY` in AWS Secrets Manager and reference it as an environment variable —
   never bake the key into the image.
4. Test: `curl -X POST https://<service-url>/ask -H "Content-Type: application/json" -d '{"question":"Describe the data"}'`

## Option: use Amazon Bedrock instead of Gemini
Install `langchain-aws`, set `MODEL=bedrock_converse:<model-id>` and give the App Runner instance
role permission to call Bedrock. No API key needed then — access is controlled by IAM.
