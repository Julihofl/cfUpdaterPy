# Cloudflare DNS Updater for Raspberry Pi
This is only a fork. All credits go to the original creator.

## Overview
This Python script updates DNS records in Cloudflare. It retrieves the public IP address of the user's machine using the ipify service and updates a specified DNS record in Cloudflare with this IP address.

## Features
- Retrieves the current public IP address.
- Updates a specified DNS record in Cloudflare with the current IP.

## Prerequisites
- Python 3.x
- `requests` library (Install using `pip install requests`)

## Setup
1. Clone or download this repository to your local machine.
2. Install the required Python packages: `pip install requests`.

## Configuration
1. Before running the script, ensure you have the following Cloudflare account details:
- API Key (Your API Key needs to have read and write permissions)
- Zone ID of the domain
- Record Name and Record Type you wish to update
2. Enter your informations into the respective variables inside the `cf_updater.py` file.

## Usage
1. Run the script using Python: `python cf_updater.py`.
2. Results will be output on the console.

## Auto Update using cronjobs
1. Type in terminal:
```
crontab -e
```
2. Insert at the bottom:
```
*/5 * * * * /usr/bin/python /path/to/file.py
```
This will run the python script every 5 minutes.

3. If you wish to log the output of the script use this:
```
*/5 * * * * /usr/bin/python /path/to/file.py >> /path/to/file.log 2>&1
```
This will redirect all output to the provided log file.

## Troubleshooting
- Ensure all entered credentials and information are correct. 
- Make sure your Cloudflare API key has the necessary permissions. If you're having trouble with Zone keys, use Global API key.
- Check your internet connection if the script fails to retrieve the public IP.

## License
[MIT License](LICENSE.md)
