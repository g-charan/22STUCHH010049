import requests # Make sure you have 'requests' installed: pip install requests

# (Paste the log function definition here from the previous response)

# Defining the end URL
TESTAPISERVER = "http://20.244.56.144/evaluation-service/logs"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJjaGFyYW5ndXR0aTIyQGlmaGVpbmRpYS5vcmciLCJleHAiOjE3NTMyNTc5MzIsImlhdCI6MTc1MzI1NzAzMiwiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6IjZhMDE0YjQ2LTE1ZjktNDgxMS04MDY1LTM0NDE4OTkxZTc5MSIsImxvY2FsZSI6ImVuLUlOIiwibmFtZSI6ImNoYXJhbiBndXR0aSIsInN1YiI6IjI0NmJhMjk1LTQ0ZWQtNDVlYi1hYjdhLTZlMGY4NTFiMjM0MCJ9LCJlbWFpbCI6ImNoYXJhbmd1dHRpMjJAaWZoZWluZGlhLm9yZyIsIm5hbWUiOiJjaGFyYW4gZ3V0dGkiLCJyb2xsTm8iOiIyMnN0dWNoaDAxMDA0OSIsImFjY2Vzc0NvZGUiOiJiQ3VDRlQiLCJjbGllbnRJRCI6IjI0NmJhMjk1LTQ0ZWQtNDVlYi1hYjdhLTZlMGY4NTFiMjM0MCIsImNsaWVudFNlY3JldCI6IkNRVFJ6WVJVS05jSEtwamgifQ.vIr5EzLn_HVh36HJOjb30V9igvrV6_wI36_t6laslKc"

# Writing the function here
def log(stack: str, level: str, pkg: str, message: str):
    request_payload = {
        "stack": stack,
        "level": level,
        "package": pkg,
        "message": message,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.post(TESTAPISERVER, headers=headers, json=request_payload)
        response.raise_for_status()
        print("Log sent successfully!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred during the request: {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Call the function exactly as you described:
log("backend", "info", "utils", "api working, connection established")