import pyperclip
import keyboard
import pyautogui
import pytesseract
from PIL import ImageGrab

# Path to the Tesseract executable (update this based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_and_extract_text():
    # Capture screenshot
    screenshot = ImageGrab.grabclipboard()

    if screenshot is not None:

        # Save screenshot to a file
        screenshot.save("screenshot.png")

        # Use OCR to extract text from the screenshot
        extracted_text = pytesseract.image_to_string(screenshot)

        # Copy extracted text to clipboard
        pyperclip.copy(extracted_text)
        print("Text extracted and copied to clipboard.")
    else:
        print("No image found in the clipboard.")

# Define the shortcut key combination
shortcut = "ctrl+print_screen"

print("Press Ctrl + Alt + C to capture image from clipboard and extract text.")

while True:
    if keyboard.is_pressed(shortcut):
        capture_and_extract_text()
        # Release keys to avoid continuous triggering
        # for key in trigger_keys:
        #     pyautogui.keyUp(key)

