import socket
import signal
import time
import os

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size
file = open("testFile.jpg","rb")

# Make list of all packets to be sent
packet_data = file.read(bufferSize-3)
seq_num = 0
base = 0
N=8
next_seq_num = 0
eof = 0
timeout = 0.01
packets = []

start = time.time()
while packet_data:
    # We need to add sequence number of 2 bytes and a character for EOF in packet
    # Buffer size will be original bufferSize-3 therefore
    packet = seq_num.to_bytes(2,'big')+packet_data+eof.to_bytes(1,'big')
    packets.insert(seq_num,packet)
    packet_data = file.read(bufferSize-3)
    seq_num+=1

total_packets = seq_num
# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def raise_exception(signum,frame):
    raise Exception("Timeout happened")

print(total_packets)
signal.signal(signal.SIGALRM, raise_exception)
start_time = time.time()

while True:
    try:
        if (next_seq_num<base+N and next_seq_num<total_packets):
            socket_udp.sendto(packets[next_seq_num], recieverAddressPort)
            if (base == next_seq_num):
                signal.setitimer(signal.ITIMER_REAL, timeout)
            if(next_seq_num<total_packets):
                next_seq_num+=1
        else:
            MessageAdressPair = socket_udp.recvfrom(bufferSize)
            ACK = int.from_bytes(MessageAdressPair[0][0:2],byteorder='big')
            if(ACK==base):
                if(base==next_seq_num):
                    signal.alarm(0)
                else:
                    signal.setitimer(signal.ITIMER_REAL, timeout)
                print("Packet number ",base,"is ACKed")
                base+=1
        if(base==total_packets):
            break
    except Exception as e:
        print(e)
        try:
            signal.setitimer(signal.ITIMER_REAL, timeout)
            i = base
            while (i<next_seq_num):
                socket_udp.sendto(packets[i],recieverAddressPort)
                i+=1
        except Exception as e1:
            print("Timeout time too low, Can't even send the window")
            exit()

#1 in bytes marks end of file
eof=1
socket_udp.sendto(eof.to_bytes(1, byteorder='big') , recieverAddressPort)
end = time.time()
time_taken = end-start
file_Size =  os.path.getsize("testFile.jpg")/1024
throughput = file_Size/time_taken
print("Throughput is ",throughput)
socket_udp.close()
file.close()
