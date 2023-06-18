import pygame

class AnimateImage:

    def __init__(self, nb_images, image_name):

        self.image = pygame.image.load('assets/accueil/animation/' + image_name + '/1.png')
        self.nb_images = nb_images
        self.current_image = 0  # Commencer à l'image 0
        self.images = animations.get(image_name)
        self.animation = False

        self.is_animation_over = False

        self.pas_rel = 0  # Pas relatif à animate()

    def start_animation(self):
        self.animation = True

    def animate(self, loop=False, final_image_num:int=0, pas:int=1):
        if self.animation:
            self.pas_rel += 1

            if self.pas_rel == pas:
                # Passer à l'image suivante
                self.current_image += 1

                if self.current_image >= len(self.images):  # Verifier si on a atteint la fin de l'animation
                    self.current_image = final_image_num

                    if not loop:  # Si l'animation n'est pas une boucle, on désactive
                        self.animation = False  # Désactiver l'animation
                        self.is_animation_over = True  # Indiquer la fin de l'animation

                # Actualiser l'image
                self.image = self.images[self.current_image]

                # Reinitialiser le pas
                self.pas_rel = 0

def load_animation_images(nb_images, image_name):
    # Charger les 24 images du sprite
    images = []
    path = f"assets/accueil/animation/{image_name}/"  # Chemin de l'image

    for num in range(1, nb_images+1):
        image_path = path + str(num) + '.png'
        images.append(pygame.image.load(image_path))

    return images

animations = {
        'Background': load_animation_images(24, 'Background'),
        'game_bar': load_animation_images(10, 'game_bar')
    }

if __name__ == "__main__":
    print(animations['Background'])

