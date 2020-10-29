import MFRC522
import signal
import socket

continue_reading = True
MIFAREReader = MFRC522.MFRC522()

cardA = [6,100,18,73,57]
cardB = [54,6,9,73,112]

def end_read(signal, frame):
  global continue_reading
  continue_reading = False
  print "Ctrl+C captured, ending read."
  MIFAREReader.GPIO_CLEEN()

signal.signal(signal.SIGINT, end_read)

while continue_reading:
  (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
  if status == MIFAREReader.MI_OK:
    print "Card detected"
  (status,backData) = MIFAREReader.MFRC522_Anticoll()
  if status == MIFAREReader.MI_OK:
    print "Card read UID: "+str(backData[0])+","+str(backData[1])+","+str(backData[2])+","+str(backData[3])+","+str(backData[4])
    if  backData == cardA:
      print "is CARD A"
      UDP_IP = "192.168.0.111"
      UDP_PORT = 80
      MESSAGE = "Hello, I am following you"

      print "UDP target IP: ", UDP_IP
      print "UDP target port: ", UDP_PORT
      print "Message: ", MESSAGE

      sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

      sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
      test = True

      while test:
        data, addr = sock.recvfrom(80)
	print "  "
	print "Receive Message: ", data
	print "Receive From   : ", addr
	test = False
    elif backData == cardB:
      print "is CARD B"
      UDP_IP = "192.168.0.106"
      UDP_PORT = 80
      MESSAGE = "Hello, I am right behind you"

      print "UDP target IP: ", UDP_IP
      print "UDP target port: ", UDP_PORT
      print "Message: ", MESSAGE

      sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

      sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
      test = True

      while test:
        data, addr = sock.recvfrom(80)
	print "  "
	print "Receive Message: ", data
	print "Receive From   : ", addr
	test = False
