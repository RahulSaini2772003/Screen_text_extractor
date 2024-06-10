import keyboard
import pyautogui
import pytesseract
import pyperclip
from PIL import Image
import tkinter as tk
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import os

# Define the shortcut key combination
shortcut = "ctrl+print_screen"

# Global variables to store mouse coordinates
start_x, start_y = 0, 0
end_x, end_y = 0, 0
overlay = None
root = None  # Define root globally
enabled = True

# Function to capture screen


def capture_screen(region):
    screenshot = pyautogui.screenshot(region=region)
    return screenshot

# Function to extract text from image


def extract_text_from_image(image):
    # Resize the image to improve quality
    image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)

    # Convert image to grayscale
    image = image.convert("L")

    # Apply thresholding to enhance contrast
    threshold_value = 100
    image = image.point(lambda p: p > threshold_value and 255)

    # Use Tesseract to perform OCR with enhanced image
    text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
    return text

# Function to handle mouse down event


def on_mouse_down(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

# Function to handle mouse up event
def draw_rectangle(event):
    global overlay, start_x, start_y, end_x, end_y
    overlay.delete("rect")  # Remove previously drawn rectangles

    # Calculate the offset between the starting point of mouse drag and current mouse position
    offset_x = event.x - start_x
    offset_y = event.y - start_y

    # Draw the rectangle on the overlay window starting from the point where the mouse is pressed
    overlay.create_rectangle(start_x, start_y, event.x,
                             event.y, outline="white", tags="rect", fill="white")


def on_mouse_up(event):
    global end_x, end_y, overlay, root
    end_x, end_y = event.x, event.y

    width = end_x - start_x
    height = end_y - start_y

    # Check if either width or height is smaller than a threshold
    min_width = 20  # Define a minimum width threshold
    min_height = 20  # Define a minimum height threshold
    if width < min_width or height < min_height:
        overlay.destroy()  # Close the overlay window
        root.destroy()  # Close the main Tkinter window
        return

    overlay.destroy()  # Close the overlay window
    root.destroy()

    # Capture the selected region
    screenshot = capture_screen(
        (start_x, start_y, end_x - start_x, end_y - start_y))

    # Extract text from the captured region
    extracted_text = extract_text_from_image(screenshot)
    print(extracted_text)

    # Print and copy the extracted text to the clipboard
    pyperclip.copy(extracted_text)

# Function to capture selected region


def capture_selected_region():
    global overlay, root

    def check_escape_key():
        if keyboard.is_pressed("esc"):
            root.destroy()  # Close the overlay window
            return
        root.after(100, check_escape_key)  # Check every 100ms

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

    # Check for the Escape key press
    check_escape_key()

    root.mainloop()  # Start Tkinter event loop


# Function to exit the application from the system tray
def exit_application(icon=None, item=None):
    global root
    try:
        if root:
            root.quit()  # Exit the Tkinter event loop
            root.destroy()  # Close the Tkinter window
        print("Application closed.")
        os._exit(0)  # Forcefully exit the program with exit code 0
    except SystemExit:
        pass


# Function to enable/disable capture functionality
icon = None
enabled = True

# Function to enable/disable capture functionality
def toggle_capture(icon=None, item=None):
    global enabled
    enabled = not enabled
    print("Capture functionality", "Enabled" if enabled else "Disabled")
    if icon:  # Check if the icon is provided
        # Update the icon menu with the new state
        update_icon_menu()

# Function to update the icon menu based on the current state
def update_icon_menu():
    global icon, enabled
    if icon:
        # Replace the menu with the updated one
        icon.menu = [item('Enable' if enabled else 'Disable', toggle_capture),
                     item('Close', exit_application)]

# Function to create the system tray icon
def create_system_tray_icon():
    global icon, enabled
    # Replace "path/to/icon.png" with the path to your icon image
    image = Image.open("icon/pxe.ico")
    # Create the icon if it doesn't exist
    if not icon:
        icon = pystray.Icon("name", image, "Snip_Text", [])
    # Update the icon menu
    update_icon_menu()
    # Run the icon
    icon.run()


def main():
    while True:
        if enabled and keyboard.is_pressed(shortcut):
            capture_selected_region()


if __name__ == "__main__":
    # Run the system tray icon in a separate thread
    threading.Thread(target=create_system_tray_icon).start()

    # Start the main functionality of the application
    main()
