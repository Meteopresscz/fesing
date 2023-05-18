import yaml
from collections import defaultdict
import struct
import logging

logger = logging.getLogger("fesing2mqtt")


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

def create_request(aid):
	header = b"\x01\x18"
	addr = aid.to_bytes(2,'big')
	reg = b"\x00\x01"
	crc = modcrc(header+addr+reg).to_bytes(2,'big')
	return header+addr+reg+crc

def read_param(spec,data,out):
	if spec['size'] == 1:
		aformat = "B"
	elif spec['size'] == 2:
		aformat = ">H"
	res = struct.unpack_from(aformat,data,offset=spec['offset'])[0]
	res += spec.get('shift',0)
	res *= spec.get('mult',1)
	out[spec['message']][spec['field']] = res

def read_all(specs,ser,aid):
	out = defaultdict(dict)
	request = create_request(aid)
	ser.write(request)
	header = ser.read(4)
	if len(header) == 0:
		raise ValueError(f"Did not received any data, is device connected and unit ID set correctly?")
	if len(header) < 4:
		raise ValueError(f"Expected 4 bytes, got {len(header)}")
	magic,nbytes = struct.unpack(">HH",header)
	if magic != 0x0118:
		raise ValueError(f"Wrong header: {header.hex()[:4]}")
	logger.debug(f"Will read {nbytes} bytes")
	data = ser.read(nbytes)
	logger.debug(f"Read {data.hex()}")
	crc = ser.read(2)
	logger.debug(f"CRC: {crc.hex()}")
	if not checkcrc(header+data+crc):
		raise ValueError(f"Wrong CRC")
	for spec in specs:
		read_param(spec, data, out)
	return dict(out)

