from io import BytesIO
from PIL import Image
from rembg import remove
from config import COLORS

def remove_bg(image_bytes):
    return remove(image_bytes)

def create_bg(width, height, color):
    bg = Image.new('RGB', (width, height), COLORS[color])
    img_bytes = BytesIO()
    bg.save(img_bytes, format='PNG')
    return img_bytes.getvalue()

def apply_bg(foreground_bytes, background_bytes, mask):
    fg = Image.open(BytesIO(foreground_bytes))
    bg = Image.open(BytesIO(background_bytes)).resize(fg.size)
    
    result = bg.copy()
    result.paste(fg, (0, 0), mask)
    
    out = BytesIO()
    result.save(out, format='PNG')
    return out.getvalue()

def get_mask(image_bytes):
    img = Image.open(BytesIO(image_bytes))
    return img.getchannel('A'), img.size