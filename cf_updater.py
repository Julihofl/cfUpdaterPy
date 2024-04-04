import requests
import sys
import datetime
import enum

# Only change these variables
g_api_key = "<YOUR_API_KEY>"
g_zone_id = "<YOUR_ZONE_ID>"
g_record_names = ["www.domain.com", "domain.com", "first.domain.com", "second.domain.com"]
g_record_type = "A"

# Don't change anything from here on
g_ip_address = requests.get("https://api.ipify.org").text
g_header = {"Authorization": "Bearer " + g_api_key,}

class LogLevel(enum.Enum):
    INFO = "info"
    ERROR = "error"

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except requests.RequestException as e:
        write_log(LogLevel.ERROR, f"Failed to get public IP: {e}")
        return None

def get_dns_record_id(record_name):
    try:
        response = requests.get(f"https://api.cloudflare.com/client/v4/zones/{g_zone_id}/dns_records?type={g_record_type}&name={record_name}", headers=g_header)
        if response.status_code == 200:
            records = response.json()["result"]
            if records:
                return records[0]["id"]
            else:
                write_log(LogLevel.ERROR, "No matching DNS record found")
                return None
        else:
            write_log(LogLevel.ERROR, f"Failed to fetch DNS records: {response.text}")
            return None
    except requests.RequestException as e:
        write_log(LogLevel.ERROR, f"API request failed: {e}")
        return None

def check_dns_record(record_name):
    response = requests.get(f"https://api.cloudflare.com/client/v4/zones/{g_zone_id}/dns_records?type={g_record_type}&name={record_name}", headers=g_header)
    if response.status_code == 200:
        records = response.json()["result"]
        if records:
            return records[0]['content']  # Return the IP address of the DNS record
    return None

def update_dns_record():
    for record_name in g_record_names:
        record_name = record_name.strip()  # Removing leading/trailing whitespace
        dns_record_ip = check_dns_record(record_name)

        if dns_record_ip == g_ip_address:
            write_log(LogLevel.INFO, f"The IP address {g_ip_address} already matches the A record for {record_name}.")
            continue
        elif dns_record_ip is None:
            write_log(LogLevel.ERROR, f"Could not retrieve the DNS record for {record_name}.")
            continue

        record_id = get_dns_record_id(record_name)
        if not record_id:
            continue

        data = {
            "type": g_record_type,
            "name": record_name,
            "content": g_ip_address,
            "ttl": 1,
            "proxied": False
        }

        try:
            response = requests.put(f"https://api.cloudflare.com/client/v4/zones/{g_zone_id}/dns_records/{record_id}", json=data, headers=g_header)
            if response.status_code == 200:
                write_log(LogLevel.INFO, f"DNS record for {record_name} updated successfully with ip {g_ip_address}.")
            else:
                write_log(LogLevel.ERROR, f"Failed to update DNS record for {record_name}: {response.text}")
        except requests.RequestException as e:
            write_log(LogLevel.ERROR, f"API request failed for {record_name}: {e}")

def write_log(level, message):
    current_time = datetime.datetime.now()
    message = f"{current_time:%Y-%m-%d %H:%M:%S} - {message}"
    if level == LogLevel.INFO:
        print(message)
    elif level == LogLevel.ERROR:
        print(message, file=sys.stderr)
    else:
        print(message)

if __name__ == "__main__":
    update_dns_record()
    print("###################################################################################################################")