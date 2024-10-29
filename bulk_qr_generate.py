import qrcode
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import zipfile

# Create a directory to store the QR codes
output_dir = "qr_codes"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define path for the zip file
zip_file_path = os.path.join(output_dir, "qr_codes.zip")

def generate_qr_codes():
    try:
        # Get the number of QR codes from the user input
        count = int(entry_count.get())
        if count <= 0:
            messagebox.showerror("Invalid Input", "Please enter a positive integer.")
            return
        
        # Clear previous QR codes
        for file in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, file))
        
        # Generate QR codes
        for i in range(1, count + 1):
            qr_data = str(i)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code image
            file_name = f"{output_dir}/{i}.png"
            qr_image.save(file_name)
        
        # Create zip file of all generated QR codes
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for i in range(1, count + 1):
                file_name = f"{output_dir}/{i}.png"
                zipf.write(file_name, os.path.basename(file_name))
        
        messagebox.showinfo("Success", f"{count} QR codes generated and saved to a zip file!")
    
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")


def download_zip_file():
    # Ask user where to save the zip file
    save_path = filedialog.asksaveasfilename(
        defaultextension=".zip",
        filetypes=[("Zip Files", "*.zip")],
        initialfile="qr_codes.zip",
    )
    if save_path:
        # Copy the generated zip file to the selected location
        with open(zip_file_path, "rb") as src, open(save_path, "wb") as dst:
            dst.write(src.read())
        messagebox.showinfo("Download", "QR code zip file downloaded successfully!")

# Set up the main GUI window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x350")

# Input field for QR code count
label_count = tk.Label(root, text="Enter number of QR codes to generate:")
label_count.pack(pady=10)

entry_count = tk.Entry(root, width=10)
entry_count.pack()

# Generate button
btn_generate = tk.Button(root, text="Generate", command=generate_qr_codes)
btn_generate.pack(pady=10)

# Frame to show preview of QR codes
frame_preview = tk.Frame(root)
frame_preview.pack(pady=10)

# Download button
btn_download = tk.Button(root, text="Download ZIP File", command=download_zip_file)
btn_download.pack(pady=10)

root.mainloop()
