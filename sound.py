import pygame


def get_sound(sound_name:str):
    return pygame.mixer.Sound(f"assets/sounds/{sound_name}.wav")

def play_sound(sound, repetion=0,time=0, fadein=0,volume=1.0):
    a = get_sound(sound_name)
    a.set_volume(volume)
    a.play(repetion,time,fadein)
    
if __name__ == '__main__':
    pygame.init()
    
    play_sound('bip',0,1000)
