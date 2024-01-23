# UG Project webcrawling
CONTAINERISED SELENIUM WEBCRAWLER

To use first create a docker container using docker build. When the container is up and running, run the shell script in the container to capture web traffic for the supplied websites, then use the parser to parse the .pcap files into .tshark files, which can then be converted to .csv files ! It might be helpful to mount a volume if you want captured traffic to be persistant.
