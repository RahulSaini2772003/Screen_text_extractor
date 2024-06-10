import keyboard
import pyautogui
import pytesseract
import pyperclip
from PIL import Image
import tkinter as tk

# Define the shortcut key combination
shortcut = "ctrl+alt+s"

# Global variables to store mouse coordinates
start_x, start_y = 0, 0
end_x, end_y = 0, 0
overlay = None
root = None  # Define root globally


def capture_screen(region):
    screenshot = pyautogui.screenshot(region=region)
    return screenshot


def extract_text_from_image(image):
    # Resize the image to improve quality
    image = image.resize((image.width * 2, image.height * 2), Image.ANTIALIAS)

    # Convert image to grayscale
    image = image.convert("L")

    # Apply thresholding to enhance contrast
    threshold_value = 100
    image = image.point(lambda p: p > threshold_value and 255)

    # Use Tesseract to perform OCR with enhanced image
    text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
    return text


def draw_rectangle(event):
    global overlay, start_x, start_y, end_x, end_y
    overlay.delete("rect")  # Remove previously drawn rectangles

    # Calculate the offset between the starting point of mouse drag and current mouse position
    offset_x = event.x - start_x
    offset_y = event.y - start_y

    # Draw the rectangle on the overlay window starting from the point where the mouse is pressed
    overlay.create_rectangle(start_x, start_y, event.x,
                             event.y, outline="white", tags="rect", fill="")


def on_mouse_down(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y


def on_mouse_up(event):
    global end_x, end_y, overlay, root
    end_x, end_y = event.x, event.y
    overlay.destroy()  # Close the overlay window
    root.destroy()  # Close the main Tkinter window

    # Capture the selected region
    screenshot = capture_screen(
        (start_x, start_y, end_x - start_x, end_y - start_y))

    # Extract text from the captured region
    extracted_text = extract_text_from_image(screenshot)

    # Print and copy the extracted text to the clipboard
    print("Extracted text:")
    print(extracted_text)
    pyperclip.copy(extracted_text)


def capture_selected_region():
    global overlay, root
    root = tk.Tk()
    root.attributes('-alpha', 0.3)
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)

    # Create the overlay window
    overlay = tk.Canvas(root, bg="black", highlightthickness=0)
    overlay.pack(fill=tk.BOTH, expand=True)

    # Bind mouse events
    overlay.bind("<ButtonPress-1>", on_mouse_down)
    overlay.bind("<ButtonRelease-1>", on_mouse_up)
    overlay.bind("<B1-Motion>", draw_rectangle)

    root.mainloop()


def main():
    print("Press shortcut key to capture screen...")

    while True:
        if keyboard.is_pressed(shortcut):
            print("Shortcut key pressed! Capturing screen...")
            capture_selected_region()


if __name__ == "__main__":
    main()
