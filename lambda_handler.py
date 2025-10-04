import json
import base64
import subprocess
import threading
import time
import requests
import os
from io import StringIO
import sys

def start_streamlit():
    """Start Streamlit app in a separate thread"""
    try:
        # Change to the app directory
        os.chdir('/var/task')
        
        # Start Streamlit
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 
            'streamlit_app.py',
            '--server.port=8501',
            '--server.address=0.0.0.0',
            '--server.headless=true',
            '--browser.gatherUsageStats=false',
            '--logger.level=error'
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for Streamlit to start
        time.sleep(5)
        
        return process
    except Exception as e:
        print(f"Error starting Streamlit: {e}")
        return None

def wait_for_streamlit(max_retries=30):
    """Wait for Streamlit to be ready"""
    for i in range(max_retries):
        try:
            response = requests.get('http://localhost:8501/healthz', timeout=1)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

# Global variable to hold the Streamlit process
streamlit_process = None

def handler(event, context):
    """AWS Lambda handler function"""
    global streamlit_process
    
    try:
        # Start Streamlit if not already running
        if streamlit_process is None:
            print("Starting Streamlit app...")
            streamlit_process = start_streamlit()
            
            if not wait_for_streamlit():
                return {
                    'statusCode': 500,
                    'body': json.dumps({'error': 'Failed to start Streamlit app'})
                }
        
        # Handle different types of requests
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query_params = event.get('queryStringParameters') or {}
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        # Construct the full URL
        url = f"http://localhost:8501{path}"
        if query_params:
            query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
            url += f"?{query_string}"
        
        # Forward the request to Streamlit
        if http_method == 'GET':
            response = requests.get(url, headers=headers, timeout=30)
        elif http_method == 'POST':
            response = requests.post(url, headers=headers, data=body, timeout=30)
        elif http_method == 'PUT':
            response = requests.put(url, headers=headers, data=body, timeout=30)
        elif http_method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        # Handle binary content
        is_binary = False
        content_type = response.headers.get('Content-Type', '')
        binary_types = ['image/', 'application/pdf', 'application/zip', 'application/octet-stream']
        
        if any(bt in content_type for bt in binary_types):
            is_binary = True
            body = base64.b64encode(response.content).decode('utf-8')
        else:
            body = response.text
        
        # Return the response
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': body,
            'isBase64Encoded': is_binary
        }
        
    except Exception as e:
        print(f"Error in Lambda handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# For local testing
if __name__ == "__main__":
    # Test event
    test_event = {
        'httpMethod': 'GET',
        'path': '/',
        'queryStringParameters': None,
        'headers': {},
        'body': ''
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))