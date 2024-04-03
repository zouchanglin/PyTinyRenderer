from PIL import Image

# Create a new image with RGB mode
image = Image.new('RGB', (50, 50))

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
# Set the color of a pixel
# Parameters: (x, y, color)
image.putpixel((24, 25), red)  # set the pixel at (50, 50) to red
image.putpixel((25, 25), green)  # set the pixel at (50, 50) to red
image.putpixel((26, 25), blue)  # set the pixel at (50, 50) to red

# Save the image
image.save('output.png')
