import pygame
import random
import math

pygame.init()


class DrawInfo:
    BLACK = (23, 23, 23)
    WHITE = (255, 255, 255)
    GREEN = (0, 202, 78)
    RED = (255, 96, 92)
    GREY = (192, 192, 192)
    LIGHT_GREY = (255, 250, 250)
    DARK_GREY = (123, 123, 123)
    BACKGROUND_COLOUR = LIGHT_GREY
    TITLE_COLOUR = BLACK

    FONT = pygame.font.SysFont('Arial', 20)
    LARGE_FONT = pygame.font.SysFont('Arial', 36)

    SIDE_PAD = 100
    TOP_PAD = 130

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualiser")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_space = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst)) * 0.9
        self.block_height = math.floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOUR)

    title = draw_info.LARGE_FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}",
        1,
        draw_info.TITLE_COLOUR
    )
    draw_info.window.blit(
        title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render(
        "R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending",
        1,
        draw_info.BLACK
    )
    draw_info.window.blit(
        controls, (draw_info.width / 2 - controls.get_width() / 2, 50))

    sorting = draw_info.FONT.render(
        "I - Insertion | B - Bubble | S - Selection", 1, draw_info.BLACK)
    draw_info.window.blit(
        sorting, (draw_info.width / 2 - sorting.get_width() / 2, 80))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, colour_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height - draw_info.TOP_PAD)

        pygame.draw.rect(draw_info.window,
                         draw_info.BACKGROUND_COLOUR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_space
        y = draw_info.height - (val - draw_info.min_val) *  \
            draw_info.block_height

        colour = draw_info.DARK_GREY

        if i in colour_positions:
            colour = colour_positions[i]

        pygame.draw.rect(draw_info.window, colour,
                         (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(
                    draw_info,
                    {j: draw_info.GREEN, j + 1: draw_info.RED},
                    True
                )
                yield True

    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN,
                      i: draw_info.RED}, True)
            yield True

    return lst


def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    if ascending:
        for i in range(len(lst)):
            min_idx = i
            for j in range(i + 1, len(lst)):
                draw_list(draw_info, {min_idx: draw_info.GREEN,
                          j: draw_info.RED}, True)
                if lst[min_idx] > lst[j]:
                    draw_list(draw_info, {min_idx: draw_info.GREEN,
                              j: draw_info.RED}, True)
                    min_idx = j

            lst[i], lst[min_idx] = lst[min_idx], lst[i]

            yield True
    else:
        for i in range(len(lst)):
            max_idx = i
            for j in range(i + 1, len(lst)):
                draw_list(draw_info, {max_idx: draw_info.GREEN,
                          j: draw_info.RED}, True)
                if lst[max_idx] < lst[j]:
                    draw_list(draw_info, {max_idx: draw_info.GREEN,
                              j: draw_info.RED}, True)
                    max_idx = j

            lst[i], lst[max_idx] = lst[max_idx], lst[i]

            yield True

    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 100
    min_val = 5
    max_val = 100

    lst = generate_list(n, min_val, max_val)
    draw_info = DrawInfo(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    while run:
        clock.tick(800)

        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algo_generator = sorting_algorithm(
                    draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
