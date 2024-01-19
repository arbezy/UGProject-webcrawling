import os
import sys
import glob
import traceback


REMOVE_RETRANSMISSIONS = True
USE_TSHARK_TCP_PAYLOAD = False
SKIP_MALFORMED = True


class PacketInfo(object):
    def __init__(self):
        self.ts = 0.0
        self.src_ip = ""
        self.dst_ip = ""
        self.src_port = 0
        self.dst_port = 0
        self.proto = ""
        self.ip_payload_size = 0
        self.ip_hdr_len = 0
        self.tcp_hdr_len = 0
        self.tcp_payload_size = 0
        self.tcp_flags = ""
        self.tcp_options_tsval = 0
        self.tcp_options_tsecr = 0
        self.tcp_seq = 0
        self.tcp_ack = 0
        self.tcp_win_size = 0
        self.tcp_expert_msg = ""


def int_or_default(str_val, default_val=0):
    return int(str_val) if len(str_val) else default_val


def parse_tshark_output(tshark_out):
	packet_info_arr = []
	if not os.path.isfile(tshark_out):
		return packet_info_arr

	for line in open(tshark_out):
		packet_info = PacketInfo()
		try:
			if SKIP_MALFORMED and "Malformed Packet" in line:
				print("Skipping malformed packet")
				continue
			print(line)
			if REMOVE_RETRANSMISSIONS and "[Retransmission (suspected)]" in line:
				print("Removing retransmitted packet")
				continue
			line = line.strip()
			items = line.split("\t")
			packet_info.ts = float(items[0])
			packet_info.src_ip = items[1]
			packet_info.dst_ip = items[2]
			packet_info.src_port = items[3]
			packet_info.dst_port = items[4]
			packet_info.proto = items[5]
			if packet_info.proto != '6':  # must be TCP
				continue
			packet_info.ip_payload_size = int_or_default(items[6])
			packet_info.ip_hdr_len = int_or_default(items[7])
			packet_info.tcp_hdr_len = int_or_default(items[8])
			if USE_TSHARK_TCP_PAYLOAD:
				if "," in items[9]:
					# packets with multiple payloads appear as A,B
					payloads = items[9].split(",")
					packet_info.tcp_payload_size = sum(int(payload) for payload in payloads)
				else:
					packet_info.tcp_payload_size = int_or_default(items[9])
				if packet_info.tcp_payload_size > packet_info.ip_payload_size:
					print("TCP >  IP payload", packet_info.tcp_payload_size, packet_info.ip_payload_size)
			else:
				packet_info.tcp_payload_size = packet_info.ip_payload_size - (packet_info.ip_hdr_len + packet_info.tcp_hdr_len)

			packet_info.tcp_flags = items[10]
			assert "0x" in packet_info.tcp_flags
			packet_info.tcp_options_tsval = int_or_default(items[11])
			packet_info.tcp_options_tsecr = int_or_default(items[12])
			packet_info.tcp_seq = int_or_default(items[13])
			packet_info.tcp_ack = int_or_default(items[14])
			packet_info.tcp_win_size = int_or_default(items[15])
			if len(items) > 16:
				packet_info.tcp_expert_msg = items[16]
			packet_info_arr.append(packet_info)
		except Exception as exc:
			print("Exception:", tshark_out, exc, line)
			print(traceback.format_exc())
	return packet_info_arr


for f in glob.glob(os.path.join(sys.argv[1], '*.tshark')):
	packet_arr = parse_tshark_output(f)
	with open(f + '.csv', 'a+') as fo:
		for p in packet_arr:
			size = p.tcp_payload_size
			if size == 0:
				continue
			if p.src_ip == '192.168.1.16':
				pass
			elif p.dst_ip == '192.168.1.16':
				size = -size
			else:
				continue
			print(p.ts, size, file=fo)
