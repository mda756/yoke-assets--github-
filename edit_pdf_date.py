import fitz  # PyMuPDF
import sys

# Open the PDF
pdf_path = "claude code creator/YokeDigital_PurchaseOrder 2024.pdf"
doc = fitz.open(pdf_path)

# Get the first page
page = doc[0]

# Search for the old date text
old_date = "28-10-24"
new_date = "29-01-26"

# Find all instances of the old date
text_instances = page.search_for(old_date)

if text_instances:
    print(f"Found {len(text_instances)} instance(s) of '{old_date}'")

    # For each instance found
    for inst in text_instances:
        # Add a white rectangle to cover the old text
        page.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))

        # Insert the new date at the same position
        page.insert_text(
            (inst.x0, inst.y1 - 2),  # Position (slightly adjusted for better alignment)
            new_date,
            fontsize=11,
            color=(0, 0, 0)
        )

    # Save the modified PDF
    output_path = "claude code creator/YokeDigital_PurchaseOrder 2024_updated.pdf"
    doc.save(output_path)
    print(f"PDF saved as: {output_path}")
    print(f"Date changed from {old_date} to {new_date}")
else:
    print(f"Date '{old_date}' not found in the PDF")

doc.close()
