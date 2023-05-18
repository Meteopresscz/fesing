import sys
import serial
import time
import pprint as pp
import logging

from utils import load_specs, read_all

UNIT_ID = 1

logging.basicConfig(level=logging.DEBUG)

specs = load_specs("fesing.yaml")
#pp.pprint(specs)

ser = serial.Serial(sys.argv[1], baudrate=9600, timeout=2)

while True:
	try:
		data = read_all(specs, ser, UNIT_ID)
		pp.pprint(data)
	except ValueError as e:
		print(f"Error in communication: {e}")
	
	time.sleep(5)

