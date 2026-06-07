from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string
import io

def generate_captcha_image(text=None):
    """
    Generates a CAPTCHA image and returns the image bytes and the text.
    """
    if text is None:
        # Generate random text: 5 characters, digits and uppercase
        text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    
    # Image dimensions
    width = 160
    height = 60
    
    # Create image with white background
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Add noise (lines)
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line(((x1, y1), (x2, y2)), fill=(200, 200, 200), width=2)
        
    # Add noise (points)
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(100, 100, 100))

    # Try to load a font, fall back to default if necessary
    try:
        # Using a standard font often available on Windows/Linux
        # On Windows 'arial.ttf' is common.
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        try:
             # Linux fallback
             font = ImageFont.truetype("DejaVuSans.ttf", 36)
        except IOError:
             # Absolute fallback
             font = ImageFont.load_default()

    # Calculate text size (approximate centering)
    # Pillow 10+ uses getbbox or getlength, old Pillow uses getsize
    # Let's use basic iteration or approximate positioning
    char_width = 25
    x_pos = 15
    
    for char in text:
        # Randomize Y position and color for each char
        y_pos = random.randint(5, 15)
        color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        draw.text((x_pos, y_pos), char, font=font, fill=color)
        x_pos += char_width

    # Apply a slight blur filter
    image = image.filter(ImageFilter.SMOOTH)
    
    # Save to bytes
    byte_io = io.BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)
    
    return byte_io, text
