import requests, re
from bs4 import BeautifulSoup
import time
from IPython.display import clear_output
        
def check_proxies(proxies):
    url = 'https://ipecho.net/plain'
    working = 0
    with open('working_proxies.txt', 'w') as file:
        for proxy in proxies:
            try:
                # https://ipecho.net/plain returns the ip address
                # of the current session if a GET request is sent.
                page = requests.get(
                  url, proxies={"http": proxy, "https": proxy}, timeout=5)
                if page.status_code == 200:
                    file.write(proxy+'\n')
                    working+=1
                    print(working, end = ' ', flush = True)
            except requests.RequestException:  # Catch all request-related errors
                continue

def main():
    regex = r"[0-9]+(?:\.[0-9]+){3}:[0-9]+"
    c = requests.get("https://spys.me/proxy.txt")
    test_str = c.text
    a = re.finditer(regex, test_str, re.MULTILINE)
    with open("proxies_list.txt", 'w') as file:
        for i in a:
           print(i.group(),file=file)

    d = requests.get("https://free-proxy-list.net/")
    soup = BeautifulSoup(d.content, 'html.parser')
    td_elements = soup.select('.fpl-list .table tbody tr td')
    ips = []
    ports = []
    proxies = []

    for j in range(0, len(td_elements), 8):
        ips.append(td_elements[j].text.strip())
        ports.append(td_elements[j + 1].text.strip())

    with open("proxies_list.txt", "a") as myfile:
        for ip, port in zip(ips, ports):
            proxy = f"{ip}:{port}"
            proxies.append(f"{ip}:{port}")
            
    check_proxies(proxies)
            
if __name__ == '__main__':
    main()
    print('done')