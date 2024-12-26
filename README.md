API Monitoring System
This Python script monitors multiple APIs and sends email reports about their status.

Features
Tests multiple API endpoints (GET and POST requests)
Sends email reports about non-working APIs
Supports custom headers and request bodies
Secure credential management using environment variables
Setup
Clone the repository:

git clone https://github.com/your-username/api-monitoring.git
Install required packages:

pip install -r requirements.txt
Create and configure the .env file:

cp default.env .env
Update the .env file with your credentials.
Update apis.json with your API endpoints:

JSON
{
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
Notes
Generate an App Password if using Gmail.
Never commit your actual .env file.
Keep apis.json updated with valid endpoints.
