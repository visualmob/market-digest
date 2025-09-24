from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap

def _load_font(size):
    try:
        # Try DejaVuSans bundled with many distros
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        # Fallback to default bitmap font (smaller)
        return ImageFont.load_default()

def make_card(date_str, bullets, indices_line, sectors_str, out_path="daily.png"):
    W,H = 1080,1350
    pad = 60
    img = Image.new("RGB",(W,H),(18,18,22))
    d = ImageDraw.Draw(img)
    font_title = _load_font(64)
    font_sub   = _load_font(40)
    font_body  = _load_font(36)

    d.text((pad,pad), "Daily Market Bites — " + date_str, font=font_title, fill=(240,240,240))
    d.text((pad,pad+110), indices_line, font=font_sub, fill=(210,210,210))

    y=pad+180
    maxw = 46
    for b in bullets:
        for line in wrap(b, width=maxw):
            d.text((pad,y), line, font=font_body, fill=(235,235,235))
            y+=48
        y+=18

    # Trim sectors if too long
    sectors_wrapped = wrap(sectors_str, width=52)
    d.text((pad, y+24), sectors_wrapped[0] if sectors_wrapped else "", font=font_sub, fill=(200,200,200))
    if len(sectors_wrapped) > 1:
        d.text((pad, y+24+48), sectors_wrapped[1], font=font_sub, fill=(200,200,200))

    img.save(out_path, "PNG")
    return out_path
