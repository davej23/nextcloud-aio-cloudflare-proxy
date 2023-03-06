'''
Update DNS Record for Domain [Remove Proxy]
'''

from cloudflare import CloudFlare
from dotenv import load_dotenv
import os
import time

load_dotenv()

api_email = os.getenv("EMAIL")
api_secret = os.getenv("KEY")
api_domain = os.getenv("DOMAIN")

cf = CloudFlare(api_email, api_secret, api_domain, proxied=False)
cf.headers = {
    'Authorization': f'Bearer {api_secret}',
    'X-Auth-Email': api_domain
}
cf.sync_dns_from_my_ip()


'''
Restart Apache Docker Container
'''

os.system('docker restart nextcloud-aio-apache')
time.sleep(60)  # Sleep for 60s until container restarted and updated cert


'''
Re-enable Proxy on Domain
'''

cf = CloudFlare(api_email, api_secret, api_domain, proxied=True)
cf.headers = {
    'Authorization': f'Bearer {api_secret}',
    'X-Auth-Email': api_domain
}
cf.sync_dns_from_my_ip()
