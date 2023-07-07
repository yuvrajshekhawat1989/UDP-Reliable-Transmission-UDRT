import socket
import signal
import os
import time

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size
file = open("testFile.jpg","rb")

# We need to add sequence number of 2 bytes and a character for EOF in packet
# Buffer size will be original bufferSize-3 therefore
packet_data = file.read(bufferSize-3)
seq_num = 0
eof = 0
timeout=0.01
retransimissions=0

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def raise_exception(signum,frame):
    raise Exception("Timeout happened")

signal.signal(signal.SIGALRM,raise_exception)

start = time.time()
while packet_data:
    try:
        packet = seq_num.to_bytes(2,'big')+packet_data+eof.to_bytes(1,'big')
        socket_udp.sendto(packet,recieverAddressPort)
        signal.setitimer(signal.ITIMER_REAL,timeout)
        packetAddressPair = socket_udp.recvfrom(bufferSize)
        ACK = packetAddressPair[0]
        while True:
            if(ACK==seq_num.to_bytes(2,'big')):
                signal.alarm(0)
                packet_data  = file.read(bufferSize-3)
                print("Packet ",seq_num," is succesfully sent and ACKed")
                seq_num+=1
                break
    except Exception as a:
        retransimissions+=1
        print(a)
        continue

# while packet_data:
#
# 	try:
#         socket_udp.sendto(  seq_num.to_bytes(2, byteorder='big') + packet_data+ eof.to_bytes(1, byteorder='big') , recieverAddressPort)
#         signal.setitimer(signal.ITIMER_REAL, timeout)
#         packetAddressPair = socket_udp.recvfrom(bufferSize)
#         ack = packetAddressPair[0]
#         while True:
#             if(ack == seq_num.to_bytes(2,'big')):
#                 signal.alarm(0)
#                 packet_data = file.read(bufferSize-3)
#                 print("Packet ", seq_num , " is succesfully sent and acknowledged")
#                 seq_num += 1
#                 break
#
#     except Exception as e:
#         retransimissions+=1
#         print(e)
#         continue

#1 in bytes marks end of file
eof=1
socket_udp.sendto(eof.to_bytes(1, byteorder='big') , recieverAddressPort)
end = time.time()
time_taken = end-start
file_Size =  os.path.getsize("testFile.jpg")/1024
throughput = file_Size/time_taken
print("Throughput is ",throughput," and number of retransimissions are ",retransimissions)
socket_udp.close()
file.close()
