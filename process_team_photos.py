import os
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np
from pathlib import Path

# Configuration
IMAGES_INPUT_DIR = "images2"
IMAGES_OUTPUT_DIR = "images2_processed"
COMPOSITE_OUTPUT_DIR = "images2_composite"
BRAND_COLOR = (25, 42, 86)  # Dark navy
PERSON_HEIGHT = 400
SHADOW_BLUR = 15
SHADOW_OPACITY = 0.3
SPACING = 30

os.makedirs(IMAGES_OUTPUT_DIR, exist_ok=True)
os.makedirs(COMPOSITE_OUTPUT_DIR, exist_ok=True)

def remove_background_simple(input_path, output_path):
    """Simple but effective background removal using color-based mask."""
    try:
        img = Image.open(input_path).convert('RGB')
        pixels = np.array(img)
        
        # Get image dimensions
        height, width, channels = pixels.shape
        
        # Convert to HSV-like color space for better separation
        # Calculate brightness
        brightness = np.mean(pixels, axis=2)
        
        # Detect light backgrounds (common in portraits)
        # Light areas typically have high values across all channels
        red, green, blue = pixels[:,:,0], pixels[:,:,1], pixels[:,:,2]
        
        # Background is typically uniform light color
        # Create mask for light/uniform areas
        bg_mask = (red > 200) & (green > 200) & (blue > 200)
        
        # Alternative: Check color uniformity (low saturation = likely background)
        max_val = np.maximum(np.maximum(red, green), blue)
        min_val = np.minimum(np.minimum(red, green), blue)
        saturation = np.where(max_val == 0, 0, (max_val - min_val) / max_val)
        
        # Combine: light OR low saturation
        bg_mask = bg_mask | (saturation < 0.1) & (brightness > 150)
        
        # If too much area is marked as background, invert
        if np.sum(bg_mask) > width * height * 0.6:
            bg_mask = ~bg_mask
        
        # Dilate edges slightly for cleaner boundaries
        from scipy.ndimage import binary_dilation
        bg_mask = binary_dilation(bg_mask, iterations=2)
        
        # Create smooth mask with gaussian blur
        mask_img = Image.fromarray((bg_mask * 255).astype(np.uint8))
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=5))
        
        # Invert to get foreground mask
        mask_array = 255 - np.array(mask_img)
        
        # Convert to RGBA
        result = Image.new('RGBA', img.size)
        result.paste(img, (0, 0))
        result.putalpha(Image.fromarray(mask_array, 'L'))
        
        result.save(output_path, 'PNG')
        return True
    except Exception as e:
        print(f"  Warning: {input_path} - {str(e)}, saving with fallback")
        # Fallback: save as-is with transparency
        try:
            img = Image.open(input_path).convert('RGBA')
            img.save(output_path, 'PNG')
            return True
        except:
            return False

def create_shadow_layer(width, height, shadow_blur=SHADOW_BLUR):
    """Create a shadow layer beneath a portrait."""
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
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
    return shadow

def resize_portrait_maintain_aspect(img, target_height=PERSON_HEIGHT):
    """Resize portrait maintaining aspect ratio."""
    ratio = target_height / img.height
    new_width = int(img.width * ratio)
    return img.resize((new_width, target_height), Image.Resampling.LANCZOS)

def add_shadow_to_portrait(portrait_path, output_path):
    """Add shadow beneath a portrait."""
    img = Image.open(portrait_path).convert('RGBA')
    
    # Resize to standard height
    img = resize_portrait_maintain_aspect(img, PERSON_HEIGHT)
    
    # Create shadow layer
    shadow = create_shadow_layer(img.width, img.height)
    
    # Composite: shadow + portrait
    result = Image.new('RGBA', img.size, (0, 0, 0, 0))
    result.paste(shadow, (0, 0), shadow)
    result.paste(img, (0, 0), img)
    
    result.save(output_path, 'PNG')
    return result

def create_group_composition(portrait_paths, output_path, bg_color=BRAND_COLOR):
    """Arrange multiple portraits into a group photo composition."""
    # Load all portraits and get their dimensions
    portraits = []
    total_width = 0
    max_height = 0
    
    for path in portrait_paths:
        if os.path.exists(path):
            img = Image.open(path).convert('RGBA')
            img = resize_portrait_maintain_aspect(img, PERSON_HEIGHT)
            portraits.append(img)
            total_width += img.width + SPACING
            max_height = max(max_height, img.height)
    
    if not portraits:
        print("No valid portraits found!")
        return
    
    # Calculate total dimensions
    total_width -= SPACING  # Remove last spacing
    total_width += SPACING * 2  # Add padding on sides
    total_height = max_height + SPACING * 2  # Add top and bottom padding
    
    # Create background
    background = Image.new('RGBA', (total_width, total_height), (*bg_color, 255))
    
    # Place portraits
    current_x = SPACING
    for portrait in portraits:
        y_pos = (total_height - portrait.height) // 2  # Center vertically
        background.paste(portrait, (current_x, y_pos), portrait)
        current_x += portrait.width + SPACING
    
    # Convert to RGB for better compatibility (keeping the background)
    # But keep as RGBA to preserve any transparency around edges
    background.save(output_path, 'PNG')
    print(f"Group composition saved to: {output_path}")

def main():
    print("Starting team photo processing...")
    
    # Process each image
    processed_portraits = []
    
    for filename in sorted(os.listdir(IMAGES_INPUT_DIR)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(IMAGES_INPUT_DIR, filename)
            output_path = os.path.join(IMAGES_OUTPUT_DIR, f"{Path(filename).stem}_transparent.png")
            
            print(f"Processing: {filename}...")
            
            # Step 1: Remove background
            if remove_background_simple(input_path, output_path):
                # Step 2: Add shadow
                shadow_path = os.path.join(IMAGES_OUTPUT_DIR, f"{Path(filename).stem}_with_shadow.png")
                add_shadow_to_portrait(output_path, shadow_path)
                processed_portraits.append(shadow_path)
                print(f"  ✓ Completed: {filename}")
            else:
                print(f"  ✗ Failed: {filename}")
    
    print(f"\nProcessed {len(processed_portraits)} portraits")
    
    # Step 3: Create group composition
    if processed_portraits:
        composition_path = os.path.join(COMPOSITE_OUTPUT_DIR, "team_group_photo.png")
        print(f"\nCreating group composition with {len(processed_portraits)} members...")
        create_group_composition(processed_portraits, composition_path, bg_color=BRAND_COLOR)
        print("✓ All processing complete!")
        print(f"\nOutput files:")
        print(f"  - Individual portraits: {IMAGES_OUTPUT_DIR}/")
        print(f"  - Group composition: {composition_path}")
    else:
        print("No portraits were successfully processed.")

if __name__ == "__main__":
    main()
