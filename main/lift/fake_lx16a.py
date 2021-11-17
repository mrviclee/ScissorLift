class ServoError(Exception):
	pass

class LX16A:
	controller = None
	servos = set()
	
	########### Initialization Functions ###########
	# Must be called before use!
	@staticmethod
	def initialize(port):
		pass
	
	def __init__(self, ID):
		pass
	
	################ Write Commands ################
	
	# Immediately after this command is sent,
	# rotate to the specified angle at uniform
	# speed, in the specified time
	
	# Possible angle values (in degrees): [0, 240], int
	# Possible time values (in milliseconds): [0, 30000], int
	
	def moveTimeWrite(self, angle, time=0):
		pass
	
	# This command is similar to servo.moveTimeWrite,
	# except that the servo will not begin rotation
	# until it receives the servo.moveStart command
	
	# Possible angle values (in degrees): [0, 240], int
	# Possible time values (in milliseconds): [0, 30000], int
	
	def moveTimeWaitWrite(self, angle, time=0):
		pass
	
	# To be used in conjunction with servo.moveTimeWaitWrite
	# Read the documentation for that command
	
	def moveStart(self):
		pass
	
	# Immediately halts all rotation,
	# regardless of the current state
	
	def moveStop(self):
		pass
	
	# Changes the servo's ID to the
	# parameter passed to this function
		
	# !!! BE CAREFUL WITH THIS COMMAND !!!
	# IT PERMANANTLY CHANGES THE ID OF THE SERVO
	# EVEN AFTER THE PROGRAM TERMINATES
	# AND AFTER THE SERVO POWERS DOWN
	# !!! YOU HAVE BEEN WARNED !!!
	
	# The ID of all servos is 1 by default
	# Possible ID values: [0, 253], int
	
	def IDWrite(self, ID):
		pass
	
	# Adds a constant offset to the angle of rotation
	
	# For example, if the offset is -125 (-30 degrees),
	# and the servo is commanded to rotate to position
	# 500 (120 degrees), it will rotate to position 375
	# (90 degrees)
	
	# The offset resets back to 0 when the servo powers off
	# However, it can be permanently set using servo.angleOffsetWrite
	
	# The offset is 0 by default
	# Possible angle values (in degrees): [-30, 30], int
	
	def angleOffsetAdjust(self, offset):
		pass
	
	# Permanently applies the offset angle set by
	# servo.AngleOffsetAdjust. After the servo powers
	# down, the offset will default to the set angle
	
	def angleOffsetWrite(self):
		pass

	# Permanently sets a restriction on the rotation
	# angle. If the current angle is outside of the bounds,
	# nothing will change. But once the angle enters the legal range,
	# it will not be allowed to exceed the limits until they are extended
	
	# After restrictions are applied, the angles will not scale
	# For example, if the bounds are set to [120, 240], the angle 0
	# does not mean a rotation of halfway
	
	# The lower bound must always be less than the upper bound
	# The default angle limits are 0 and 240
	# Possible lower values (in degrees): [0, 240], int
	# Possible upper values (in degrees): [0, 240], int
	
	def angleLimitWrite(self, lower, upper):
		pass
	
	# Sets the lower and upper bounds on the input voltage
	
	# If the input voltage exceeds these bounds, the LED
	# on the servo will flash and the servo will not rotate
	
	# Possible lower values (in millivolts): [4500, 12000], int
	# Possible higher values (in millivolts): [4500, 12000], int
	
	def vInLimitWrite(self, lower, upper):
		pass

	# Sets the maximum internal temperature
	
	# If the servo temperature exceeds the limit, the LED
	# on the servo will flash and the servo will not rotate
	
	# Default maximum temperature is 85 degrees
	# Possible temperature values (in degrees celcius): [50, 100], int
	
	def tempMaxLimitWrite(self, temp):
		pass
	
	# The LX-16A has two modes:
	# Servo mode (with precise angle control)
	# Motor mode (with continuous rotation)
	
	# This command sets the servo to servo mode
	
	def servoMode(self):
		pass
	
	# This command sets the servo to motor mode
	
	# The speed parameter controls how fast
	# the servo spins
	
	# -1000 is full speed backwards, and
	# 1000 is full speed forwards
	# Possible speed values: [-1000, 1000], int
	
	def motorMode(self, speed):
		pass
	
	# Controls the power state of the servo
	
	# In the power down state, the servo consumes
	# less power, but will also not respond to commands
	# It will respond once powered on
	
	# Possible power values:
	# 0 for power down, 1 for power on
	
