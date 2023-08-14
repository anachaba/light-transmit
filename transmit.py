from pyfirmata import Arduino
import time

# Morse code dictionary (same as before)
morse_code_dict = {
    # ... (same as before) refer from both-ways.py
}

# Connect to the Arduino board
board = Arduino('COM26')  # Update this with the correct serial port

# Define the LED pin
led_pin = 8

board.digital[led_pin].mode = pyfirmata.OUTPUT

def encode_morse_code(message):
    morse_code_signal = []
    for char in message:
        morse_code = morse_code_dict.get(char)
        if morse_code:
            morse_code_signal.extend(morse_code)
            morse_code_signal.append(' ')  # Gap between characters
    return morse_code_signal

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

            time.sleep(0.3)  # Gap between signals

    except KeyboardInterrupt:
        board.digital[led_pin].write(0)
        board.exit()

if __name__ == "__main__":
    main()
