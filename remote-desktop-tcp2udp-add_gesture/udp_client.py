from socket import *

HOST = '0.0.0.0'
PORT = 8888
BUFSIZ = 1024
ADDRESS = (HOST, PORT)

udpClientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    data = input('>')
    if not data:
        break

    # 发送数据
    udpClientSocket.sendto(data.encode('utf-8'), ADDRESS)
    # 接收数据
    data, ADDR = udpClientSocket.recvfrom(BUFSIZ)
    if not data:
        break
    print("服务器端响应：", data.decode('utf-8'))

udpClientSocket.close()
