import pygame
import numpy as np

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()
        
    def load_sounds(self):
        # Create simple placeholder sounds
        self.sounds['move'] = self._create_beep(220, 100)      # Lower pitch, short
        self.sounds['attack'] = self._create_beep(440, 200)    # Medium pitch, medium
        self.sounds['defeat'] = self._create_beep(110, 500)    # Low pitch, long
        self.sounds['select'] = self._create_beep(660, 50)     # High pitch, very short
        self.sounds['turn'] = self._create_beep(330, 150)      # Medium-low pitch
        self.sounds['victory'] = self._create_beep(880, 400)   # High pitch, long
        self.sounds['ability'] = self._create_beep(550, 300)   # Medium-high pitch
        self.sounds['item'] = self._create_beep(660, 200)      # High pitch, medium
    
    def _create_beep(self, frequency, duration):
        # Create a simple beep sound using pygame's built-in functionality
        sample_rate = 44100
        buffer = np.zeros((int(sample_rate * duration / 1000), 2), dtype=np.int16)
        max_sample = 2**(16 - 1) - 1

        for sample in range(len(buffer)):
            t = float(sample) / sample_rate
            value = int(max_sample * np.sin(2 * np.pi * frequency * t))
            buffer[sample][0] = value  # Left channel
            buffer[sample][1] = value  # Right channel

        sound = pygame.mixer.Sound(buffer=buffer)
        return sound
    
    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
