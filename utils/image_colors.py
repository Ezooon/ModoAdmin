import collections

from PIL import Image
from kivy.graphics.texture import Texture
import array


def kivy_to_pil(kivy_image):
    # Get Kivy image texture
    texture = kivy_image.texture

    # Get the image data
    image_data = texture.pixels

    # Convert the data to a 1D array
    arr = array.array('B', image_data)

    # Convert the array to a bytes object
    image_bytes = arr.tobytes()

    # Create a PIL Image from the bytes, using the original image's size and mode
    pil_image = Image.frombytes(mode='RGBA', size=(texture.width, texture.height), data=image_bytes)

    return pil_image


def get_accent_color(image):
    # Open the image file
    # Resize the image to speed up processing
    img = kivy_to_pil(image)

    img = img.resize((50, 50))

    # Get colors
    colors = img.getcolors(img.size[0]*img.size[1])

    # Sort them by count
    sorted_colors = sorted(colors, key=lambda x: x[0], reverse=True)

    # Get the most frequent color
    accent_color = sorted_colors[0][1]

    return [v/255 for v in accent_color]
