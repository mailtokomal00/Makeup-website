import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def generate_noise(width, height, scale=1.0):
    # Generates fine micro powder texture noise
    noise = np.random.normal(0, 15 * scale, (height, width)).astype(np.float32)
    return noise

def create_studio_background(width, height):
    # Ultra-smooth editorial studio background matching #EAE3D9
    arr = np.zeros((height, width, 4), dtype=np.float32)
    
    # Soft linear gradient from top (#FAF6F0) to bottom (#DFD7CC)
    for y in range(height):
        t = y / height
        r = 250 * (1 - t) + 223 * t
        g = 246 * (1 - t) + 215 * t
        b = 240 * (1 - t) + 204 * t
        arr[y, :, 0] = r
        arr[y, :, 1] = g
        arr[y, :, 2] = b
        arr[y, :, 3] = 255
        
    img = Image.fromarray(np.uint8(arr), 'RGBA')
    
    # Soft central spotlight effect
    spotlight = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    sp_draw = ImageDraw.Draw(spotlight)
    sp_draw.ellipse([width * 0.15, height * 0.05, width * 0.85, height * 0.75], fill=(255, 255, 252, 60))
    spotlight = spotlight.filter(ImageFilter.GaussianBlur(100))
    img = Image.alpha_composite(img, spotlight)
    
    # Smooth Studio Pedestal Surface
    ped_y = int(height * 0.68)
    ped = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(ped)
    
    # Pedestal Top Ellipse Surface
    p_draw.ellipse([width * 0.10, ped_y - 50, width * 0.90, ped_y + 110], fill=(244, 238, 230, 255))
    # Pedestal Front Rim & Base
    p_draw.rectangle([width * 0.10, ped_y + 30, width * 0.90, height], fill=(232, 224, 214, 255))
    p_draw.ellipse([width * 0.10, height - 60, width * 0.90, height + 60], fill=(220, 212, 202, 255))
    
    ped = ped.filter(ImageFilter.GaussianBlur(1.5))
    img = Image.alpha_composite(img, ped)
    
    # Soft contact shadow line on pedestal edge
    shadow_line = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    sl_draw = ImageDraw.Draw(shadow_line)
    sl_draw.ellipse([width * 0.10, ped_y + 25, width * 0.90, ped_y + 35], fill=(160, 150, 140, 70))
    shadow_line = shadow_line.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img, shadow_line)
    
    return img

