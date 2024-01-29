# UG Project webcrawling
CONTAINERISED SELENIUM WEBCRAWLER

To use first create a docker container using docker build, next run the container using 'docker run -p 4444:4444/tcp -p 4444:4444/udp --shm-size=2gb IMAGENAME'. When the container is up and runnin, run the shell script in the container to capture web traffic for the supplied websites (in urls.txt), then use the parser to parse the .pcap files into .tshark files, which can then be converted to .csv files ! It might be helpful to mount a volume if you want captured traffic to be persistant.

Crawler will visit a site, take a screenshot, wait for 5 seconds then close. Capturing all traffic as it does.
