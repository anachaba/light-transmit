from pyfirmata import Arduino, util
import time
import pyfirmata

# Morse code dictionary
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    '.': '.-.-.-', ',': '--..--',' ':'.......'
}

# Connect to the Arduino board
board = Arduino('COM26')  # Update this with the correct serial port

# Define the LED pin and photoresistor pin
led_pin = 8
photoresistor_pin = 0  # Analog pin 0

board.digital[led_pin].mode = pyfirmata.OUTPUT
analog_input = board.get_pin('a:0:i')
it = util.Iterator(board)
it.start()

def read_light_intensity():
    return analog_input.read()

def encode_morse_code(message):
    morse_code_signal = []
    for char in message:
        morse_code = morse_code_dict.get(char)
        if morse_code:
            morse_code_signal.extend(morse_code)
            morse_code_signal.append(' ')  # Gap between characters
    return morse_code_signal

def decode_morse_code(morse_code_signal):
    decoded_message = ""
    current_symbol = ""
    
    for signal in morse_code_signal:
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
    user_input = input("Enter a message: ").upper()
    morse_code_signal = encode_morse_code(user_input)

    try:
        for signal in morse_code_signal:
            if signal == '.':
                board.digital[led_pin].write(1)
                time.sleep(0.3)
                board.digital[led_pin].write(0)
            elif signal == '-':
                board.digital[led_pin].write(1)
                time.sleep(0.9)
                board.digital[led_pin].write(0)
            elif signal == ' ':
                time.sleep(0.6)  # Gap between characters

            light_intensity = read_light_intensity()
            if light_intensity is not None:
                print("light intensity ==>", light_intensity)

            time.sleep(0.3)  # Gap between signals

        decoded_text = decode_morse_code(morse_code_signal)
        print("Decoded message:", decoded_text)

    except KeyboardInterrupt:
        board.digital[led_pin].write(0)
        board.exit()

if __name__ == "__main__":
    main()
