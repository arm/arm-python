import sys, time, math

sys.path.insert(0, "../lib")
import serial, Leap

servo_bounds = {
	'pinch': (90, 180),
	'wrist': (0,180),
	'twist': (10,180),
	'elbow': (5, 180),
	'shoulder_right': (0, 174),
	'shoulder_left': (180, 6)
}

leap_bounds = {
	'pinch': (0, 1),
	'wrist': (-90,90),
	'elbow': (0, -180),
	# 'shoulder': (0, 180),
}

l1 = 140 # length of upper arm
l2 = 128.86 # length of forearm

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
			# 1 - pinchStrength because sersvo is inverted
			# shoulder = #blah 0-180
			x = hand.palm_position.x
			y = hand.palm_position.y
			z = hand.palm_position.z

			# set bounds of interaction
			if y < 150:
				y = 150
			if y > 500:
				y = 500
			if x > 200:
				x = 200
			if x < -200:
				x = -200
			if z > 200:
				z = 200
			if z < -200:
				z = -200

			z = 200 - z
			rotation =  math.atan(z / x) * (180 / math.pi)
		


			# print x, z, y
			shoulder = (z / 400) * 174;
			# print z, shoulder
			# print shoulder
			if x < 0:
				rotation = 180 + rotation
			rotation = 180 - rotation
			# print rotation
			
			x = x/2
			y = y/2
			z = z/2
			dist = math.sqrt(x**2 + z**2) # x, z distance from origin point
			theta_2 = math.atan2(-math.sqrt(1 - ((dist**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2))**2 ), ((dist**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)) )
			
			k1 = l1 + l2 * math.cos(theta_2)
			k2 = l2 * math.sin(theta_2)

			theta_1 = math.atan2(y, dist) - math.atan2(k2, k1) # in radians

			# print theta_1 * (180 / math.pi), theta_2 * (180 / math.pi)

			elbow = map_range_tuples(leap_bounds['elbow'], servo_bounds['elbow'], theta_2 * (180 / math.pi))
			print theta_2 * (180 / math.pi), elbow


			send = [255]
			send.append(int(pinch))
			send.append(int(wrist))
			send.append(int(rotation))
			send.append(int(elbow))
			send.append(int(174 - shoulder))
			send.append(int(shoulder))


			# cool visual for pinch strength:
			# for i in range(0, 90 - int(pinch - 90)):
				# sys.stdout.write('-')
			# print ''
			# print wrist

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
