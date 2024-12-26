# API Monitoring System

This Python script monitors multiple APIs and sends email reports about their status.

## Features
- Tests multiple API endpoints (GET and POST requests)
- Sends email reports about non-working APIs
- Supports custom headers and request bodies
- Secure credential management using environment variables

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/api-monitoring.git

2.   Install required packages:
  pip install -r requirements.txt

3. Create .env file:

*  Copy default.env to .env
*  Update with your credentials

    cp default.env .env

Update apis.json with your API endpoints:
jsonCopy{
    "API_Name": {
        "url": "https://api.example.com",
        "method": "GET"
    }
}

Run the script:

    python script.py



Configuration

    .env: Email credentials and SMTP settings
    apis.json: API endpoints and configurations

Note
Make sure to:

    1. Generate an App Password if using Gmail
    2. Never commit your actual .env file
    3. Keep apis.json updated with valid endpoints