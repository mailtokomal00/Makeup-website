import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_studio_background(width, height):
    # Create soft studio gradient background (warm beige/sand theme matching website)
    bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    arr = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Base background gradient (soft warm sand)
    for y in range(height):
        ratio = y / height
        r = int(238 - ratio * 15) # 238 to 223
        g = int(230 - ratio * 16) # 230 to 214
        b = int(220 - ratio * 18) # 220 to 202
        arr[y, :, 0] = r
        arr[y, :, 1] = g
        arr[y, :, 2] = b
        arr[y, :, 3] = 255
        
    img = Image.fromarray(arr, 'RGBA')
    
    # Add subtle central studio vignette / light highlight
    draw = ImageDraw.Draw(img)
    # Radial light in top center
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([width*0.1, -height*0.2, width*0.9, height*0.8], fill=(255, 252, 245, 45))
    overlay = overlay.filter(ImageFilter.GaussianBlur(80))
    img = Image.alpha_composite(img, overlay)
    
    # Draw soft studio pedestal at the bottom
    ped_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    ped_draw = ImageDraw.Draw(ped_overlay)
    
    ped_top = int(height * 0.70)
    # Pedestal top surface (ellipse)
    ped_draw.ellipse([width * 0.12, ped_top - 40, width * 0.88, ped_top + 100], fill=(245, 240, 233, 255))
    # Pedestal body
    ped_draw.rectangle([width * 0.12, ped_top + 30, width * 0.88, height], fill=(234, 227, 218, 255))
    ped_draw.ellipse([width * 0.12, height - 50, width * 0.88, height + 50], fill=(225, 217, 207, 255))
    
    # Blur pedestal edges slightly
    ped_overlay = ped_overlay.filter(ImageFilter.GaussianBlur(1))
    img = Image.alpha_composite(img, ped_overlay)
    
    return img

def add_drop_shadow(img, bbox, blur_radius=30, opacity=120):
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    draw.ellipse(bbox, fill=(35, 30, 25, opacity))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
    return Image.alpha_composite(img, shadow)


