import requests

def send_log(message):
    url = "https://eodxk8e2io7oo5d.m.pipedream.net"
    payload = {"message": message}
    response = requests.post(url, json=payload)
    print(f"Log sent. Status code: {response.status_code}")

# Example usage
send_log("This is a test log from my script")