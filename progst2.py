import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def encode_message():
    # Get the message to encode
    message = message_entry.get()

    if not message:
        messagebox.showwarning("Input Error", "Please enter a message to encode.")
        return

    # Ask user to select an image file
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])

    if not image_path:
        return

    # Load the image
    try:
        image = Image.open(image_path)
        image = image.convert("RGB")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open image: {e}")
        return

    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '00000000'

    # Encode the message into the image
    pixels = list(image.getdata())
    new_pixels = []
    message_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if message_index < len(binary_message):
            r = (r & ~1) | int(binary_message[message_index])
            message_index += 1
        if message_index < len(binary_message):
            g = (g & ~1) | int(binary_message[message_index])
            message_index += 1
        if message_index < len(binary_message):
            b = (b & ~1) | int(binary_message[message_index])
            message_index += 1
        new_pixels.append((r, g, b))

    # Save the new image
    encoded_image = Image.new(image.mode, image.size)
    encoded_image.putdata(new_pixels)
    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])

    if output_path:
        encoded_image.save(output_path)
        messagebox.showinfo("Success", "Message encoded successfully!")

def decode_message():
    # Ask user to select an image file
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])

    if not image_path:
        return

    # Load the image
    try:
        image = Image.open(image_path)
        image = image.convert("RGB")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open image: {e}")
        return

    # Decode the message from the image
    binary_message = ""
    for pixel in image.getdata():
        r, g, b = pixel
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)

    # Convert binary message to text
    decoded_message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == "00000000":
            break
        decoded_message += chr(int(byte, 2))

    messagebox.showinfo("Decoded Message", f"Message: {decoded_message}")

# Create the main window
root = tk.Tk()
root.title("Steganography Powerhouse")
root.geometry("450x450")

# Create and place widgets
message_label = tk.Label(root, text="Enter Message to Encode:")
message_label.pack(pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=10)

encode_button = tk.Button(root, text="Encode Message", command=encode_message)
encode_button.pack(pady=10)

decode_button = tk.Button(root, text="Decode Message", command=decode_message)
decode_button.pack(pady=10)

# Run the main loop
root.mainloop()