import os
import asyncio
import logging
import sys
import requests
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)s]: %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)

# Extract environment variables for API URLs, keys, and timeout
SONARR_API_URL = f"{os.environ['SONARR_URL']}/api/v3"
RADARR_API_URL = f"{os.environ['RADARR_URL']}/api/v3"
SONARR_API_KEY = os.environ['SONARR_API_KEY']
RADARR_API_KEY = os.environ['RADARR_API_KEY']
API_TIMEOUT = int(os.environ['API_TIMEOUT']) # seconds
CLEAN_LIST = {}

# Function to make API requests
async def make_api_request(type, url, api_key, params=None):
    try:
        headers = {'X-Api-Key': api_key}
        # Make the API request asynchronously
        response = None
        if type == 'get':
            response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url, params=params, headers=headers))
        else:
            response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.delete(url, params=params, headers=headers))

        response.raise_for_status()  # Raise exception for non-200 status codes

        if type == 'get':
            return response.json()  # Parse JSON response
        else:
            return
        
    except (RequestException, ValueError) as e:
        if e.response.status_code == 404:
            return None
        
        logging.error(f'❌ Failed {type}-request to {url}. Reason: {e}')
        return None

# Function to remove stalled downloads
async def remove_stalled_downloads(api_url, api_key, service):
    logging.info(f'👀 Checking {service}')
    CLEAN_LIST = {}
    queue_url = f'{api_url}/queue'
    # Retrieve queue information
    queue = await make_api_request('get', queue_url, api_key, {'page': '1', 'pageSize': await count_records(api_url, api_key)})
    if queue is not None and 'records' in queue:
        # Iterate through queue items
        for item in queue['records']:
            if all(key in item for key in ['title', 'status', 'trackedDownloadStatus']):
                # Check for stalled downloads
                if item['title'] not in CLEAN_LIST and item['status'] == 'warning' and item['errorMessage'] == 'The download is stalled with no connections':
                    logging.info(f'🧹 Cleaning {item["title"]}')
                    # Remove stalled download
                    await make_api_request('delete', f'{api_url}/queue/{item["id"]}', api_key, {'removeFromClient': 'true', 'blocklist': 'true'})
                    CLEAN_LIST[item['title']] = 'yes'
            else:
                logging.warning(f'🚩 Skipping item in {service} (missing or invalid keys)')
    else:
        logging.warning(f'🚩 {service} queue is empty (no requests?)')
    logging.info(f'✨ Finished cleaning {service}')

# Function to count records in the queue
async def count_records(api_url, api_key):
    queue_url = f'{api_url}/queue'
    queue = await make_api_request('get', queue_url, api_key)
    return queue.get('totalRecords', 0) if isinstance(queue, dict) else 0  # Ensure queue is a dictionary

# Function to convert seconds to hours and minutes
def seconds_to_hours_minutes(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours == 0 and minutes == 0:
        return f"{seconds} second{'s' if seconds != 1 else ''}"
    return ' '.join([f"{t} {unit}{'s' if t != 1 else ''}" for t, unit in zip([hours, minutes], ['hour', 'minute']) if t])

# Main function
async def main():
    while True:
        logging.info('')
        logging.info('🧼 Ready to clean')
        await remove_stalled_downloads(SONARR_API_URL, SONARR_API_KEY, 'Sonarr')
        await remove_stalled_downloads(RADARR_API_URL, RADARR_API_KEY, 'Radarr')
        logging.info(f'🛀 Taking a break for {seconds_to_hours_minutes(API_TIMEOUT)}')
        logging.info('')
        await asyncio.sleep(API_TIMEOUT)

# Entry point
if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('👋 Script stopped')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
