import os
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

# Configuration
IMAGES_INPUT_DIR = "images2"
COMPOSITE_OUTPUT_DIR = "images2_composite"
BRAND_COLOR = (25, 42, 86)  # Dark navy
PERSON_HEIGHT = 400
SHADOW_BLUR = 15
SHADOW_OPACITY = 0.3
SPACING = 30

os.makedirs(COMPOSITE_OUTPUT_DIR, exist_ok=True)

def create_shadow_layer(width, height):
    """Create a soft shadow layer beneath a portrait."""
    shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    
    # Draw ellipse shadow at bottom
    shadow_height = height // 8
    shadow_top = height - shadow_height - 20
    
    draw.ellipse(
        [(width * 0.1, shadow_top), (width * 0.9, height - 20)],
        fill=(0, 0, 0, int(255 * SHADOW_OPACITY))
    )
    
    # Blur the shadow
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=SHADOW_BLUR))
    return shadow

def resize_maintain_aspect(img, target_height=PERSON_HEIGHT):
    """Resize image maintaining aspect ratio."""
    ratio = target_height / img.height
    new_width = int(img.width * ratio)
    return img.resize((new_width, target_height), Image.Resampling.LANCZOS)

def add_shadow_to_image(img):
    """Add shadow layer to image."""
    shadow = create_shadow_layer(img.width, img.height)
    result = Image.new('RGBA', img.size, (0, 0, 0, 0))
    result.paste(shadow, (0, 0), shadow)
    result.paste(img, (0, 0), img)
    return result

def create_group_composition(image_files, output_path, bg_color=BRAND_COLOR):
    """Arrange multiple images into a group photo composition."""
    portraits = []
    total_width = 0
    max_height = 0
    
    # Load and prepare all images
    for img_file in sorted(image_files):
        try:
            img_path = os.path.join(IMAGES_INPUT_DIR, img_file)
            img = Image.open(img_path).convert('RGBA')
            
            # Resize to standard height
            img = resize_maintain_aspect(img, PERSON_HEIGHT)
            
            # Add shadow
            img_with_shadow = add_shadow_to_image(img)
            portraits.append(img_with_shadow)
            
            total_width += img_with_shadow.width + SPACING
            max_height = max(max_height, img_with_shadow.height)
            
            print(f"  ✓ Loaded: {img_file}")
        except Exception as e:
            print(f"  ✗ Failed to load {img_file}: {e}")
    
    if not portraits:
        print("No valid images found!")
        return False
    
    # Calculate canvas dimensions
    total_width -= SPACING  # Remove last spacing
    total_width += SPACING * 2  # Add padding on sides
    total_height = max_height + SPACING * 2
    
    # Create background
    background = Image.new('RGBA', (total_width, total_height), (*bg_color, 255))
    
    # Place portraits
    current_x = SPACING
    for portrait in portraits:
        y_pos = (total_height - portrait.height) // 2  # Center vertically
        background.paste(portrait, (current_x, y_pos), portrait)
        current_x += portrait.width + SPACING
    
    # Save composition
    background.save(output_path, 'PNG')
    return True

def main():
    print("Creating team group photo from employee images...")
    
    # Get all PNG images from images2 folder
    image_files = [f for f in os.listdir(IMAGES_INPUT_DIR) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print("No images found in images2 folder!")
        return
    
    print(f"\nFound {len(image_files)} employee photos:")
    
    # Create group composition
    output_path = os.path.join(COMPOSITE_OUTPUT_DIR, "team_group_photo.png")
    
    if create_group_composition(image_files, output_path, bg_color=BRAND_COLOR):
        print(f"\n✓ Group photo created successfully!")
        print(f"Output: {output_path}")
    else:
        print("Failed to create group composition.")

if __name__ == "__main__":
    main()
