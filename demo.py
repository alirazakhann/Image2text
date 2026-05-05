"""
Demo script to test the handwriting converter functionality
"""

from PIL import Image, ImageDraw, ImageFont
import io
import base64

def create_sample_handwritten_image():
    """
    Create a sample handwritten-style image for testing
    """
    # Create a white background
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a handwriting-like font, fallback to default
    try:
        # You might need to install a handwriting font or use system fonts
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Sample handwritten content
    y_pos = 50
    
    # Title
    draw.text((50, y_pos), "Physics Notes - Chapter 3", fill='black', font=font_large)
    y_pos += 50
    
    # Bullet points
    draw.text((50, y_pos), "• Newton's Laws of Motion:", fill='black', font=font_medium)
    y_pos += 30
    draw.text((70, y_pos), "1. Law of Inertia", fill='black', font=font_small)
    y_pos += 25
    draw.text((70, y_pos), "2. F = ma", fill='black', font=font_small)
    y_pos += 25
    draw.text((70, y_pos), "3. Action-Reaction", fill='black', font=font_small)
    y_pos += 40
    
    # Mathematical equation
    draw.text((50, y_pos), "Kinetic Energy: KE = ½mv²", fill='black', font=font_medium)
    y_pos += 40
    
    # Table header
    draw.text((50, y_pos), "Comparison Table:", fill='black', font=font_medium)
    y_pos += 30
    
    # Simple table
    draw.text((50, y_pos), "Object    | Mass (kg) | Velocity (m/s)", fill='black', font=font_small)
    y_pos += 20
    draw.text((50, y_pos), "---------|-----------|---------------", fill='black', font=font_small)
    y_pos += 20
    draw.text((50, y_pos), "Car      | 1000      | 20", fill='black', font=font_small)
    y_pos += 20
    draw.text((50, y_pos), "Ball     | 0.5       | 15", fill='black', font=font_small)
    y_pos += 40
    
    # Figure description
    draw.text((50, y_pos), "[FIGURE: Force diagram showing vectors]", fill='black', font=font_small)
    y_pos += 30
    
    # Draw a simple diagram
    draw.rectangle([400, 200, 600, 300], outline='black', width=2)
    draw.text((450, 240), "Block", fill='black', font=font_small)
    
    # Force arrows
    draw.line([500, 200, 500, 150], fill='black', width=3)  # Up arrow
    draw.text((510, 160), "N", fill='black', font=font_small)
    
    draw.line([500, 300, 500, 350], fill='black', width=3)  # Down arrow
    draw.text((510, 320), "mg", fill='black', font=font_small)
    
    return image

def save_sample_image():
    """Save a sample image for testing"""
    image = create_sample_handwritten_image()
    image.save("sample_handwritten_notes.png")
    print("Sample image saved as 'sample_handwritten_notes.png'")
    print("You can use this image to test the converter!")

if __name__ == "__main__":
    save_sample_image()