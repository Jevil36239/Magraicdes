import sys, time, random, requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from sys import platform
from colorama import init, Fore, Back, Style

__author__      = "Jevil36239"
__github__      = "github.com/Jevil36239"
__Finished__    = "22 - Maret - 2023"
__name__        = "Mass Grab IPs by Country codes"

# Kode Warna buat text.

GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
BLUE = '\033[34m'
RESET = '\033[0m'

# Kode warna buat warnain daftar kode negara, soalnya nanti make random buat warnain textnya.

colors = [Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
RESET = Style.RESET_ALL

# Ya biasa gabut cuma buat ngecek Running System aja.
if platform == "linux" or platform == "linux2":
    SYS_MSG = "Running on Linux"
elif platform == "darwin":
    SYS_MSG = "Running on Mac OS"
elif platform == "win32":
    SYS_MSG = "Running on Windows"
else:
    SYS_MSG = "Unknown system"


# Bagian intro yang nampilin loading messages

LOADING_MSGS = [
    "Loading...",
    "Please wait...",
    "Please dont recode it bro",
    "Dont sell this code bro",
    "Just fucking obey my messages",
    "not gonna obey? it's okay I understand.",
]


sys.stdout.write(YELLOW + SYS_MSG + RESET + '\n\n')
sys.stdout.flush()
time.sleep(1)


for i in range(10):
    loading_msg = random.choice(LOADING_MSGS)
    sys.stdout.write(BLUE + loading_msg + RESET)
    sys.stdout.flush()
    time.sleep(0.2)
    sys.stdout.write('\b' * len(loading_msg) + ' ' * len(loading_msg) + '\b' * len(loading_msg))
    sys.stdout.flush()


msg0=('''
                \||/
                |  !___oo   _  _ ____ ____ ____ ____ _ ____ ___  ____ ____ 
      /\  /\   / (__,,,,|   |\/| |__| | __ |__/ |__| | |    |  \ |___ [__  
     ) /^\) ^\/ _)          |  | |  | |__] |  \ |  | | |___ |__/ |___ ___] 
     )   _ /  / _)     ___________(- Mass Grab IPs by Country codes
 /\  )/\/ ||  | )_)                      
<  >      |(,,) )__)
 ||      /    \)___)\       
 | \____(      )___) )___
  \______(_______;;; __;;;  - github.com/Jevil36239 
  
''') # banner inspired from github.com/Snifer/EIPO


# Mager ngehias warna, jadinya ninggal implentasi ( nempel ) text di ascii art biar ada warnanya.

for i in msg0:
    if i == '-':
        sys.stdout.write(RED + i + RESET)
    elif i == '(' or i == ')':
        sys.stdout.write(BLUE + i + RESET)
    elif i == '<' or i == '>':
        sys.stdout.write(YELLOW + i + RESET)
    elif i.isupper():
        sys.stdout.write(GREEN + i + RESET)
    else:
        sys.stdout.write(i)
    sys.stdout.flush()
    time.sleep(0.001)


def get_country_codes():
    # Bagian ini ngambil list kode negara di web iphu.com terus ngescrape bagian kode negara sama jumlah IP.

    url = 'https://en.ipshu.com/country-list?page='
    page_num = 1 
    country_codes = []
    while True:
        response = requests.get(url + str(page_num))
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        if len(rows) <= 1: 
            break
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                country_code = cols[0].text.strip()
                num_ips = cols[2].text.strip()
                country_codes.append((country_code, num_ips))
        page_num += 1
    return country_codes





def get_ips_by_country(country_code, num_pages):
    # Bagian ini buat ngescrape isi IP di setiap pages pada suatu negara, itu pun scrapenya juga ada hitungan ip dari tabel start IP ke end IP
    # Jadi ga cuma ngescrape cuma berdasarkan display tabel start IP sama end IP
    # Ini juga ngitung ada berapa ip Kalo diitung dari tabel start IP ke end IP

    # dan juga salah satu alasan kenapa dapet resultsnya banyak :V

    ips = []
    for page in tqdm(range(1, num_pages+1), desc='Scraping Pages', unit='page'):
        url = f'https://en.ipshu.com/ip-country/{country_code}?page={page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for row in soup.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) > 1:
                start_ip = cols[0].text.strip()
                end_ip = cols[1].text.strip()
                if '-' in start_ip and '-' in end_ip:
                    start_ip_parts = start_ip.split('.')
                    end_ip_parts = end_ip.split('.')
                    for i in range(int(start_ip_parts[3]), int(end_ip_parts[3])+1):
                        ip = f'{start_ip_parts[0]}.{start_ip_parts[1]}.{start_ip_parts[2]}.{i}'
                        ips.append(ip)
                else:
                    if '-' in start_ip:
                        start_ip = start_ip.split('-')[0]
                    if '-' in end_ip:
                        end_ip = end_ip.split('-')[1]
                    start_ip_parts = start_ip.split('.')
                    end_ip_parts = end_ip.split('.')
                    for i in range(int(start_ip_parts[3]), int(end_ip_parts[3])+1):
                        ip = f'{start_ip_parts[0]}.{start_ip_parts[1]}.{start_ip_parts[2]}.{i}'
                        ips.append(ip)
    return ips



country_codes = get_country_codes()
country_codes.sort() #sort() buat nyusun listnya biar jadi alfabet
print(Fore.BLUE + "Available country codes:")


# Perapian buat displays daftar kode negara sama jumlah IP.

for i in range(0, len(country_codes), 4): 
    codes = []
    for j in range(i, min(i+4, len(country_codes))):
        code, num_ips = country_codes[j]
        color = random.choice(colors) # dan ini bagian randomized colornya.
        codes.append(color + "{:<5} {:<20}".format(code, num_ips) + RESET)
    print("  ".join(codes))



country_code = input('Enter a two-letter country code (e.g. US): ')
num_pages = int(input('Enter the number of pages to scrape: '))

ips = get_ips_by_country(country_code, num_pages)
total_ips = len(ips)
with open(f'{country_code}_ips.txt', 'w') as f:
    for ip in tqdm(ips, desc='Saving IPs', unit='ip', total=total_ips): #buat progress barnya dari module tqdm
        f.write(f'{ip}\n')

# Buat ngitung total ip yang ke scrape
print(f'Total number of IP addresses: {total_ips}')
