import json
import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List, Tuple

def load_apis(file_path: str) -> Dict:
    """
    Load API endpoints from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing API endpoints
        
    Returns:
        dict: Dictionary of API endpoints
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"API configuration file not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")

def test_api(name: str, api_config: Dict, timeout: int = 10) -> Tuple[bool, str]:
    """
    Test an API endpoint for availability.
    
    Args:
        name (str): Name of the API
        api_config (dict): API configuration including URL, method, headers, and body
        timeout (int): Request timeout in seconds
        
    Returns:
        tuple: (is_working, error_message)
    """
    try:
        method = api_config.get('method', 'GET').upper()
        url = api_config['url']
        headers = api_config.get('headers', {})
        body = api_config.get('body', None)

        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=body, timeout=timeout)
        else:
            return False, f"Unsupported HTTP method: {method}"

        if response.status_code == 200:
            return True, ""
        else:
            return False, f"Status code: {response.status_code}"
    except requests.Timeout:
        return False, "Request timed out"
    except requests.RequestException as e:
        return False, f"Request failed: {str(e)}"

def test_all_apis(apis: Dict) -> List[Dict]:
    """
    Test all API endpoints and return list of non-working APIs.
    
    Args:
        apis (dict): Dictionary of API endpoints to test
        
    Returns:
        list: List of dictionaries containing information about non-working APIs
    """
    non_working = []
    
    for name, api_config in apis.items():
        is_working, error = test_api(name, api_config)
        if not is_working:
            non_working.append({
                "name": name,
                "url": api_config['url'],
                "method": api_config.get('method', 'GET'),
                "error": error
            })
    
    return non_working

def create_email_content(non_working_apis: List[Dict]) -> Tuple[str, str]:
    """
    Create email subject and body based on API test results.
    
    Args:
        non_working_apis (list): List of non-working APIs
        
    Returns:
        tuple: (email_subject, email_body)
    """
    subject = "API Test Report"
    
    if not non_working_apis:
        body = "All APIs are working properly."
    else:
        body = "The following APIs are not working:\n\n"
        for api in non_working_apis:
            body += f"API: {api['name']}\n"
            body += f"URL: {api['url']}\n"
            body += f"Method: {api['method']}\n"
            body += f"Error: {api['error']}\n"
            body += "-" * 50 + "\n"
    
    return subject, body

def send_email(recipient: str, subject: str, body: str) -> None:
    """
    Send email using SMTP.
    
    Args:
        recipient (str): Recipient email address
        subject (str): Email subject
        body (str): Email body content
    """
    # Get email credentials from environment variables
    smtp_user = os.getenv("EMAIL_USER")
    smtp_pass = os.getenv("EMAIL_PASS")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    if not all([smtp_user, smtp_pass]):
        raise ValueError("Email credentials not found in environment variables")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

def main():
    """Main function to run the API monitoring script."""
    # Load environment variables
    load_dotenv()
    
    # Configuration
    api_config_file = "apis.json"
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    
    if not recipient_email:
        raise ValueError("Recipient email not found in environment variables")
    
    try:
        # Load and test APIs
        apis = load_apis(api_config_file)
        non_working_apis = test_all_apis(apis)
        
        # Create and send email report
        subject, body = create_email_content(non_working_apis)
        send_email(recipient_email, subject, body)
        
        print("API test completed and report sent successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()