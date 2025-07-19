# App Store Review LLM AgentCore

An intelligent app review analysis service built with AWS Bedrock AgentCore and Strands AI agents. This service automatically scrapes, analyzes, and provides insights from Google Play Store app reviews using advanced language models.

## 🚀 Features

- **Automated App Discovery**: Find apps by name and retrieve their Google Play Store IDs
- **Review Scraping**: Extract up to 100 recent reviews from Google Play Store
- **Intelligent Analysis**: AI-powered sentiment analysis and issue identification
- **Multi-language Support**: Analysis results in both English and Chinese
- **AWS Integration**: Built on AWS Bedrock AgentCore for scalable deployment
- **Flexible Filtering**: Filter reviews by rating scores (1-5 stars)

## 🏗️ Architecture

This service is built using:
- **AWS Bedrock AgentCore**: Serverless runtime for AI agents
- **Strands AI**: Agent framework for tool orchestration
- **Claude 3.7 Sonnet**: Advanced language model for analysis
- **Google Play Scraper**: Review data extraction

## 📋 Prerequisites

- AWS Account with Bedrock AgentCore access
- Python 3.8+
- Required AWS permissions (see `role_policy_example.json`)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd appstore-review-llm-agentcore
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials**:
   ```bash
   aws configure
   ```

## 🚀 Usage

### Local Development

Run the service locally:
```bash
python app_reviews_agentcore_simple.py
```

### API Usage

The service accepts JSON payloads with the following parameters:

```json
{
    "app_name": "Calculator",
    "store": "Google Play",
    "country": "us",
    "rank": -1
}
```

**Parameters:**
- `app_name` (required): Name of the app to analyze
- `store` (optional): App store platform (default: "Google Play")
- `country` (optional): Country code for reviews (default: "us")
- `rank` (optional): Filter by star rating 1-5, -1 for all ratings (default: -1)

### Example Client Usage

```python
import boto3
import json

client = boto3.client('bedrock-agentcore')

payload = {
    "app_name": "Calculator",
    "store": "Google Play",
    "country": "us"
}

response = client.invoke_agent_runtime(
    agentRuntimeArn="your-agent-runtime-arn",
    qualifier="DEFAULT",
    payload=json.dumps(payload).encode()
)

for content in response["response"]:
    print(content)
```

## 📊 Output Format

The service returns a comprehensive analysis including:

- **Common Issues**: Identified problems mentioned in reviews
- **Rating Distribution**: Percentage breakdown of 1-5 star ratings
- **Sentiment Summary**: Overall user sentiment analysis
- **Bilingual Results**: Analysis in both English and Chinese

Example output structure:
```json
{
    "result": "Detailed analysis in markdown format...",
    "app_id": "com.example.calculator",
    "app_name": "Calculator",
    "store": "Google Play",
    "country": "us",
    "timestamp": "2024-01-01T12:00:00"
}
```

## 🔧 Configuration

### AWS Permissions

The service requires specific AWS permissions. Use the provided `role_policy_example.json` as a template:

- ECR access for container images
- CloudWatch Logs for monitoring
- Bedrock model invocation
- AgentCore workload access

### Environment Variables

Set the following environment variables if needed:
- `AWS_REGION`: AWS region (default: us-east-1)
- `LOG_LEVEL`: Logging level (default: INFO)

## 📁 Project Structure

```
appstore-review-llm-agentcore/
├── app_reviews_agentcore_simple.py  # Main service implementation
├── test_agentcore_client.py         # Example client code
├── requirements.txt                 # Python dependencies
├── role_policy_example.json         # AWS IAM policy template
├── output/                          # Generated review data (created at runtime)
└── README.md                        # This file
```

## 🔍 How It Works

1. **App Discovery**: The service searches Google Play Store for the specified app name
2. **Review Extraction**: Scrapes up to 100 recent reviews using google-play-scraper
3. **Data Processing**: Saves raw review data to JSON files in the `output/` directory
4. **AI Analysis**: Uses Claude 3.7 Sonnet to analyze reviews for:
   - Common issues and complaints
   - Rating distribution patterns
   - Overall sentiment trends
5. **Result Generation**: Returns formatted analysis in both English and Chinese

## 🚨 Error Handling

The service includes comprehensive error handling for:
- Invalid app names or IDs
- Network connectivity issues
- API rate limiting
- AWS service errors

## 📝 Logging

Detailed logging is provided for:
- Service initialization
- Review scraping progress
- Analysis completion
- Error conditions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🆘 Support

For issues and questions:
1. Check the logs for detailed error messages
2. Verify AWS permissions and credentials
3. Ensure all dependencies are properly installed
4. Review the example client code for proper usage

## 🔮 Future Enhancements

- Support for Apple App Store reviews
- Advanced sentiment analysis metrics
- Historical trend analysis
- Multi-language review processing
- Real-time monitoring dashboard