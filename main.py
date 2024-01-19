import sys
from selenium import webdriver
from time import sleep

from dumputils import *
from common import *
from utils import *


# args should be ?(self?), visit_number, url_visited 
i, url = sys.argv[1:3]
print(f'Visit {i} to {url}')
# EARLY QUIC WFP PAPER USED CHROME RATHER THAN FIREFOX
# http://172.17.0.2:4444
# http://localhost:4444
# check this is correct too....
# todo: change selenium to use quic etc
with webdriver.Remote("http://localhost:4444", options=webdriver.ChromeOptions()) as driver:
    sleep(2)
    site = url.split('//')[1].split('.')[0]
    fname = f'/usr/src/app/results/{i}_{site}.pcap'
    with Sniffer(path=fname, filter=DEFAULT_FILTER):
        driver.get(url)
        sleep(5)
