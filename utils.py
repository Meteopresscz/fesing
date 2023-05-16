import yaml
from collections import defaultdict


def modcrc(buf):
	crc = 0xFFFF;
	for pos in range(len(buf)):
		crc ^= buf[pos]
		for i in range(7,-1,-1):
			if ((crc & 0x0001) != 0):
				crc >>= 1
				crc ^= 0xA001
			else:
				crc >>= 1
	return (crc>>8) | ((crc&0xff)<<8)
 
def checkcrc(buf):
	payload = buf[:-2]
	crc = modcrc(payload)
	#crc &= 0x7F7F
	expected = buf[-2] * 256 + buf[-1]
	if crc != expected:
		#print("CRC mismatch, got %04X expected %04X"%(crc, expected))
		return False
	return True



def load_specs(filename):
	with open(filename) as f:
		loader = yaml.Loader(f)
		specs = loader.get_data()
	return specs
