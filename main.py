import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Increase the image size limit
Image.MAX_IMAGE_PIXELS = None

def split_image_from_folder(rows, cols, output_pdf):
    # Define the path to the image folder
    folder_path = r'F:\Visual Code\PosterRasor\image'

    # Get the list of image files in the folder and sort alphabetically
    images = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    if not images:
        print("No images found in the folder.")
        return

    # Load the first image in alphabetical order
    image_path = os.path.join(folder_path, images[0])
    image = Image.open(image_path)
    img_width, img_height = image.size

    # Calculate dimensions of each part
    part_width = img_width // cols
    part_height = img_height // rows

    # Create PDF canvas
    pdf = canvas.Canvas(output_pdf, pagesize=letter)
    pdf_width, pdf_height = letter

    for row in range(rows):
        for col in range(cols):
            # Calculate the crop box
            left = col * part_width
            upper = row * part_height
            right = left + part_width
            lower = upper + part_height

            # Crop the image
            part = image.crop((left, upper, right, lower))

            # Scale part to fit PDF page
            part = part.resize((int(pdf_width), int(pdf_height)), Image.LANCZOS)

            # Save each part to a PDF page
            pdf.drawInlineImage(part, 0, 0, width=pdf_width, height=pdf_height)
            pdf.showPage()

    # Save PDF
    pdf.save()
    print(f"Image {images[0]} split across {rows}x{cols} pages in {output_pdf}")

# Example usage:
split_image_from_folder(4, 6, r'F:\Visual Code\PosterRasor\output_image3.pdf')
