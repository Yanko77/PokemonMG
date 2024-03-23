import pygame


class Music:
    def __init__(self):#, game):
        #self.game = game
        self.music_list = ('assets/sounds/justeflute.wav',)

    def queue(self, music_name):
        pygame.mixer.music.queue(f'assets/sounds/{music_name}.wav')
        print(f'queue {music_name}')

    def load(self, music_name):
        pygame.mixer.music.load(f'assets/sounds/{music_name}.wav')
        print(f'load {music_name}')

    def play(self, loops=0):
        pygame.mixer.music.play(loops=loops, fade_ms=1000)
        print('joue')


def get_sound(sound_name:str):
    return pygame.mixer.Sound(f"assets/sounds/{sound_name}.wav")


def play_sound(sound_name, repetion=0, time=0, fadein=0, volume=1.0):
    a = get_sound(sound_name)
    a.set_volume(volume)
    a.play(repetion, time, fadein)
    return a


if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption("test")
    screen = pygame.display.set_mode((1280, 720))

    m = Music()
    m.load("pokemonmg_main_theme2")
    m.play()
    """m.queue("pokemonmg_main_theme2")"""

    # play_sound('pokemonmg_main_theme2', 1, volume=0.5)
    # 24030

    playing = True

    while playing:

        print(pygame.mixer.music.get_pos())
        if pygame.mixer.music.get_pos() == 24030:
            # play_sound('pokemonmg_main_theme2', 1, volume=0.5)
            pygame.mixer.music.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

    pygame.quit()
