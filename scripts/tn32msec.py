import serial, sys

s = serial.Serial(sys.argv[1], baudrate=38400, timeout=0.01)

RESET = 0x62
GET_SW = 0x30
GET_HW = 0x32

def send(dev, op, data=b"\0", seq=0x00):
    packet = bytearray([0xe0, len(data) + 4, dev, seq, op])
    packet += data
    packet += bytearray([sum(packet[1:]) % 256])

    s.write(packet)

def recv():
    data = s.read(4096)
    assert data[0] == 0xe0
    return data[7:-1]

send(0, RESET); recv()
send(0, GET_SW)
print("1P Software version:", recv().decode("latin-1"))
send(0, GET_HW)
print("1P Hardware version:", recv().decode("latin-1"))

'''
send(1, RESET); recv()
send(1, GET_SW)
print("2P Software version:", recv().decode("latin-1"))
send(1, GET_HW)
print("2P Hardware version:", recv().decode("latin-1"))
'''