import requests

# Defining the Params here (Python's equivalent is type hints, but not enforced at runtime)
# For documentation purposes:
# class Params:
#     stack: str
#     level: str
#     pkg: str
#     message: str

# Defining the end URL
TESTAPISERVER = "http://20.244.56.144/evaluation-service/logs"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJjaGFyYW5ndXR0aTIyQGlmaGVpbmRpYS5vcmciLCJleHAiOjE3NTMyNTMxNTQsImlhdCI6MTc1MzI1MjI1NCwiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6IjQ3Njg0YzA3LTY2NGUtNDVhYS04YjhjLWNhNDk2Mjk3YzkyMCIsImxvY2FsZSI6ImVuLUlOIiIsIm5hbWUiOiJjaGFyYW4gZ3V0dGkiLCJzdWIiOiIyNDZiYTI5NS00NGVmLTQ1ZWItYWI3YS02ZTBmODUxYjIzNDAjIn0sImVtYWlsIjoiY2hhcmFuZ3V0dGkyMkBpZmhlaW5kaWEub3JnIiwibmFtZSI6ImNoYXJhbiBndXR0aSIsInJvbGxObyI6IjIyc3R1Y2hpMDEwMDQ5IiwiYWNjZXNzQ29kZSI6ImJDdUNGRlQiLCJjbGllbnRJRCI6IjI0NmJhMjk1LTQ0ZWQtNDVlYi1hYjdhLTZlMGY4NTFiMjM0MCIsImNsaWVudFNlY3JldCI6IkNRVFJ6WVJVS05jSEtwamgifQ.y_IOfyuBs1mMIfnQ6pui_RAQY38-3e6sNxDoT51JyVg"

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
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)
        print("Log sent successfully!") # Optional: confirmation message
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

# Example usage:
# log(
#     stack="Error in data processing service",
#     level="ERROR",
#     pkg="data-processor",
#     message="Failed to process batch ID 123 due to invalid format."
# )

# log(
#     stack="User registration successful",
#     level="INFO",
#     pkg="auth-service",
#     message="New user charan.gutti@ifheindia.org registered."
# )