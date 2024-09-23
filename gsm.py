
'''from time import sleep
import serial

def setup_modem():
    # Update the port to COM6
    ser = serial.Serial()
    ser.port = 'COM6'
    ser.baudrate = 115200
    ser.timeout = 1
    ser.open()
    ser.write(b'AT+CMGF=1\r\n')  # Set to text mode
    ser.write(b'AT+CPMS="ME","SM","ME"\r\n')  # Set preferred message storage area
    return ser

def sendsms(ser, number, text):
    ser.write(b'AT+CMGF=1\r\n')  # Ensure text mode
    sleep(2)
    ser.write(f'AT+CMGS="{number}"\r\n'.encode())  # Set recipient
    sleep(2)
    ser.write(text.encode())  # Write message text
    sleep(2)
    ser.write(b'\x1A')  # End message with Ctrl+Z (hex 0x1A)
    print(f"Text: {text} \nhas been sent to: {number}")

def read_all_sms(ser):
    ser.write(b'AT+CMGF=1\r\n')  # Ensure text mode
    sleep(2)
    ser.write(b'AT+CMGL="ALL"\r\n')  # List all messages
    sleep(5)
    responses = ser.readlines()
    messages = []
    for response in responses:
        if response.startswith(b'+CMGL:'):
            idx = responses.index(response)
            if idx + 1 < len(responses):
                messages.append(responses[idx + 1].decode().strip())
    return messages

def delete_all_sms(ser):
    ser.write(b'AT+CMGF=0\r\n')  # Set to PDU mode
    sleep(2)
    ser.write(b'AT+CMGD=0,4\r\n')  # Delete all messages
    sleep(2)
    ser.write(b'AT+CMGF=1\r\n')  # Set back to text mode

def main():
    ser = setup_modem()
    sendsms(ser, '+917001358094', 'Hello, this is a test message!')
    messages = read_all_sms(ser)
    for message in messages:
        print(f"Message: {message}")
    delete_all_sms(ser)
    ser.close()

if __name__ == "__main__":
    main()'''
from time import sleep
import serial

def setup_modem():
    try:
        ser = serial.Serial()
        ser.port = 'COM8'
        ser.baudrate = 115200
        ser.timeout = 1
        ser.open()
        ser.write(b'AT+CMGF=1\r\n')  # Set to text mode
        sleep(2)
        ser.write(b'AT+CPMS="ME","SM","ME"\r\n')  # Set preferred message storage area
        sleep(2)
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

def sendsms(ser, number, text):
    try:
        ser.write(b'AT+CMGF=1\r\n')  # Ensure text mode
        sleep(2)
        ser.write(f'AT+CMGS="{number}"\r\n'.encode())  # Set recipient
        sleep(2)
        ser.write(text.encode())  # Write message text
        sleep(2)
        ser.write(b'\x1A')  # End message with Ctrl+Z (hex 0x1A)
        sleep(5)  # Allow time for the message to be sent
        print(f"Text: {text} \nhas been sent to: {number}")
    except Exception as e:
        print(f"Failed to send SMS. Error: {e}")

def read_all_sms(ser):
    try:
        ser.write(b'AT+CMGF=1\r\n')  # Ensure text mode
        sleep(2)
        ser.write(b'AT+CMGL="ALL"\r\n')  # List all messages
        sleep(5)
        responses = []
        while True:
            line = ser.readline().decode().strip()
            if not line:
                break
            responses.append(line)
        
        messages = []
        i = 0
        while i < len(responses):
            if responses[i].startswith('+CMGL:'):
                i += 1
                if i < len(responses):
                    messages.append(responses[i])
            i += 1
        
        return messages
    except Exception as e:
        print(f"Failed to read SMS. Error: {e}")
        return []

def delete_all_sms(ser):
    try:
        ser.write(b'AT+CMGF=0\r\n')  # Set to PDU mode
        sleep(2)
        ser.write(b'AT+CMGD=0,4\r\n')  # Delete all messages
        sleep(2)
        ser.write(b'AT+CMGF=1\r\n')  # Set back to text mode
        sleep(2)
    except Exception as e:
        print(f"Failed to delete SMS. Error: {e}")

def main():
    ser = setup_modem()
    if ser:
        sendsms(ser, '7668151892', 'Hello, this is a test message!')
        messages = read_all_sms(ser)
        for message in messages:
            print(f"Message: {message}")
        delete_all_sms(ser)
        ser.close()

if __name__ == "__main__":
    main()
