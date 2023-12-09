import os

import pygame as pg
import constants as c
import setup, tools
save_path = "./MarioPics"


class MarioSprites:
    def __init__(self):
        self.sprite_sheet = pg.image.load("mario_bros.png")
        self.right_frames = []
        self.left_frames = []
        self.load_images_from_sheet()

    def load_images_from_sheet(self):
        """Extracts Mario images from his sprite sheet and assigns
        them to appropriate lists"""
        self.right_frames = []
        self.left_frames = []

        self.right_small_normal_frames = []
        self.left_small_normal_frames = []
        self.right_small_green_frames = []
        self.left_small_green_frames = []
        self.right_small_red_frames = []
        self.left_small_red_frames = []
        self.right_small_black_frames = []
        self.left_small_black_frames = []

        self.right_big_normal_frames = []
        self.left_big_normal_frames = []
        self.right_big_green_frames = []
        self.left_big_green_frames = []
        self.right_big_red_frames = []
        self.left_big_red_frames = []
        self.right_big_black_frames = []
        self.left_big_black_frames = []

        self.right_fire_frames = []
        self.left_fire_frames = []

        # Images for normal small mario#

        self.right_small_normal_frames.append(
            self.get_image(178, 32, 12, 16))  # Right [0]
        self.right_small_normal_frames.append(
            self.get_image(80, 32, 15, 16))  # Right walking 1 [1]
        self.right_small_normal_frames.append(
            self.get_image(96, 32, 16, 16))  # Right walking 2 [2]
        self.right_small_normal_frames.append(
            self.get_image(112, 32, 16, 16))  # Right walking 3 [3]
        self.right_small_normal_frames.append(
            self.get_image(144, 32, 16, 16))  # Right jump [4]
        self.right_small_normal_frames.append(
            self.get_image(130, 32, 14, 16))  # Right skid [5]
        self.right_small_normal_frames.append(
            self.get_image(160, 32, 15, 16))  # Death frame [6]
        self.right_small_normal_frames.append(
            self.get_image(320, 8, 16, 24))  # Transition small to big [7]
        self.right_small_normal_frames.append(
            self.get_image(241, 33, 16, 16))  # Transition big to small [8]
        self.right_small_normal_frames.append(
            self.get_image(194, 32, 12, 16))  # Frame 1 of flag pole Slide [9]
        self.right_small_normal_frames.append(
            self.get_image(210, 33, 12, 16))  # Frame 2 of flag pole slide [10]

        # Images for small green mario (for invincible animation)#

        self.right_small_green_frames.append(
            self.get_image(178, 224, 12, 16))  # Right standing [0]
        self.right_small_green_frames.append(
            self.get_image(80, 224, 15, 16))  # Right walking 1 [1]
        self.right_small_green_frames.append(
            self.get_image(96, 224, 16, 16))  # Right walking 2 [2]
        self.right_small_green_frames.append(
            self.get_image(112, 224, 15, 16))  # Right walking 3 [3]
        self.right_small_green_frames.append(
            self.get_image(144, 224, 16, 16))  # Right jump [4]
        self.right_small_green_frames.append(
            self.get_image(130, 224, 14, 16))  # Right skid [5]

        # Images for red mario (for invincible animation)#

        self.right_small_red_frames.append(
            self.get_image(178, 272, 12, 16))  # Right standing [0]
        self.right_small_red_frames.append(
            self.get_image(80, 272, 15, 16))  # Right walking 1 [1]
        self.right_small_red_frames.append(
            self.get_image(96, 272, 16, 16))  # Right walking 2 [2]
        self.right_small_red_frames.append(
            self.get_image(112, 272, 15, 16))  # Right walking 3 [3]
        self.right_small_red_frames.append(
            self.get_image(144, 272, 16, 16))  # Right jump [4]
        self.right_small_red_frames.append(
            self.get_image(130, 272, 14, 16))  # Right skid [5]

        # Images for black mario (for invincible animation)#

        self.right_small_black_frames.append(
            self.get_image(178, 176, 12, 16))  # Right standing [0]
        self.right_small_black_frames.append(
            self.get_image(80, 176, 15, 16))  # Right walking 1 [1]
        self.right_small_black_frames.append(
            self.get_image(96, 176, 16, 16))  # Right walking 2 [2]
        self.right_small_black_frames.append(
            self.get_image(112, 176, 15, 16))  # Right walking 3 [3]
        self.right_small_black_frames.append(
            self.get_image(144, 176, 16, 16))  # Right jump [4]
        self.right_small_black_frames.append(
            self.get_image(130, 176, 14, 16))  # Right skid [5]

        # Images for normal big Mario

        self.right_big_normal_frames.append(
            self.get_image(176, 0, 16, 32))  # Right standing [0]
        self.right_big_normal_frames.append(
            self.get_image(81, 0, 16, 32))  # Right walking 1 [1]
        self.right_big_normal_frames.append(
            self.get_image(97, 0, 15, 32))  # Right walking 2 [2]
        self.right_big_normal_frames.append(
            self.get_image(113, 0, 15, 32))  # Right walking 3 [3]
        self.right_big_normal_frames.append(
            self.get_image(144, 0, 16, 32))  # Right jump [4]
        self.right_big_normal_frames.append(
            self.get_image(128, 0, 16, 32))  # Right skid [5]
        self.right_big_normal_frames.append(
            self.get_image(336, 0, 16, 32))  # Right throwing [6]
        self.right_big_normal_frames.append(
            self.get_image(160, 10, 16, 22))  # Right crouching [7]
        self.right_big_normal_frames.append(
            self.get_image(272, 2, 16, 29))  # Transition big to small [8]
        self.right_big_normal_frames.append(
            self.get_image(193, 2, 16, 30))  # Frame 1 of flag pole slide [9]
        self.right_big_normal_frames.append(
            self.get_image(209, 2, 16, 29))  # Frame 2 of flag pole slide [10]

        # Images for green big Mario#

        self.right_big_green_frames.append(
            self.get_image(176, 192, 16, 32))  # Right standing [0]
        self.right_big_green_frames.append(
            self.get_image(81, 192, 16, 32))  # Right walking 1 [1]
        self.right_big_green_frames.append(
            self.get_image(97, 192, 15, 32))  # Right walking 2 [2]
        self.right_big_green_frames.append(
            self.get_image(113, 192, 15, 32))  # Right walking 3 [3]
        self.right_big_green_frames.append(
            self.get_image(144, 192, 16, 32))  # Right jump [4]
        self.right_big_green_frames.append(
            self.get_image(128, 192, 16, 32))  # Right skid [5]
        self.right_big_green_frames.append(
            self.get_image(336, 192, 16, 32))  # Right throwing [6]
        self.right_big_green_frames.append(
            self.get_image(160, 202, 16, 22))  # Right Crouching [7]

        # Images for red big Mario#

        self.right_big_red_frames.append(
            self.get_image(176, 240, 16, 32))  # Right standing [0]
        self.right_big_red_frames.append(
            self.get_image(81, 240, 16, 32))  # Right walking 1 [1]
        self.right_big_red_frames.append(
            self.get_image(97, 240, 15, 32))  # Right walking 2 [2]
        self.right_big_red_frames.append(
            self.get_image(113, 240, 15, 32))  # Right walking 3 [3]
        self.right_big_red_frames.append(
            self.get_image(144, 240, 16, 32))  # Right jump [4]
        self.right_big_red_frames.append(
            self.get_image(128, 240, 16, 32))  # Right skid [5]
        self.right_big_red_frames.append(
            self.get_image(336, 240, 16, 32))  # Right throwing [6]
        self.right_big_red_frames.append(
            self.get_image(160, 250, 16, 22))  # Right crouching [7]

        # Images for black big Mario#

        self.right_big_black_frames.append(
            self.get_image(176, 144, 16, 32))  # Right standing [0]
        self.right_big_black_frames.append(
            self.get_image(81, 144, 16, 32))  # Right walking 1 [1]
        self.right_big_black_frames.append(
            self.get_image(97, 144, 15, 32))  # Right walking 2 [2]
        self.right_big_black_frames.append(
            self.get_image(113, 144, 15, 32))  # Right walking 3 [3]
        self.right_big_black_frames.append(
            self.get_image(144, 144, 16, 32))  # Right jump [4]
        self.right_big_black_frames.append(
            self.get_image(128, 144, 16, 32))  # Right skid [5]
        self.right_big_black_frames.append(
            self.get_image(336, 144, 16, 32))  # Right throwing [6]
        self.right_big_black_frames.append(
            self.get_image(160, 154, 16, 22))  # Right Crouching [7]

        # Images for Fire Mario#

        self.right_fire_frames.append(
            self.get_image(176, 48, 16, 32))  # Right standing [0]
        self.right_fire_frames.append(
            self.get_image(81, 48, 16, 32))  # Right walking 1 [1]
        self.right_fire_frames.append(
            self.get_image(97, 48, 15, 32))  # Right walking 2 [2]
        self.right_fire_frames.append(
            self.get_image(113, 48, 15, 32))  # Right walking 3 [3]
        self.right_fire_frames.append(
            self.get_image(144, 48, 16, 32))  # Right jump [4]
        self.right_fire_frames.append(
            self.get_image(128, 48, 16, 32))  # Right skid [5]
        self.right_fire_frames.append(
            self.get_image(336, 48, 16, 32))  # Right throwing [6]
        self.right_fire_frames.append(
            self.get_image(160, 58, 16, 22))  # Right crouching [7]
        self.right_fire_frames.append(
            self.get_image(0, 0, 0, 0))  # Place holder [8]
        self.right_fire_frames.append(
            self.get_image(193, 50, 16, 29))  # Frame 1 of flag pole slide [9]
        self.right_fire_frames.append(
            self.get_image(209, 50, 16, 29))  # Frame 2 of flag pole slide [10]

        # The left image frames are numbered the same as the right
        # frames but are simply reversed.

        for frame in self.right_small_normal_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_small_normal_frames.append(new_image)

        for frame in self.right_small_green_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_small_green_frames.append(new_image)

        for frame in self.right_small_red_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_small_red_frames.append(new_image)

        for frame in self.right_small_black_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_small_black_frames.append(new_image)

        for frame in self.right_big_normal_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_big_normal_frames.append(new_image)

        for frame in self.right_big_green_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_big_green_frames.append(new_image)

        for frame in self.right_big_red_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_big_red_frames.append(new_image)

        for frame in self.right_big_black_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_big_black_frames.append(new_image)

        for frame in self.right_fire_frames:
            new_image = pg.transform.flip(frame, True, False)
            self.left_fire_frames.append(new_image)

        self.normal_small_frames = [self.right_small_normal_frames,
                                    self.left_small_normal_frames]

        self.green_small_frames = [self.right_small_green_frames,
                                   self.left_small_green_frames]

        self.red_small_frames = [self.right_small_red_frames,
                                 self.left_small_red_frames]

        self.black_small_frames = [self.right_small_black_frames,
                                   self.left_small_black_frames]

        self.invincible_small_frames_list = [self.normal_small_frames,
                                             self.green_small_frames,
                                             self.red_small_frames,
                                             self.black_small_frames]

        self.normal_big_frames = [self.right_big_normal_frames,
                                  self.left_big_normal_frames]

        self.green_big_frames = [self.right_big_green_frames,
                                 self.left_big_green_frames]

        self.red_big_frames = [self.right_big_red_frames,
                               self.left_big_red_frames]

        self.black_big_frames = [self.right_big_black_frames,
                                 self.left_big_black_frames]

        self.fire_frames = [self.right_fire_frames,
                            self.left_fire_frames]

        self.invincible_big_frames_list = [self.normal_big_frames,
                                           self.green_big_frames,
                                           self.red_big_frames,
                                           self.black_big_frames]

        self.all_images = [self.right_big_normal_frames,
                           self.right_big_black_frames,
                           self.right_big_red_frames,
                           self.right_big_green_frames,
                           self.right_small_normal_frames,
                           self.right_small_green_frames,
                           self.right_small_red_frames,
                           self.right_small_black_frames,
                           self.left_big_normal_frames,
                           self.left_big_black_frames,
                           self.left_big_red_frames,
                           self.left_big_green_frames,
                           self.left_small_normal_frames,
                           self.left_small_red_frames,
                           self.left_small_green_frames,
                           self.left_small_black_frames]

        self.right_frames = self.normal_small_frames[0]
        self.left_frames = self.normal_small_frames[1]

    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet and saves it to a folder"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)
        image = pg.transform.scale(image,
                                   (int(rect.width * c.SIZE_MULTIPLIER),
                                    int(rect.height * c.SIZE_MULTIPLIER)))

        return image


def save_images(frames, folder, prefix):
    for i, frame in enumerate(frames):
        filename = f"{prefix}_{i}.png"
        pg.image.save(frame, f"{folder}/{filename}")


def main():
    mario_sprites = MarioSprites()

    # 保存所有图片
    save_images(mario_sprites.right_frames, "./mario/small_normal", "right_small_normal")
    save_images(mario_sprites.left_frames, "./mario/small_normal", "left_small_normal")

    save_images(mario_sprites.left_big_normal_frames, "./mario/big_normal", "left_big_normal")
    save_images(mario_sprites.right_big_normal_frames,"./mario/big_normal", "right_big_normal")

    save_images(mario_sprites.right_fire_frames, "./mario/big_fire", "right_big_fire")


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
