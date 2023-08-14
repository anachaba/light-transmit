from pyfirmata import Arduino, util
import time

# Morse code dictionary
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    # ... (rest of the Morse code dictionary)
}

# Connect to the Arduino board
board = Arduino('COM26')  # Update this with the correct serial port

# Define the photoresistor pin
photoresistor_pin = 0  # Analog pin 0

board.analog[photoresistor_pin].enable_reporting()

def read_light_intensity():
    return board.analog[photoresistor_pin].read()

def decode_morse_code(morse_code):
    decoded_message = ""
    current_symbol = ""
    
    for signal in morse_code:
        if signal == '.' or signal == '-':
            current_symbol += signal
        elif signal == ' ':
            char = None
            for key, value in morse_code_dict.items():
                if value == current_symbol:
                    char = key
                    break
            decoded_message += char if char else ' '
            current_symbol = ""
    return decoded_message

def main():
    morse_code_signal = []

    try:
        while True:
            light_intensity = read_light_intensity()
            
            if light_intensity is not None:
                if light_intensity < 0.1:  # Adjust threshold as needed
                    morse_code_signal.append('.')
                else:
                    morse_code_signal.append('-')

                time.sleep(0.05)  # Adjust as needed

    except KeyboardInterrupt:
        decoded_text = decode_morse_code(morse_code_signal)
        print("Decoded message:", decoded_text)

if __name__ == "__main__":
    main()
