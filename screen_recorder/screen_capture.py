from PIL import ImageGrab, Image
import numpy as np
import time
import threading
from typing import Optional, Tuple, List

class ScreenRecorder:
    def __init__(self, fps=30.0):
        """Initialize screen recorder.
        
        Args:
            fps: Frames per second for recording
        """
        self.fps = fps
        self.recording = False
        self.frames = []
        self.frame_interval = 1.0 / fps
        self.last_frame_time = 0
        self.selection_rect = None
        
    def capture_region(self, region: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
        """Capture a specific region of the screen or full screen.
        
        Args:
            region: Optional tuple of (left, top, right, bottom)
            
        Returns:
            PIL Image of the region or full screen
        """
        try:
            return ImageGrab.grab(bbox=region)
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None
        
    def start_recording(self, region=None):
        """Start recording screen.
        
        Args:
            region: Custom region to record (left, top, right, bottom)
        """
        if self.recording:
            return
            
        self.recording = True
        self.frames = []
        self.last_frame_time = 0
        self.selection_rect = region
        
        # Start recording thread
        self.record_thread = threading.Thread(target=self._record_frames)
        self.record_thread.daemon = True
        self.record_thread.start()
        
    def stop_recording(self) -> List[np.ndarray]:
        """Stop recording and return captured frames.
        
        Returns:
            List of frames as numpy arrays
        """
        self.recording = False
        if hasattr(self, 'record_thread'):
            self.record_thread.join()
        return self.frames
        
    def _record_frames(self):
        """Internal method to record frames."""
        while self.recording:
            current_time = time.time()
            
            # Maintain frame rate
            if current_time - self.last_frame_time < self.frame_interval:
                time.sleep(0.001)  # Small sleep to prevent CPU overuse
                continue
                
            try:
                # Capture frame
                frame = self.capture_region(self.selection_rect)
                
                if frame:
                    # Convert to numpy array and append
                    frame_array = np.array(frame)
                    self.frames.append(frame_array)
                    self.last_frame_time = current_time
                    
            except Exception as e:
                print(f"Error capturing frame: {e}")
                time.sleep(0.1)  # Prevent rapid error loops