def generate_eyeshadow_product(width=1024, height=1024):
    bg = create_studio_background(width, height)
    
    # Drop shadow under palette
    bg = add_drop_shadow(bg, [width * 0.20, height * 0.62, width * 0.80, height * 0.75], blur_radius=40, opacity=130)
    
    # Palette Layer
    palette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(palette)
    
    # Main Palette Body (Angled 3D Opened Compact)
    # Outer Casing (Rose Gold / Champagne Metallic)
    p_left, p_top, p_right, p_bottom = int(width * 0.22), int(height * 0.35), int(width * 0.78), int(height * 0.68)
    
    # Shadow bevel
    draw.rounded_rectangle([p_left-4, p_top-4, p_right+4, p_bottom+4], radius=24, fill=(180, 140, 110, 100))
    # Outer Metallic Frame
    draw.rounded_rectangle([p_left, p_top, p_right, p_bottom], radius=20, fill=(28, 26, 25, 255))
    draw.rounded_rectangle([p_left+3, p_top+3, p_right-3, p_bottom-3], radius=18, outline=(212, 175, 120, 255), width=3)
    
    # Opened Top Lid (Angled upper reflection)
    lid_top, lid_bottom = int(height * 0.14), int(height * 0.34)
    draw.rounded_rectangle([p_left+10, lid_top, p_right-10, lid_bottom], radius=16, fill=(35, 32, 30, 255))
    # Mirror inset in lid
    draw.rounded_rectangle([p_left+24, lid_top+14, p_right-24, lid_bottom-10], radius=10, fill=(230, 235, 240, 255))
    # Mirror glare line
    draw.polygon([(p_left+30, lid_top+14), (p_left+120, lid_top+14), (p_left+60, lid_bottom-10), (p_left+30, lid_bottom-10)], fill=(255, 255, 255, 120))
    
    # Brand logo on mirror frame top
    try:
        font_logo = ImageFont.truetype("arial.ttf", 22)
    except:
        font_logo = ImageFont.load_default()
    
    draw.text((width * 0.5, lid_top + 8), "L U X E   B E A U T Y", fill=(212, 175, 120, 255), font=font_logo, anchor="mb")
    
    # Bottom Base - Eyeshadow Pan Grid (2 rows x 3 columns)
    pan_colors = [
        # (Name, Base RGB, Shimmer RGB)
        ("Rose Gold", (195, 120, 115), (245, 200, 190)),
        ("Champagne Shimmer", (225, 190, 145), (255, 240, 210)),
        ("Dusty Rose", (170, 95, 105), (210, 140, 150)),
        ("Bronze Glow", (145, 90, 60), (200, 145, 105)),
        ("Velvet Nude", (185, 145, 125), (225, 195, 175)),
        ("Golden Pearl", (210, 165, 95), (255, 225, 160))
    ]
    
    grid_left = p_left + 35
    grid_top = p_top + 25
    grid_width = p_right - p_left - 70
    grid_height = p_bottom - p_top - 50
    
    col_w = grid_width / 3
    row_h = grid_height / 2
    
    idx = 0
    for r in range(2):
        for c in range(3):
            cx = grid_left + c * col_w + col_w / 2
            cy = grid_top + r * row_h + row_h / 2
            rx, ry = col_w * 0.38, row_h * 0.38
            
            name, base_rgb, shim_rgb = pan_colors[idx]
            
            # Pan Metallic Rim
            draw.ellipse([cx - rx - 3, cy - ry - 3, cx + rx + 3, cy + ry + 3], fill=(180, 145, 100, 255))
            draw.ellipse([cx - rx - 1, cy - ry - 1, cx + rx + 1, cy + ry + 1], fill=(20, 18, 17, 255))
            
            # Powder Pan Base
            draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(*base_rgb, 255))
            
            # Powder Pressed Ring Texture
            draw.ellipse([cx - rx*0.75, cy - ry*0.75, cx + rx*0.75, cy + ry*0.75], outline=(*shim_rgb, 140), width=2)
            draw.ellipse([cx - rx*0.4, cy - ry*0.4, cx + rx*0.4, cy + ry*0.4], fill=(*shim_rgb, 180))
            
            # Highlight Specular Spot
            draw.ellipse([cx - rx*0.5, cy - ry*0.5, cx - rx*0.1, cy - ry*0.1], fill=(255, 255, 255, 150))
            
            idx += 1
            
    # Composite palette onto background
    palette = palette.filter(ImageFilter.GaussianBlur(0.5))
    final_img = Image.alpha_composite(bg, palette)
    
    # Add subtle luxury text below
    draw_final = ImageDraw.Draw(final_img)
    try:
        font_sub = ImageFont.truetype("georgia.ttf", 26)
    except:
        font_sub = ImageFont.load_default()
    draw_final.text((width * 0.5, height * 0.84), "ROSE GOLD EYESHADOW PALETTE", fill=(45, 40, 35, 230), font=font_sub, anchor="mm")
    
    return final_img

