"""
Video to GIF Converter (Enhanced)
Converts all video files to animated GIF format with proper color space handling
"""

import os
import numpy as np

def convert_video_to_gif(fps=10, duration=30):
    """Convert all video files to GIF with robust color handling"""
    try:
        import imageio
        from PIL import Image
    except ImportError:
        print('✗ Error: Required libraries not installed')
        print('Install with: pip install imageio imageio-ffmpeg pillow')
        return
    
    supported_formats = ('.mp4', '.avi', '.mov', '.webm', '.mkv')
    converted_count = 0
    error_count = 0
    
    for filename in os.listdir('.'):
        if filename.lower().endswith(supported_formats):
            try:
                output_name = filename.rsplit('.', 1)[0] + '.gif'
                print(f'Converting: {filename}...', end=' ', flush=True)
                
                reader = imageio.get_reader(filename)
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
                                    # Normalize float to 0-255
                                    frame = (frame * 255).astype(np.uint8) if frame.max() <= 1.0 else frame.astype(np.uint8)
                                else:
                                    frame = frame.astype(np.uint8)
                            
                            # Handle different color spaces
                            if len(frame.shape) == 3:
                                if frame.shape[2] == 4:  # RGBA
                                    frame = frame[:, :, :3]
                                elif frame.shape[2] != 3:  # Not RGB/BGR
                                    # Use imageio to convert
                                    continue
                            elif len(frame.shape) == 2:  # Grayscale
                                frame = np.stack([frame] * 3, axis=2)
                            
                            # Convert to PIL Image and ensure RGB
                            pil_img = Image.fromarray(frame, mode='RGB')
                            frames_pil.append(pil_img)
                            frame_count += 1
                            
                        except Exception as e:
                            continue
                
                if frames_pil and len(frames_pil) > 1:
                    # Save GIF
                    frames_pil[0].save(
                        output_name,
                        save_all=True,
                        append_images=frames_pil[1:],
                        duration=int(1000/fps),
                        loop=0,
                        optimize=False
                    )
                    print(f'✓ ({frame_count} frames)')
                    converted_count += 1
                else:
                    print(f'✗ (no frames)')
                    error_count += 1
                    
            except Exception as e:
                print(f'✗ Error: {str(e)[:50]}')
                error_count += 1
    
    print(f'\n--- Summary ---')
    print(f'Converted: {converted_count} file(s)')
    if error_count > 0:
        print(f'Failed: {error_count} file(s)')

if __name__ == '__main__':
    convert_video_to_gif(fps=15, duration=30)


