import qrcode
from PIL import Image, ImageOps
import cv2
from pyzbar.pyzbar import decode
import os

# Function to generate a colorful QR code with an embedded image and padding
def generate_qr(data, profile_image_path, fill_color="green", back_color="white"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction level
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    # Create a colorful QR code
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

    # Open and resize the profile image to embed in the center of the QR code
    profile_img = Image.open(profile_image_path)

    # Reduce the size of the profile image (e.g., 80x80) to avoid covering too much of the QR code
    profile_img = profile_img.resize((80, 80), Image.LANCZOS)

    # Add padding around the profile image (e.g., 10px padding)
    padding_color = "white"  # You can change the padding color if needed
    profile_img_with_padding = ImageOps.expand(profile_img, border=10, fill=padding_color)

    # Calculate the position to paste the profile image in the center of the QR code
    qr_width, qr_height = qr_img.size
    profile_position = (
        (qr_width - profile_img_with_padding.size[0]) // 2,
        (qr_height - profile_img_with_padding.size[1]) // 2
    )

    # Paste the profile image with padding on the QR code
    qr_img.paste(profile_img_with_padding, profile_position)

    # Save the colorful QR code
    qr_img.save('advanced_qr_with_profile.png', dpi=(300, 300))
    print("Colorful QR code with embedded profile image saved as 'advanced_qr_with_profile.png'")

# Function to decode a QR code
def decode_qr(image_path):
    # Open the QR code image and convert it to grayscale
    img = Image.open(image_path).convert('L')

    # Convert the image to OpenCV format for decoding
    img_cv = cv2.imread(image_path)

    # Decode the QR code using pyzbar
    decoded_objects = decode(img_cv)

    if decoded_objects:
        for obj in decoded_objects:
            print("QR Code detected!")
            print("Type:", obj.type)
            print("Data:", obj.data.decode('utf-8'))  # Decode the data and print it
    else:
        print("No QR code detected.")

# Main menu for user input
def main():
    print("Welcome to the Advanced QR Code Generator and Decoder!")
    print("Choose an option:")
    print("1. Encode (Generate a colorful QR code with an embedded profile picture)")
    print("2. Decode (Extract data from an existing QR code)")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        data = input("Enter the data to encode (e.g., a URL): ")
        profile_image_path = input("Enter the path to the profile image: ")
        fill_color = input("Enter the QR foreground color (default: green): ") or "green"
        back_color = input("Enter the QR background color (default: white): ") or "white"

        generate_qr(data, profile_image_path, fill_color, back_color)

    elif choice == "2":
        qr_image_path = input("Enter the path to the QR code image: ")
        decode_qr(qr_image_path)

    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
