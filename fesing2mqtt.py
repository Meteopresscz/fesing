import sys
import serial
import struct
import time
import pprint as pp
from collections import defaultdict

from utils import checkcrc, load_specs


REQUEST = bytes.fromhex("01 18 00 00 00 01 e0 08")

specs = load_specs("fesing.yaml")

pp.pprint(specs)


def read_param(spec,data,out):
	if spec['size'] == 1:
		aformat = "B"
	elif spec['size'] == 2:
		aformat = ">H"
	res = struct.unpack_from(aformat,data,offset=spec['offset'])[0]
	res += spec.get('shift',0)
	res *= spec.get('mult',1)
	out[spec['message']][spec['field']] = res



ser = serial.Serial(sys.argv[1], baudrate=9600)
out = defaultdict(dict)

while True:
	ser.write(REQUEST)
	header = ser.read(4)
	magic,nbytes = struct.unpack(">HH",header)
	if magic != 0x0118:
		print(f"Wrong header: {header.hex()[:4]}")
		time.sleep(5)
		continue
	print(f"Will read {nbytes} bytes")
	data = ser.read(nbytes)
	print(f"Read {data.hex()}")
	crc = ser.read(2)
	print(f"CRC: {crc.hex()}")
	if checkcrc(header+data+crc):
		print("CRC OK")
		for spec in specs:
			read_param(spec, data, out)
		pp.pprint(out)
	else:
		print("CRC FAIL")
	time.sleep(5)

