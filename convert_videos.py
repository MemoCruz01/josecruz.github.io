"""
Master Video to GIF Converter - converts all MP4 videos in all project folders
"""

import os
import numpy as np

def convert_video_to_gif_batch(base_folder, fps=10, duration=30):
    """Convert all video files in all subfolders to GIF"""
    try:
        import imageio
        from PIL import Image
    except ImportError:
        print('✗ Error: Required libraries not installed')
        print('Install with: pip install imageio imageio-ffmpeg pillow')
        return 0, 0
    
    supported_formats = ('.mp4', '.avi', '.mov', '.webm', '.mkv')
    converted_count = 0
    error_count = 0
    
    print("Starting video to GIF conversion...")
    print("=" * 60)
    
    for root, dirs, files in os.walk(base_folder):
        for filename in files:
            if filename.lower().endswith(supported_formats):
                file_path = os.path.join(root, filename)
                try:
                    output_name = os.path.splitext(file_path)[0] + '.gif'
                    rel_path = os.path.relpath(file_path, base_folder)
                    print(f'Converting: {rel_path}...', end=' ', flush=True)
                    
                    reader = imageio.get_reader(file_path)
                    meta = reader.get_meta_data()
                    video_fps = meta.get('fps', 30)
                    frame_interval = max(1, int(video_fps / fps))
                    
                    frames_pil = []
                    frame_count = 0
                    max_frames = int(duration * fps)
                    
                    for i, frame in enumerate(reader):
                        if i % frame_interval == 0 and frame_count < max_frames:
                            try:
                                # Ensure frame is uint8
                                if frame.dtype != np.uint8:
                                    if frame.dtype == np.float32 or frame.dtype == np.float64:
                                        frame = (frame * 255).astype(np.uint8) if frame.max() <= 1.0 else frame.astype(np.uint8)
                                    else:
                                        frame = frame.astype(np.uint8)
                                
                                # Handle different color spaces
                                if len(frame.shape) == 3:
                                    if frame.shape[2] == 4:  # RGBA
                                        img_pil = Image.fromarray(frame, 'RGBA')
                                    elif frame.shape[2] == 3:  # RGB
                                        img_pil = Image.fromarray(frame, 'RGB')
                                    else:
                                        continue
                                else:
                                    img_pil = Image.fromarray(frame, 'L')
                                
                                frames_pil.append(img_pil)
                                frame_count += 1
                            except Exception as e:
                                continue
                    
                    if frames_pil:
                        frames_pil[0].save(
                            output_name,
                            save_all=True,
                            append_images=frames_pil[1:],
                            duration=int(1000 / fps),
                            loop=0,
                            optimize=False
                        )
                        print(f'✓ -> {os.path.basename(output_name)}')
                        converted_count += 1
                    else:
                        print('✗ (no frames)')
                        error_count += 1
                        
                except Exception as e:
                    print(f'✗ Error: {e}')
                    error_count += 1
    
    return converted_count, error_count

if __name__ == '__main__':
    project_base = r'D:\A EMINENT Master\10 Portfolio Applications\josecruz.github.io\projects'
    
    converted, errors = convert_video_to_gif_batch(project_base, fps=10, duration=30)
    
    print("\n" + "=" * 60)
    print(f"Successfully converted: {converted} file(s)")
    if errors > 0:
        print(f"Failed: {errors} file(s)")
    print("=" * 60)
