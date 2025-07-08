from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os

def generate_pdf(timestamp=None, output_path=None):
    try:
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if output_path is None:
            output_path = 'static/report.pdf'

        if os.path.exists(output_path):
            os.remove(output_path)
            print(f"[🗑️] Removed old PDF: {output_path}")

        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        margin = 50

        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin, height - margin, "SOMA - Moon Boulder Detection Report")
        c.setFont("Helvetica", 10)
        c.drawString(margin, height - margin - 15, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.setStrokeColorRGB(0.5, 0.5, 0.5)
        c.setLineWidth(0.5)
        c.line(margin, height - margin - 25, width - margin, height - margin - 25)

        # Stats Summary with spacing
        y = height - margin - 50
        stats_file = "static/stats_summary.txt"
        if os.path.exists(stats_file):
            with open(stats_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if y < margin + 100:
                        c.showPage()
                        y = height - margin - 50
                        c.setFont("Helvetica", 10)

                    clean_line = ''.join(char for char in line.strip() if ord(char) < 128)

                    if clean_line.endswith(('SUMMARY', 'DISTRIBUTION', 'COVERAGE')):
                        y -= 15
                        c.setFont("Helvetica-Bold", 11)
                        c.setFillColorRGB(0.2, 0.2, 0.2)
                        c.drawString(margin, y, clean_line)
                        c.setFillColorRGB(0, 0, 0)
                        y -= 12
                    elif clean_line.startswith('-') or clean_line.startswith('='):
                        continue
                    elif clean_line:
                        c.setFont("Helvetica", 10)
                        c.drawString(margin, y, clean_line[:100])
                        y -= 10
                    else:
                        y -= 6
        else:
            c.drawString(margin, y, "Statistics summary not available.")
            y -= 15

        # Image drawing function
        def draw_image(title, path, y_offset):
            nonlocal c

            scaled_height = 0
            if os.path.exists(path):
                try:
                    img = ImageReader(path)
                    img_width, img_height = img.getSize()
                    max_width = width - 2 * margin
                    max_height = 250
                    aspect_ratio = img_width / img_height
                    if max_width / aspect_ratio <= max_height:
                        scaled_width = max_width
                        scaled_height = max_width / aspect_ratio
                    else:
                        scaled_height = max_height
                        scaled_width = max_height * aspect_ratio

                    if y_offset - scaled_height - 45 < margin:
                        c.showPage()
                        y_offset = height - margin - 50

                except:
                    scaled_height = 0

            # Draw header after potential page break
            c.setFont("Helvetica-Bold", 12)
            c.setFillColorRGB(0.2, 0.2, 0.2)
            c.drawCentredString(width / 2, y_offset, title)
            c.setStrokeColorRGB(0.7, 0.7, 0.7)
            c.setLineWidth(0.5)
            c.line(margin, y_offset - 5, width - margin, y_offset - 5)
            c.setFillColorRGB(0, 0, 0)
            y_offset -= 25

            if os.path.exists(path):
                try:
                    x_pos = (width - scaled_width) / 2
                    y_pos = y_offset - scaled_height
                    c.drawImage(path, x_pos, y_pos, scaled_width, scaled_height)
                    y_offset = y_pos - 30
                    print(f"[📷] Added image to PDF: {title}")

                except Exception as e:
                    c.setFont("Helvetica", 9)
                    c.drawString(margin, y_offset, f"Could not load image: {os.path.basename(path)}")
                    y_offset -= 15
                    print(f"[⚠️] Could not add image {path}: {str(e)}")
            else:
                c.setFont("Helvetica", 9)
                c.drawString(margin, y_offset, f"Image not found: {os.path.basename(path)}")
                y_offset -= 15
                print(f"[⚠️] Image not found: {path}")

            return y_offset

        # Images section
        y = draw_image("1. Original Image", "static/preview.jpg", y)
        y = draw_image("2. Detected Boulders", "static/boulders_detected.jpg", y)
        y = draw_image("3. Detected Landslide", "static/landslides_detected.jpg", y)
        y = draw_image("4. Boulder Clustering Analysis", "static/clustered_boulders_plot.jpg", y)
        y = draw_image("5. Risk Assessment Heatmap", "static/risk_heatmap.jpg", y)
        y = draw_image("6. Source Point Analysis", "static/boulders_with_source.jpg", y)

        # Final page
        c.showPage()
        y = height - margin - 70
        c.setFont("Helvetica-Bold", 16)
        c.setFillColorRGB(0.1, 0.1, 0.1)
        c.drawCentredString(width / 2, y, "✅ Analysis Complete")
        y -= 30
        c.setFillColorRGB(0, 0, 0)

        c.setFont("Helvetica", 10)
        final_lines = [
            "This report contains comprehensive analysis of lunar boulder distribution,",
            "clustering patterns, risk assessment, and source point estimation.",
            "All analysis performed using advanced computer vision and machine learning techniques."
        ]
        for line in final_lines:
            c.drawCentredString(width / 2, y, line)
            y -= 15

        # Footer
        def add_footer(page_num):
            footer_text = "SOMA - Advanced Lunar Analysis System | Generated by Clueless Coders"
            c.setFont("Helvetica-Oblique", 8)
            c.setFillColorRGB(0.4, 0.4, 0.4)
            c.setStrokeColorRGB(0.8, 0.8, 0.8)
            c.setLineWidth(0.25)
            c.line(margin, margin, width - margin, margin)
            c.drawCentredString(width / 2, margin - 10, footer_text)
            
            c.setFillColorRGB(0, 0, 0)

        add_footer(1)
        c.save()
        print(f"[✅] Fresh PDF report saved to: {output_path}")
        return output_path

    except Exception as e:
        print(f"[❌] Failed to generate PDF: {str(e)}")
        try:
            c = canvas.Canvas(output_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, "PDF Generation Error")
            c.setFont("Helvetica", 12)
            c.drawString(50, 720, f"Error: {str(e)}")
            c.drawString(50, 700, "Please try uploading your image again.")
            c.save()
            print(f"[📄] Error PDF created: {output_path}")
        except:
            pass
        return None
