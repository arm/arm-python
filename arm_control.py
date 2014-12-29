import sys, time

sys.path.insert(0, "../lib")
import serial, Leap

servo_bounds = {
	'pinch': (90, 180),
	'wrist': (0,180),
}

leap_bounds = {
	'pinch': (0, 1),
	'wrist': (-90,90),
}

class Listener(Leap.Listener):
	def on_init(self, controller):
		print "Initialized Leap Motion"

	def on_connect(self, controller):
		print "Connected to Leap Motion"

	def on_disconnect(self, controller):
		# Note: not dispatched when running in a debugger.
		print "Disconnected from Leap Motion"

	def on_exit(self, controller):
		print "Exited"

	def on_frame(self, controller):
		frame = controller.frame()
		if frame.hands:
			hand = frame.hands.rightmost
			pinch = map_range_tuples(leap_bounds['pinch'], servo_bounds['pinch'], 1 - hand.pinch_strength) # fix to use tuples later
			wrist = map_range_tuples(leap_bounds['wrist'], servo_bounds['wrist'], hand.direction.pitch * Leap.RAD_TO_DEG)
			# 1 - pinchStrength because servo is inverted
			send = [255]
			send.append(int(pinch))
			send.append(int(wrist))

			# cool visual for pinch strength:
			# for i in range(0, 90 - int(pinch - 90)):
				# sys.stdout.write('-')
			# print ''
			print wrist
			# clear buffers!
			arduino_ser.flushInput()
			arduino_ser.flushOutput()
			# print arduino_ser.inWaiting()
			arduino_ser.write(bytearray(send))
			time.sleep(0.04)

def map_range(min_orig, max_orig, min_new, max_new, value):
	range_orig = max_orig - min_orig
	range_new = max_new - min_new
	ratio = range_new / range_orig
	return (value - min_orig) * ratio + min_new # new value 

def map_range_tuples(bounds_orig, bounds_new, value):
	min_orig, max_orig = bounds_orig
	min_new, max_new = bounds_new
	return map_range(min_orig, max_orig, min_new, max_new, value)

def main():
	port = 'COM3'
	baud = 9600

	global arduino_ser
	arduino_ser = serial.Serial(port, baud)
	# arduino_ser.write(bytearray([
	# 	255, # arduino waits for 0xff as start of msg 
	# ]))

	listener = Listener()
	controller = Leap.Controller()

	# Have the listener receive events from the controller
	controller.add_listener(listener)

	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the listener when done
		controller.remove_listener(listener)

if __name__ == "__main__":
	main()
