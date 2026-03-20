"""
Image to WebP Converter
Converts all PNG and JPEG images in the current directory to WebP format with quality 85
Usage: python png-to-webp-converter.py
"""

from PIL import Image
import os

def convert_png_to_webp(quality=85):
    """Convert all PNG and JPEG files in current directory to WebP format"""
    converted_count = 0
    error_count = 0
    
    for filename in os.listdir('.'):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(filename).convert('RGB')
                output_name = filename.rsplit('.', 1)[0] + '.webp'
                img.save(output_name, 'WEBP', quality=quality)
                print(f'✓ Converted: {filename} -> {output_name}')
                converted_count += 1
            except Exception as e:
                print(f'✗ Error converting {filename}: {e}')
                error_count += 1
    
    # Summary
    print(f'\n--- Summary ---')
    print(f'Successfully converted: {converted_count} file(s)')
    if error_count > 0:
        print(f'Failed: {error_count} file(s)')

if __name__ == '__main__':
    convert_png_to_webp()
