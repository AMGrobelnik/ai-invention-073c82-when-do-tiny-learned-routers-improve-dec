#!/usr/bin/env python3
"""
Convert PDF pages to PNG images for visual review.
"""
import sys
try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf"])
    import fitz

def convert_pdf_to_images(pdf_path, output_dir, dpi=150):
    """Convert PDF pages to PNG images."""
    import os
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Open PDF
    doc = fitz.open(pdf_path)
    
    print(f"Converting {len(doc)} pages at {dpi} DPI...")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Calculate zoom factor for DPI
        zoom = dpi / 72  # 72 DPI is the base
        mat = fitz.Matrix(zoom, zoom)
        
        # Render page to pixmap
        pix = page.get_pixmap(matrix=mat)
        
        # Save as PNG
        output_path = os.path.join(output_dir, f"page_{page_num + 1:02d}.png")
        pix.save(output_path)
        print(f"  Saved {output_path}")
    
    doc.close()
    print(f"\nDone! Converted {len(doc)} pages to {output_dir}/")

if __name__ == "__main__":
    pdf_path = "paper.pdf"
    output_dir = "page_images"
    convert_pdf_to_images(pdf_path, output_dir, dpi=150)
