import fitz  # PyMuPDF
import os
import sys

def analyze_pdf(pdf_path, output_dir="pdf_streams"):
    """
    Analyze all xref objects in a PDF and extract:
    - Raw and decoded streams
    - Images as PNG/JPEG if detected
    """
    if not os.path.isfile(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        return

    os.makedirs(output_dir, exist_ok=True)

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return

    print(f"Analyzing '{pdf_path}' ...")
    print(f"Total xref objects: {doc.xref_length()}")

    for xref in range(1, doc.xref_length()):
        try:
            obj_type = doc.xref_get_key(xref, "Type")[1]  # e.g., /Image, /Font, /Page
        except Exception:
            obj_type = None

        if doc.xref_is_stream(xref):
            try:
                filters = doc.xref_get_key(xref, "Filter")[1]
            except Exception:
                filters = None

            # Get raw stream
            try:
                raw_data = doc.xref_stream_raw(xref)
                raw_len = len(raw_data)
                raw_path = os.path.join(output_dir, f"xref_{xref}_raw.bin")
                with open(raw_path, "wb") as f:
                    f.write(raw_data)
            except Exception as e:
                print(f"[xref {xref}] Error reading raw stream: {e}")
                raw_data = b""
                raw_len = 0
                raw_path = None

            # Get decoded stream
            try:
                decoded_data = doc.xref_stream(xref)
                decoded_path = os.path.join(output_dir, f"xref_{xref}_decoded.bin")
                with open(decoded_path, "wb") as f:
                    f.write(decoded_data)
            except Exception as e:
                print(f"[xref {xref}] Error reading decoded stream: {e}")
                decoded_data = b""
                decoded_path = None

            # If it's an image, save it as PNG/JPEG
            if obj_type == "/Image":
                try:
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n < 5:  # RGB or grayscale
                        img_path = os.path.join(output_dir, f"xref_{xref}.png")
                        pix.save(img_path)
                    else:  # CMYK: convert to RGB first
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                        img_path = os.path.join(output_dir, f"xref_{xref}.png")
                        pix.save(img_path)
                    pix = None
                    print(f"[xref {xref}] Image extracted: {img_path}")
                except Exception as e:
                    print(f"[xref {xref}] Error extracting image: {e}")

            print(f"[xref {xref}] Stream object | Type: {obj_type} | Raw length: {raw_len} | Filter: {filters}")

        else:
            print(f"[xref {xref}] Non-stream object | Type: {obj_type}")

    doc.close()
    print(f"\nExtraction complete. Files saved in: {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_streams.py <PDF_FILE> [OUTPUT_DIR]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "pdf_streams"

    analyze_pdf(pdf_file, out_dir)
