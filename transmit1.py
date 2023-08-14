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
    '.': '.-.-.-', ',': '--..--'
}

# Connect to the Arduino board
board = Arduino('COM26')  # Update this with the correct serial port

# Define the pin number for the LED
led_pin = 8

# Set up the pin as OUTPUT
board.digital[led_pin].mode = pyfirmata.OUTPUT

def send_morse_code(message):
    for char in message:
        if char == ' ':
            time.sleep(3)  # Gap between words
        else:
            morse_code = morse_code_dict.get(char.upper())
            if morse_code:
                for symbol in morse_code:
                    if symbol == '.':
                        board.digital[led_pin].write(1)  # LED on for a dot
                        time.sleep(0.3)
                        board.digital[led_pin].write(0)
                        time.sleep(0.3)
                    elif symbol == '-':
                        board.digital[led_pin].write(1)  # LED on for a dash
                        time.sleep(0.9)
                        board.digital[led_pin].write(0)
                        time.sleep(0.3)
            time.sleep(0.6)  # Gap between letters

try:
    while True:
        user_input = input("Enter a message: ")
        send_morse_code(user_input)
except KeyboardInterrupt:
    # Turn off the LED and close the connection when the program is terminated
    board.digital[led_pin].write(0)
    board.exit()
