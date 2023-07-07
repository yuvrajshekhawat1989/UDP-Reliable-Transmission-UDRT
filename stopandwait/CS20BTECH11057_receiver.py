import socket

recieverIP = "10.0.0.2"
recieverPort   = 20002
bufferSize  = 1024 #Message Buffer Size

f = open("receiver.jpg","wb")
expected_seq_num = 0

# Create a UDP socket
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind socket to localIP and localPort
socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully....." )
eof = 1
while True:

    #wait to recieve message from the server
    packetAddressPair = socket_udp.recvfrom(bufferSize)

    packet = packetAddressPair[0]
    senderAddress = packetAddressPair[1]
    #Checking whether whole file has been received or not
    if(packet[-1:] == eof.to_bytes(1,'big')):
        break
    #Now since the packet is received, we need to send its ACK
    seq_num = int.from_bytes(packet[0:2],'big')
    print(seq_num)
    if(expected_seq_num==seq_num):
        f.write(packet[2:-1])
        print("Packet received, sending ACK for packet: ",seq_num)
        socket_udp.sendto(expected_seq_num.to_bytes(2,'big'), senderAddress)
        expected_seq_num+=1
    else:
        print("Packet is not expected, sending ACK for last received packet")
        last_recv_seq_num = expected_seq_num-1
        socket_udp.sendto(last_recv_seq_num.to_bytes(2,'big'), senderAddress)


    # # Sending a reply to client
    # message = str.encode("This is a reply message from the server")
    # socket_udp.sendto(message, senderAddress)
