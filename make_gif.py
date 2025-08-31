from PIL import Image, ImageDraw, ImageFont
import math

# Load the original logo
logo_path = "/Users/g.m.sabbirahamed/Desktop/diulogoside.png"
logo = Image.open(logo_path).convert("RGBA")
w, h = logo.size

frames = []

# Animation parameters
zoom_min = 0.8
zoom_max = 1.0
zoom_frames = 20
rotation_frames = 40
pause_frames = 120

total_frames = zoom_frames * 2 + rotation_frames + pause_frames

def scale_image(img, scale):
    new_size = (int(w * scale), int(h * scale))
    return img.resize(new_size, Image.LANCZOS)

def simulate_3d_rotate(img, angle_deg):
    # Angle in radians
    angle = math.radians(angle_deg)
    # Horizontal squeeze factor simulating rotation around vertical axis
    squeeze = abs(math.cos(angle))
    if squeeze < 0.1:
        squeeze = 0.1  # avoid too thin

    # Width after squeezing
    new_w = int(w * squeeze)
    img_scaled = img.resize((new_w, h), Image.LANCZOS)

    # Create a blank transparent frame
    frame = Image.new("RGBA", (w, h), (0,0,0,0))
    # Paste squeezed image centered horizontally
    frame.paste(img_scaled, ((w - new_w)//2, 0), img_scaled)

    # Optional: skew effect can be added for more realism but kept simple here
    return frame

for i in range(total_frames):
    frame = Image.new("RGBA", (w, h), (0,0,0,0))

    if i < zoom_frames:
        # Zoom out: scale 1.0 -> 0.8
        scale = zoom_max - ( (zoom_max - zoom_min) * (i / zoom_frames) )
        img_scaled = scale_image(logo, scale)
        frame.paste(img_scaled, ((w - img_scaled.width)//2, (h - img_scaled.height)//2), img_scaled)

    elif i < zoom_frames * 2:
        # Zoom in: scale 0.8 -> 1.0
        idx = i - zoom_frames
        scale = zoom_min + ( (zoom_max - zoom_min) * (idx / zoom_frames) )
        img_scaled = scale_image(logo, scale)
        frame.paste(img_scaled, ((w - img_scaled.width)//2, (h - img_scaled.height)//2), img_scaled)

    elif i < zoom_frames * 2 + rotation_frames:
        # Rotation: 0 -> 360 degrees
        idx = i - (zoom_frames * 2)
        angle = (idx / rotation_frames) * 360
        frame = simulate_3d_rotate(logo, angle)

    else:
        # Pause: just show full logo at normal size
        frame.paste(logo, (0,0), logo)

    frames.append(frame)

frames[0].save(
    "diu_simple_animation3.gif",
    save_all=True,
    append_images=frames[1:],
    optimize=False,
    duration=50,  # ~20fps
    loop=0,  # infinite loop
    disposal=2  # Clear frame before next frame
)
