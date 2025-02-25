import pygame
import os
import requests
from io import BytesIO

API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
API_KEY_STATIC = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'


class Search:
    def __init__(self, *args, **kwargs):
        self.ll = '37.541425%2C55.749132'
        self.zoom = 10

    def get_map(self):
        if self.ll:
            map_request = f"https://static-maps.yandex.ru/v1?apikey={API_KEY_STATIC}&ll={self.ll}&z={self.zoom}"
        else:
            map_request = f"https://static-maps.yandex.ru/v1?apikey={API_KEY_STATIC}"
        # if add_params:
        #     map_request += "&" + add_params
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса")
            raise RuntimeError("HTTP: ", response.status_code)
        return response

    def draw_map(self):
        response = self.get_map()
        map_file = "map.png"
        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
        except FileNotFoundError:
            print("Ошибка записи в файл")
        return map_file


def main():
    map1 = Search()
    file = map1.draw_map()

    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    while pygame.event.wait().type != pygame.QUIT:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if map1.zoom < 21:
                        map1.zoom += 1
                if event.key == pygame.K_PAGEDOWN:
                    if map1.zoom > 0:
                        map1.zoom -= 1
        file = map1.draw_map()
        screen.blit(pygame.image.load(file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(file)


if __name__ == '__main__':
    main()
