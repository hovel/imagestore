from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from django.conf import settings

def watermark(im, requested_size, opts):
    width, height = im.size
    font_scale = settings.IMAGESTORE_FONT_SCALE
    text = settings.IMAGESTORE_WATERMARK_TEXT
    font_size = int(font_scale*height)
    if font_size < 5:
        font_size = 5
    margin = (int(width*0.05), int(height*0.05))
    im0 = watermarkit(im, text, font_size, margin=margin, font_name=settings.IMAGESTORE_WATERMARK_FONT)
    return im0

def watermarkit(image, text, font_size=90, font_name = 'tahoma.ttf', opacity = 0.6, color=(0,0,0), margin=(30,30)):
    font=ImageFont.truetype(font_name, font_size)
    im0 = Imprint(image, text, font=font, opacity=opacity, color=color, margin=margin)
    return im0

def ReduceOpacity(im, opacity):
    """
    Returns an image with reduced opacity.
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879
    """
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def Imprint(im, inputtext, font=None, color=None, opacity=0.6, margin=(30,30)):
    """
    imprints a PIL image with the indicated text in lower-right corner
    """
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    textlayer = Image.new("RGBA", im.size, (0,0,0,0))
    textdraw = ImageDraw.Draw(textlayer)
    textsize = textdraw.textsize(inputtext, font=font)
    textpos = [im.size[i]-textsize[i]-margin[i] for i in [0,1]]
    textdraw.text(textpos, inputtext, font=font, fill=color)
    if opacity != 1:
        textlayer = ReduceOpacity(textlayer,opacity)
    return Image.composite(textlayer, im, textlayer)
 

