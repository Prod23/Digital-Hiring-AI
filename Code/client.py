import requests

# Server URL
server_url = 'http://127.0.0.1:5002'

# Function to get the Google Drive link from the server
def get_drive_link():
    endpoint = f'{server_url}/get_drive_link'
    response = requests.post(endpoint)
    if response.status_code == 200:
        data = response.json()
        drive_link = data.get('drive_link')
        print(f"Received drive link: {drive_link}")
    else:
        print("Failed to retrieve drive link from the server.")

if __name__ == '__main__':
    # Get the Google Drive link from the server
    get_drive_link()



