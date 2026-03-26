"""
Convert specific MP4 videos to GIF with proper naming
"""

import os
from pathlib import Path

def convert_specific_videos_to_gif():
    """Convert specific MP4 files to GIF with new filenames"""
    try:
        import imageio
        import numpy as np
        from PIL import Image
    except ImportError:
        print('✗ Error: Required libraries not installed')
        return
    
    # Map of source MP4 to output GIF with proper naming
    conversions = [
        ('D:\\A EMINENT Master\\10 Portfolio Applications\\josecruz.github.io\\projects\\project-2-ev-assembly\\img\\RobotStudio 3-8.mp4', 
         'D:\\A EMINENT Master\\10 Portfolio Applications\\josecruz.github.io\\projects\\project-2-ev-assembly\\img\\RobotStudio-3-8.gif'),
        ('D:\\A EMINENT Master\\10 Portfolio Applications\\josecruz.github.io\\projects\\project-4-baja\\img\\BTBRacing video.mp4',
         'D:\\A EMINENT Master\\10 Portfolio Applications\\josecruz.github.io\\projects\\project-4-baja\\img\\BTBRacing-video.gif'),
        ('D:\\A EMINENT Master\\10 Portfolio Applications\\josecruz.github.io\\projects\\project-6-gesture-recognition\\img\\InShot201.mp4',
         'D:\\A EMINENT Master\\10 Portfolio Applications\\josecruz.github.io\\projects\\project-6-gesture-recognition\\img\\InShot201.gif'),
        ('D:\\A EMINENT Master\\10 Portfolio Applications\\josecruz.github.io\\projects\\Project-7-swarm-robotic-path-planning_n_exploration\\PSO_swarm_simulation.mp4',
         'D:\\A EMINENT Master\\10 Portfolio Applications\\josecruz.github.io\\projects\\Project-7-swarm-robotic-path-planning_n_exploration\\PSO_swarm_simulation.gif'),
    ]
    
    converted_count = 0
    error_count = 0
    
    print("Converting MP4 videos to GIF...")
    print("=" * 70)
    
    for mp4_path, gif_path in conversions:
        if os.path.exists(mp4_path):
            try:
                print(f'Converting: {os.path.basename(mp4_path)}...', end=' ', flush=True)
                
                reader = imageio.get_reader(mp4_path)
                meta = reader.get_meta_data()
                video_fps = meta.get('fps', 30)
                frame_interval = max(1, int(video_fps / 10))  # Target 10 fps for GIF
                
                frames_pil = []
                frame_count = 0
                max_frames = int(30 * 10)  # 30 seconds at 10fps = max 300 frames
                
                for i, frame in enumerate(reader):
                    if i % frame_interval == 0 and frame_count < max_frames:
                        try:
                            # Ensure frame is uint8
                            if frame.dtype != np.uint8:
                                if frame.dtype == np.float32 or frame.dtype == np.float64:
                                    frame = (frame * 255).astype(np.uint8) if frame.max() <= 1.0 else frame.astype(np.uint8)
                                else:
                                    frame = frame.astype(np.uint8)
                            
                            # Handle color spaces
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
                        gif_path,
                        save_all=True,
                        append_images=frames_pil[1:],
                        duration=100,  # 100ms per frame = 10fps
                        loop=0,
                        optimize=False
                    )
                    print(f'✓ -> {os.path.basename(gif_path)}')
                    converted_count += 1
                else:
                    print('✗ (no frames extracted)')
                    error_count += 1
                    
            except Exception as e:
                print(f'✗ Error: {str(e)[:50]}')
                error_count += 1
        else:
            print(f'✗ File not found: {mp4_path}')
            error_count += 1
    
    print("\n" + "=" * 70)
    print(f"Successfully converted: {converted_count} file(s)")
    if error_count > 0:
        print(f"Failed: {error_count} file(s)")
    print("=" * 70)

if __name__ == '__main__':
    convert_specific_videos_to_gif()
