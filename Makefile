DEFAULT_PORT = /dev/tty.usbmodem0000000000001

upload:
	mpremote connect $(DEFAULT_PORT) cp i2c_device.py :
	mpremote connect $(DEFAULT_PORT) cp bmx160.py :
	mpremote connect $(DEFAULT_PORT) cp main.py :

console:
	mpremote connect $(DEFAULT_PORT)