def render_eyeshadow_palette(width=1024, height=1024):
    bg = create_studio_background(width, height)
    
    # Soft Ambient Shadow on Pedestal
    shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow)
    sh_draw.ellipse([width * 0.18, height * 0.61, width * 0.82, height * 0.74], fill=(30, 25, 20, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(42))
    bg = Image.alpha_composite(bg, shadow)
    
    # Palette Layer
    palette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(palette)
    
    # Palette Outer Casing Coordinates
    p_left, p_top, p_right, p_bottom = int(width * 0.22), int(height * 0.36), int(width * 0.78), int(height * 0.67)
    
    # Outer Metallic Frame (Rose Gold Metallic Bevel)
    draw.rounded_rectangle([p_left-3, p_top-3, p_right+3, p_bottom+3], radius=22, fill=(210, 165, 125, 255))
    draw.rounded_rectangle([p_left, p_top, p_right, p_bottom], radius=20, fill=(26, 24, 23, 255))
    draw.rounded_rectangle([p_left+3, p_top+3, p_right-3, p_bottom-3], radius=18, outline=(195, 145, 100, 255), width=2)
    
    # Opened Lid (Angled upper section with mirror)
    lid_top, lid_bottom = int(height * 0.15), int(height * 0.35)
    draw.rounded_rectangle([p_left+8, lid_top, p_right-8, lid_bottom], radius=16, fill=(32, 29, 28, 255))
    draw.rounded_rectangle([p_left+12, lid_top+4, p_right-12, lid_bottom-2], radius=14, outline=(180, 135, 90, 255), width=2)
    
    # Glass Mirror Inset with Light Reflection
    mirror_box = [p_left+24, lid_top+14, p_right-24, lid_bottom-10]
    draw.rounded_rectangle(mirror_box, radius=10, fill=(225, 232, 238, 255))
    
    # Glare rays across mirror
    glare = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glare)
    g_draw.polygon([(p_left+30, lid_top+14), (p_left+140, lid_top+14), (p_left+70, lid_bottom-10), (p_left+30, lid_bottom-10)], fill=(255, 255, 255, 140))
    g_draw.polygon([(p_left+160, lid_top+14), (p_left+220, lid_top+14), (p_left+150, lid_bottom-10), (p_left+90, lid_bottom-10)], fill=(255, 255, 255, 70))
    glare = glare.filter(ImageFilter.GaussianBlur(2))
    palette = Image.alpha_composite(palette, glare)
    draw = ImageDraw.Draw(palette)
    
    # Logo on top mirror frame
    try:
        font_logo = ImageFont.truetype("arial.ttf", 20)
    except:
        font_logo = ImageFont.load_default()
    draw.text((width * 0.5, lid_top + 8), "L U X E   B E A U T Y", fill=(212, 175, 120, 255), font=font_logo, anchor="mb")
    
    # Bottom Base - 6 Eyeshadow Pans
    pan_colors = [
        ("Rose Gold Shimmer", (205, 130, 120), (250, 210, 195)),
        ("Champagne Glow", (230, 195, 150), (255, 245, 220)),
        ("Velvet Mauve", (165, 95, 110), (215, 145, 160)),
        ("Bronze Radiance", (150, 95, 65), (210, 155, 115)),
        ("Soft Terracotta", (190, 125, 95), (235, 175, 145)),
        ("Golden Silk", (215, 170, 100), (255, 230, 165))
    ]
    
    grid_left = p_left + 35
    grid_top = p_top + 22
    grid_width = p_right - p_left - 70
    grid_height = p_bottom - p_top - 44
    
    col_w = grid_width / 3
    row_h = grid_height / 2
    
    idx = 0
    for r in range(2):
        for c in range(3):
            cx = int(grid_left + c * col_w + col_w / 2)
            cy = int(grid_top + r * row_h + row_h / 2)
            rx, ry = int(col_w * 0.38), int(row_h * 0.38)
            
            name, base_rgb, shim_rgb = pan_colors[idx]
            
            # Metal Pan Bevel Rim
            draw.ellipse([cx - rx - 3, cy - ry - 3, cx + rx + 3, cy + ry + 3], fill=(185, 145, 105, 255))
            draw.ellipse([cx - rx - 1, cy - ry - 1, cx + rx + 1, cy + ry + 1], fill=(15, 14, 13, 255))
            
            # Base Powder Fill
            draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(*base_rgb, 255))
            
            # Add Realistic Micro Powder Texture Noise & Specular Shimmer
            pan_w, pan_h = rx * 2, ry * 2
            pan_img = Image.new('RGBA', (pan_w, pan_h), (0, 0, 0, 0))
            p_draw = ImageDraw.Draw(pan_img)
            p_draw.ellipse([0, 0, pan_w, pan_h], fill=(*base_rgb, 255))
            
            pan_arr = np.array(pan_img).astype(np.float32)
            noise = generate_noise(pan_w, pan_h, scale=0.8)
            
            for channel in range(3):
                pan_arr[:, :, channel] = np.clip(pan_arr[:, :, channel] + noise, 0, 255)
                
            pan_img = Image.fromarray(np.uint8(pan_arr), 'RGBA')
            
            # Shimmer Highlight overlay
            shim = Image.new('RGBA', (pan_w, pan_h), (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(shim)
            s_draw.ellipse([pan_w*0.2, pan_h*0.2, pan_w*0.8, pan_h*0.8], fill=(*shim_rgb, 130))
            s_draw.ellipse([pan_w*0.25, pan_h*0.25, pan_w*0.5, pan_h*0.5], fill=(255, 255, 255, 160))
            shim = shim.filter(ImageFilter.GaussianBlur(4))
            
            pan_img = Image.alpha_composite(pan_img, shim)
            
            # Mask to circle
            mask = Image.new('L', (pan_w, pan_h), 0)
            m_draw = ImageDraw.Draw(mask)
            m_draw.ellipse([0, 0, pan_w, pan_h], fill=255)
            
            palette.paste(pan_img, (cx - rx, cy - ry), mask)
            draw = ImageDraw.Draw(palette)
            
            idx += 1
            
    palette = palette.filter(ImageFilter.GaussianBlur(0.3))
    final_img = Image.alpha_composite(bg, palette)
    
    return final_img

def render_blush_compact(width=1024, height=1024):
    bg = create_studio_background(width, height)
    
    # Soft Ambient Shadow on Pedestal
    shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow)
    sh_draw.ellipse([width * 0.22, height * 0.59, width * 0.78, height * 0.73], fill=(30, 25, 20, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(40))
    bg = Image.alpha_composite(bg, shadow)
    
    blush = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(blush)
    
    cx, cy = int(width * 0.5), int(height * 0.47)
    radius = int(width * 0.25)
    
    # Opened Lid (Angled mirror top lid behind compact)
    lid_cy = cy - int(radius * 0.85)
    draw.ellipse([cx - int(radius*0.92), lid_cy - int(radius*0.8), cx + int(radius*0.92), lid_cy + int(radius*0.8)], fill=(24, 22, 21, 255))
    draw.ellipse([cx - int(radius*0.88), lid_cy - int(radius*0.75), cx + int(radius*0.88), lid_cy + int(radius*0.75)], fill=(210, 165, 120, 255))
    draw.ellipse([cx - int(radius*0.82), lid_cy - int(radius*0.68), cx + int(radius*0.82), lid_cy + int(radius*0.68)], fill=(230, 238, 245, 255))
    
    # Mirror Glare
    glare = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glare)
    g_draw.polygon([(cx - radius*0.5, lid_cy - radius*0.6), (cx + radius*0.3, lid_cy - radius*0.6), (cx - radius*0.1, lid_cy + radius*0.5), (cx - radius*0.7, lid_cy + radius*0.5)], fill=(255, 255, 255, 140))
    glare = glare.filter(ImageFilter.GaussianBlur(2))
    blush = Image.alpha_composite(blush, glare)
    draw = ImageDraw.Draw(blush)
    
    # Main Circular Metallic Compact Base (Rose Gold & Obsidian Black)
    draw.ellipse([cx - radius - 5, cy - radius - 5, cx + radius + 5, cy + radius + 5], fill=(195, 150, 110, 255))
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(28, 25, 24, 255))
    draw.ellipse([cx - radius + 4, cy - radius + 4, cx + radius - 4, cy + radius - 4], fill=(210, 165, 120, 255))
    draw.ellipse([cx - radius + 8, cy - radius + 8, cx + radius - 8, cy + radius - 8], fill=(18, 16, 15, 255))
    
    # Pressed Powder Pan Fill
    p_rad = radius - 18
    pan_w, pan_h = p_rad * 2, p_rad * 2
    pan_img = Image.new('RGBA', (pan_w, pan_h), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(pan_img)
    
    base_pink = (230, 130, 145)
    p_draw.ellipse([0, 0, pan_w, pan_h], fill=(*base_pink, 255))
    
    # Add Texture & Concentric Waves Motif
    pan_arr = np.array(pan_img).astype(np.float32)
    noise = generate_noise(pan_w, pan_h, scale=0.7)
    for ch in range(3):
        pan_arr[:, :, ch] = np.clip(pan_arr[:, :, ch] + noise, 0, 255)
    pan_img = Image.fromarray(np.uint8(pan_arr), 'RGBA')
    p_draw = ImageDraw.Draw(pan_img)
    
    for i in range(1, 7):
        r_i = p_rad * (i / 7)
        p_draw.ellipse([p_rad - r_i, p_rad - r_i, p_rad + r_i, p_rad + r_i], outline=(255, 205, 215, 130), width=2)
        
    # Specular Lighting Highlight
    shim = Image.new('RGBA', (pan_w, pan_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shim)
    s_draw.ellipse([pan_w*0.2, pan_h*0.2, pan_w*0.7, pan_h*0.7], fill=(255, 220, 228, 150))
    s_draw.ellipse([pan_w*0.25, pan_h*0.25, pan_w*0.48, pan_h*0.48], fill=(255, 245, 248, 180))
    shim = shim.filter(ImageFilter.GaussianBlur(10))
    pan_img = Image.alpha_composite(pan_img, shim)
    
    # Mask to circular pan
    mask = Image.new('L', (pan_w, pan_h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.ellipse([0, 0, pan_w, pan_h], fill=255)
    
    blush.paste(pan_img, (cx - p_rad, cy - p_rad), mask)
    
    # Soft Powder Dust Effect
    dust = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dust)
    np.random.seed(99)
    for _ in range(90):
        angle = np.random.uniform(0, 2*np.pi)
        dist = p_rad + np.random.uniform(-4, 12)
        px = cx + dist * np.cos(angle)
        py = cy + dist * np.sin(angle)
        pr = np.random.uniform(1.2, 3.0)
        d_draw.ellipse([px-pr, py-pr, px+pr, py+pr], fill=(240, 160, 175, np.random.randint(70, 190)))
    dust = dust.filter(ImageFilter.GaussianBlur(0.8))
    blush = Image.alpha_composite(blush, dust)
    
    blush = blush.filter(ImageFilter.GaussianBlur(0.3))
    final_img = Image.alpha_composite(bg, blush)
    
    return final_img

if __name__ == '__main__':
    eyeshadow_img = render_eyeshadow_palette()
    eyeshadow_img.save(r'c:\Users\mailt\OneDrive\Desktop\makeup\images\eyeshadow.png')
    print("Successfully generated eyeshadow.png")
    
    blush_img = render_blush_compact()
    blush_img.save(r'c:\Users\mailt\OneDrive\Desktop\makeup\images\blush.png')
    print("Successfully generated blush.png")