def generate_blush_product(width=1024, height=1024):
    bg = create_studio_background(width, height)
    
    # Drop shadow under compact
    bg = add_drop_shadow(bg, [width * 0.24, height * 0.60, width * 0.76, height * 0.74], blur_radius=38, opacity=140)
    
    # Blush Compact Layer
    blush = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(blush)
    
    cx, cy = width * 0.5, height * 0.48
    radius = int(width * 0.24)
    
    # Open Top Lid (angled behind compact)
    lid_cy = cy - radius * 0.85
    draw.ellipse([cx - radius*0.9, lid_cy - radius*0.8, cx + radius*0.9, lid_cy + radius*0.8], fill=(25, 23, 22, 255))
    draw.ellipse([cx - radius*0.85, lid_cy - radius*0.75, cx + radius*0.85, lid_cy + radius*0.75], fill=(212, 175, 120, 255))
    # Mirror inset
    draw.ellipse([cx - radius*0.78, lid_cy - radius*0.68, cx + radius*0.78, lid_cy + radius*0.68], fill=(235, 240, 245, 255))
    # Mirror glare
    draw.polygon([(cx - radius*0.5, lid_cy - radius*0.6), (cx + radius*0.2, lid_cy - radius*0.6), (cx - radius*0.2, lid_cy + radius*0.5), (cx - radius*0.7, lid_cy + radius*0.5)], fill=(255, 255, 255, 130))
    
    # Main Circular Compact Base
    # Outer Casing (Metallic Rose Gold Rim & Matte Black Base)
    draw.ellipse([cx - radius - 6, cy - radius - 6, cx + radius + 6, cy + radius + 6], fill=(190, 150, 110, 255))
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(28, 25, 24, 255))
    draw.ellipse([cx - radius + 4, cy - radius + 4, cx + radius - 4, cy + radius - 4], fill=(212, 175, 120, 255))
    draw.ellipse([cx - radius + 10, cy - radius + 10, cx + radius - 10, cy + radius - 10], fill=(20, 18, 17, 255))
    
    # Pressed Powder Pan (Soft Radiant Silk Pink Blush)
    p_rad = radius - 20
    draw.ellipse([cx - p_rad, cy - p_rad, cx + p_rad, cy + p_rad], fill=(225, 135, 145, 255))
    
    # Concentric Silk Wave Waves / Embossed Pattern
    for i in range(1, 6):
        r_i = p_rad * (i / 6)
        alpha = int(120 - i * 15)
        draw.ellipse([cx - r_i, cy - r_i, cx + r_i, cy + r_i], outline=(250, 195, 205, alpha), width=3)
        
    # Central Embossed Rose Motif / Shimmer Highlight
    draw.ellipse([cx - p_rad*0.35, cy - p_rad*0.35, cx + p_rad*0.35, cy + p_rad*0.35], fill=(240, 165, 175, 200))
    draw.ellipse([cx - p_rad*0.4, cy - p_rad*0.4, cx - p_rad*0.1, cy - p_rad*0.1], fill=(255, 230, 235, 140))
    
    # Fine Powder Dust Particles on Edge
    dust_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dust_overlay)
    np.random.seed(42)
    for _ in range(120):
        angle = np.random.uniform(0, 2*np.pi)
        dist = p_rad + np.random.uniform(-8, 14)
        px = cx + dist * np.cos(angle)
        py = cy + dist * np.sin(angle)
        pr = np.random.uniform(1, 3.5)
        d_draw.ellipse([px-pr, py-pr, px+pr, py+pr], fill=(235, 160, 170, np.random.randint(60, 180)))
        
    dust_overlay = dust_overlay.filter(ImageFilter.GaussianBlur(1))
    blush = Image.alpha_composite(blush, dust_overlay)
    
    # Composite blush compact onto background
    final_img = Image.alpha_composite(bg, blush)
    
    # Add subtle luxury title below
    draw_final = ImageDraw.Draw(final_img)
    try:
        font_sub = ImageFont.truetype("georgia.ttf", 26)
    except:
        font_sub = ImageFont.load_default()
    draw_final.text((width * 0.5, height * 0.84), "SILK SOFT POWDER BLUSH", fill=(45, 40, 35, 230), font=font_sub, anchor="mm")
    
    return final_img

if __name__ == '__main__':
    eyeshadow_img = generate_eyeshadow_product()
    eyeshadow_img.save(r'c:\Users\mailt\OneDrive\Desktop\makeup\images\eyeshadow.png')
    print("Generated c:\\Users\\mailt\\OneDrive\\Desktop\\makeup\\images\\eyeshadow.png")
    
    blush_img = generate_blush_product()
    blush_img.save(r'c:\Users\mailt\OneDrive\Desktop\makeup\images\blush.png')
    print("Generated c:\\Users\\mailt\\OneDrive\Desktop\\makeup\\images\\blush.png")
