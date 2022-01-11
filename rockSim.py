import serial, requests, json, time, random

ser = serial.Serial('COM2')

ser.flushInput()

bytes = ""
decoderTag = "6e35c4d4-9e1e-4e84-bcae-fe762cc1e0c3"
packet = ""
api = "https://whiskershub.aphcarios.com/api/whiskers/Device/test/"
postBuffer = ""
packet = ""

print("Serial Port Initialized.")

print("Listening to Gateway...")

def decode():
    global bytes, postBuffer
    ser_decode = ser_byte.decode("utf-8")
    try:
        if ser_decode == "\r" or ser_decode == "\n":
            if bytes != "":
                print("\nReceived: ", end=bytes)
            
            if bytes == "":
                return
            
            elif bytes == "AT":
                time.sleep(random.randint(0, 100)/1000)
                print("\nResponse: OK")
                ser.write("OK\r".encode())
            
            elif bytes[0:5] == "AT&K0":
                time.sleep(random.randint(0, 100)/1000)
                print("\nResponse: OK")
                ser.write("OK\r".encode())
            
            elif bytes[0:9] == "AT+SBDWT=":
                time.sleep(random.randint(0, 100)/1000)
                postBuffer = bytes[9:]
                print("\nPOST Buffer: ", end=postBuffer)
                ser.write("OK\r".encode())
            
            elif bytes[0:8] == "AT+SBDIX":
                if netCheck():
                    time.sleep(random.randint(0, 5000)/1000)
                    print("\nResponse: +SBDIX: 0, 0, 0, 0, 0, 0")
                    ser.write("+SBDIX: 0, 0, 0, 0, 0, 0\r".encode())
                    packet = '[{"data":"' + postBuffer + '"}]'
                    post(api+decoderTag, json.loads(packet))
                else:
                    print("\nResponse: +SBDIX: 32, 0, 0, 0, 0, 0")
                    ser.write("+SBDIX: 32, 0, 0, 0, 0, 0\r".encode())
            
            else:
                print("\nUnknown AT Command.")
            
            bytes = ""
        else:
            if ser_decode != "\r" and ser_decode != "\n":
                bytes = bytes + ser_decode
    except:
        bytes = ""

def post(url, json):
    x = requests.post(url+decoderTag, json=json)
    print("\nPOST Response: ", end=str(x))
    print("\nPOST Response Body:")
    print(x.text)

def netCheck():
    try:
        request = requests.get("https://www.google.com", timeout=2)
        return True
    except:
        return False

while True:
    ser_byte = ser.read()
    decode()