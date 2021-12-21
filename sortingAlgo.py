import pygame
import random

pygame.init()

class DrawInformation():
    BLACK = 0, 0, 0
    WHITE = 193, 232, 227
    GREEN = 0, 255, 0
    RED = 255, 0, 0

    FONT = pygame.font.SysFont('Corbel', 20)
    LARGE_FONT = pygame.font.SysFont('Corbel', 40)

    SIDE_PAD = 100
    TOP_PAD = 150
    GRADIENTS = [
        (75, 75, 75),
        (100, 100, 100),
        (150, 150, 150),
        (200, 200, 200),
        (225, 225, 225)
    ]

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width-self.SIDE_PAD))/len(lst)
        self.block_height = round((self.height - self.TOP_PAD))/(self.max_val)
        self.start_x = self.SIDE_PAD//2


def generate_lst(n, min_val, max_val):
    lst = random.sample(range(min_val, max_val), n)
    # for _ in range(n):
    #     val = random.randint(min_val, max_val)
    #     lst.append(val)

    return lst


def draw(draw_info, algo, ascending):
    draw_info.window.fill(draw_info.WHITE)

    title = draw_info.FONT.render(f"{algo} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 20))

    controls = draw_info.FONT.render("R - Reset || Space - Sorting || A - Ascending || D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2,45))

    sorting = draw_info.FONT.render("I - Insertion || B - Bubble || H - Heap || S - Shell", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 65))

    draw_lst(draw_info)
    pygame.display.update()


def draw_lst(draw_info, color_pos={}, clear_bg=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.WHITE, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        color = draw_info.GRADIENTS[i%5]

        if i in color_pos:
            color = color_pos[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


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
            draw_lst(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst


def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_lst(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True

    return True


def heapifymin(arr, n, i):
    smallest = i  # Initialize smalles as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2
    if l < n and arr[l] < arr[smallest]:
        smallest = l

    if r < n and arr[r] < arr[smallest]:
        smallest = r
    if smallest != i:
        (arr[i], arr[smallest]) = (arr[smallest], arr[i])
        heapifymin(arr, n, smallest)


def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2
    if l < n and arr[largest] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def shellSort(draw_info, ascending = True):
    arr = draw_info.lst
    n = len(arr)
    gap = int(n / 2)
    if ascending:
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                draw_lst(draw_info, {temp: draw_info.RED, arr[j]: draw_info.GREEN}, True)
                while j >= gap and arr[j - gap] > temp:
                    draw_lst(draw_info, {arr[j-gap]: draw_info.RED, arr[i]: draw_info.GREEN}, True)
                    arr[j] = arr[j - gap]
                    j -= gap
                    yield True
                arr[j] = temp
                draw_lst(draw_info, {arr[j]: draw_info.GREEN}, True)

            gap = int(gap/2)
            draw_lst(draw_info, {gap: draw_info.RED}, True)
    else:
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                draw_lst(draw_info, {temp: draw_info.RED, arr[j]: draw_info.GREEN}, True)
                while j >= gap and arr[j - gap] < temp:
                    draw_lst(draw_info, {arr[j - gap]: draw_info.RED, arr[i]: draw_info.GREEN}, True)
                    arr[j] = arr[j - gap]
                    j -= gap
                    yield True
                arr[j] = temp
                draw_lst(draw_info, {arr[j]: draw_info.GREEN}, True)

            gap = int(gap / 2)
            draw_lst(draw_info, {gap: draw_info.RED}, True)


def heapSort(draw_info, ascending=True):
    n = len(draw_info.lst)
    arr = draw_info.lst
    if ascending:
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)

        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]  # swap
            draw_lst(draw_info, {0: draw_info.RED, i: draw_info.GREEN}, True)
            heapify(arr, i, 0)
            yield True
    else:
        for i in range(n // 2 - 1, -1, -1):
            heapifymin(arr, n, i)

        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]  # swap
            draw_lst(draw_info, {0: draw_info.RED, i: draw_info.GREEN}, True)
            heapifymin(arr, i, 0)
            yield True


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 300
    lst = generate_lst(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    ascending = True
    sorting = False
    sorting_algorithm = heapSort
    sorting_algorithm_name = "Heap Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)
        pygame.display.update()
        draw(draw_info, sorting_algorithm_name, ascending)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                new_lst = generate_lst(n, min_val, max_val)
                draw_info.set_list(new_lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heapSort
                sorting_algorithm_name = "Heap Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = shellSort
                sorting_algorithm_name = "Shell Sort"


    pygame.quit()

if __name__ == "__main__":
    main()
