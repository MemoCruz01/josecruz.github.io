"""
Master conversion script - converts all PNG/JPG images to WebP in all project folders
"""

from PIL import Image
import os
import sys

def convert_images_in_folder(folder_path, recursive=True):
    """Convert all PNG and JPEG files in a folder to WebP format"""
    converted_count = 0
    error_count = 0
    
    print(f"\nProcessing folder: {folder_path}")
    
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, filename)
                    try:
                        img = Image.open(file_path).convert('RGB')
                        output_name = os.path.splitext(file_path)[0] + '.webp'
                        img.save(output_name, 'WEBP', quality=85)
                        print(f'✓ {os.path.relpath(file_path)}: {filename} -> {os.path.basename(output_name)}')
                        converted_count += 1
                    except Exception as e:
                        print(f'✗ Error converting {filename}: {e}')
                        error_count += 1
    else:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(folder_path, filename)
                try:
                    img = Image.open(file_path).convert('RGB')
                    output_name = os.path.splitext(file_path)[0] + '.webp'
                    img.save(output_name, 'WEBP', quality=85)
                    print(f'✓ {filename} -> {os.path.basename(output_name)}')
                    converted_count += 1
                except Exception as e:
                    print(f'✗ Error converting {filename}: {e}')
                    error_count += 1
    
    return converted_count, error_count

if __name__ == '__main__':
    project_base = r'D:\A EMINENT Master\10 Portfolio Applications\josecruz.github.io\projects'
    
    total_converted = 0
    total_errors = 0
    
    print("Starting image conversion to WebP...")
    print("=" * 60)
    
    # Convert images in all projects recursively
    converted, errors = convert_images_in_folder(project_base, recursive=True)
    total_converted += converted
    total_errors += errors
    
    print("\n" + "=" * 60)
    print(f"TOTAL - Successfully converted: {total_converted} file(s)")
    if total_errors > 0:
        print(f"TOTAL - Failed: {total_errors} file(s)")
    print("=" * 60)
