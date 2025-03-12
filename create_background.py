from PIL import Image, ImageDraw

def create_background():
    # Create a new image with a gradient background
    width = 800
    height = 600
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Create a simple gradient background
    for y in range(height):
        # Calculate color based on y position
        r = int(50 + (y / height) * 50)  # Dark blue to slightly lighter blue
        g = int(50 + (y / height) * 50)
        b = int(100 + (y / height) * 100)
        
        # Draw a line with the calculated color
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # Add some simple decorative elements
    for i in range(50):
        x = (i * 20) % width
        y = (i * 15) % height
        size = 3
        draw.ellipse([x-size, y-size, x+size, y+size], fill=(255, 255, 255, 128))
    
    # Save the image
    image.save('assets/images/background.png')

if __name__ == "__main__":
    create_background() 