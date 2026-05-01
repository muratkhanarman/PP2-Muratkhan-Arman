import pygame
import sys
import datetime

pygame.init()

WIDTH, HEIGHT = 1100, 700
TOOLBAR_HEIGHT = 100
CANVAS_WIDTH = WIDTH
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont('Arial', 18)
small_font = pygame.font.SysFont('Arial', 14)

current_color = BLACK
brush_size = 2
tool = "pencil"
drawing = False
start_pos = None
last_pos = None
text_input = ""
text_pos = None
text_active = False

size_input = ""
size_box_active = False
SIZE_BOX_RECT = pygame.Rect(855, 10, 40, 30)

color_palette = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, (255, 165, 0), (255, 192, 203)]


def draw_toolbar():
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    tools = [
        ("pencil", 10, 10, "/"),
        ("line", 80, 10, "|"),
        ("rect", 150, 10, "□"),
        ("circle", 220, 10, "○"),
        ("square", 290, 10, "■"),
        ("triangle", 360, 10, "▲"),
        ("rhombus", 430, 10, "◆"),
        ("fill", 500, 10, "[]"),
        ("text", 570, 10, "T"),
    ]

    for name, x, y, icon in tools:
        color = YELLOW if tool == name else GRAY
        pygame.draw.rect(screen, color, (x, y, 60, 40))
        pygame.draw.rect(screen, BLACK, (x, y, 60, 40), 1)
        screen.blit(font.render(icon, True, BLACK), (x + 20, y + 10))
        screen.blit(small_font.render(name, True, BLACK), (x + 5, y + 25))

    sizes = [(2, 650, 10), (5, 720, 10), (10, 790, 10)]
    for sz, x, y in sizes:
        color = YELLOW if brush_size == sz else GRAY
        pygame.draw.rect(screen, color, (x, y, 45, 40))
        pygame.draw.rect(screen, BLACK, (x, y, 45, 40), 1)
        screen.blit(font.render(str(sz), True, BLACK), (x + 12, y + 10))
        pygame.draw.circle(screen, BLACK, (x + 22, y + 32), min(sz // 2, 6))

    for i, color in enumerate(color_palette):
        x = 10 + i * 35
        y = 60
        if current_color == color:
            pygame.draw.rect(screen, YELLOW, (x - 2, y - 2, 34, 34))
        pygame.draw.rect(screen, color, (x, y, 30, 30))
        pygame.draw.rect(screen, BLACK, (x, y, 30, 30), 1)

    box_color = WHITE if size_box_active else LIGHT_GRAY
    pygame.draw.rect(screen, box_color, SIZE_BOX_RECT)
    pygame.draw.rect(screen, BLACK, SIZE_BOX_RECT, 2 if size_box_active else 1)
    display_text = size_input if size_box_active else str(brush_size)
    screen.blit(small_font.render(display_text, True, BLACK), (SIZE_BOX_RECT.x + 4, SIZE_BOX_RECT.y + 8))
    screen.blit(small_font.render("px", True, BLACK), (SIZE_BOX_RECT.x + SIZE_BOX_RECT.width + 2, SIZE_BOX_RECT.y + 8))

    screen.blit(small_font.render("Ctrl+S: Save", True, BLACK), (10, TOOLBAR_HEIGHT - 18))


def draw_shape(surface, color, start, end, shape, thickness):
    x1, y1 = start
    x2, y2 = end

    if shape == "rect":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(surface, color, rect, thickness)

    elif shape == "circle":
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        radius = max(abs(x2 - x1), abs(y2 - y1)) // 2
        pygame.draw.circle(surface, color, center, radius, thickness)

    elif shape == "square":
        side = max(abs(x2 - x1), abs(y2 - y1))
        sx = x1
        sy = y1
        ex = sx + (side if x2 >= x1 else -side)
        ey = sy + (side if y2 >= y1 else -side)
        rect = pygame.Rect(min(sx, ex), min(sy, ey), side, side)
        pygame.draw.rect(surface, color, rect, thickness)

    elif shape == "triangle":
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        cx = (x1 + x2) // 2
        top_y = min(y1, y2)
        bot_y = max(y1, y2)
        points = [
            (cx, top_y),
            (cx - w // 2, bot_y),
            (cx + w // 2, bot_y),
        ]
        pygame.draw.polygon(surface, color, points, thickness)

    elif shape == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        dx = abs(x2 - x1) // 2
        dy = abs(y2 - y1) // 2
        points = [(cx, cy - dy), (cx + dx, cy), (cx, cy + dy), (cx - dx, cy)]
        pygame.draw.polygon(surface, color, points, thickness)

    elif shape == "line":
        pygame.draw.line(surface, color, start, end, thickness)


def flood_fill(surface, pos, target_color, replacement_color):
    target_color = target_color[:3]
    replacement_color = replacement_color[:3]
    if target_color == replacement_color:
        return

    width, height = surface.get_size()
    if not (0 <= pos[0] < width and 0 <= pos[1] < height):
        return
    if surface.get_at(pos)[:3] != target_color:
        return

    stack = [pos]
    visited = set()
    visited.add(pos)

    while stack:
        x, y = stack.pop()
        surface.set_at((x, y), replacement_color)
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                if surface.get_at((nx, ny))[:3] == target_color:
                    visited.add((nx, ny))
                    stack.append((nx, ny))


def save_canvas():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{timestamp}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")
    big_font = pygame.font.SysFont('Arial', 30)
    msg = big_font.render(f"Saved: {filename}", True, GREEN)
    screen.blit(msg, (WIDTH // 2 - 150, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(1000)


running = True

while running:
    draw_toolbar()
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    if drawing and start_pos and tool in ("line", "rect", "circle", "square", "triangle", "rhombus"):
        mx, my = pygame.mouse.get_pos()
        end_canvas = (mx, my - TOOLBAR_HEIGHT)
        preview = canvas.copy()
        draw_shape(preview, current_color, start_pos, end_canvas, tool, brush_size)
        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    if text_active and text_pos:
        text_surface = font.render(text_input + "|", True, current_color)
        screen.blit(text_surface, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if size_box_active:
                if event.key == pygame.K_RETURN:
                    try:
                        val = int(size_input)
                        if 1 <= val <= 100:
                            brush_size = val
                    except ValueError:
                        pass
                    size_input = ""
                    size_box_active = False
                elif event.key == pygame.K_ESCAPE:
                    size_input = ""
                    size_box_active = False
                elif event.key == pygame.K_BACKSPACE:
                    size_input = size_input[:-1]
                elif event.unicode.isdigit() and len(size_input) < 3:
                    size_input += event.unicode

            elif text_active:
                if event.key == pygame.K_RETURN:
                    if text_pos and text_input:
                        canvas.blit(font.render(text_input, True, current_color), text_pos)
                    text_active = False
                    text_input = ""
                    text_pos = None
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_input = ""
                    text_pos = None
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif event.unicode.isprintable():
                    text_input += event.unicode

            else:
                if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_s:
                    save_canvas()
                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if SIZE_BOX_RECT.collidepoint(mx, my):
                size_box_active = True
                size_input = ""
                continue

            if size_box_active:
                size_box_active = False
                size_input = ""

            if my < TOOLBAR_HEIGHT:
                tool_clicks = [
                    ("pencil", 10, 70),
                    ("line", 80, 140),
                    ("rect", 150, 210),
                    ("circle", 220, 280),
                    ("square", 290, 350),
                    ("triangle", 360, 420),
                    ("rhombus", 430, 490),
                    ("fill", 500, 560),
                    ("text", 570, 630),
                ]
                for name, x_start, x_end in tool_clicks:
                    if x_start <= mx <= x_end and 10 <= my <= 50:
                        tool = name
                        break

                if 650 <= mx <= 695 and 10 <= my <= 50:
                    brush_size = 2
                elif 720 <= mx <= 765 and 10 <= my <= 50:
                    brush_size = 5
                elif 790 <= mx <= 835 and 10 <= my <= 50:
                    brush_size = 10

                for i, color in enumerate(color_palette):
                    cx = 10 + i * 35
                    cy = 60
                    if cx <= mx <= cx + 30 and cy <= my <= cy + 30:
                        current_color = color
                continue

            canvas_x = mx
            canvas_y = my - TOOLBAR_HEIGHT

            if canvas_y < 0 or canvas_y >= CANVAS_HEIGHT:
                continue

            canvas_pos = (canvas_x, canvas_y)

            if tool == "pencil":
                drawing = True
                last_pos = canvas_pos
                pygame.draw.circle(canvas, current_color, canvas_pos, brush_size // 2)

            elif tool in ("line", "rect", "circle", "square", "triangle", "rhombus"):
                drawing = True
                start_pos = canvas_pos

            elif tool == "fill":
                try:
                    target = canvas.get_at(canvas_pos)
                    flood_fill(canvas, canvas_pos, target, current_color)
                except Exception as e:
                    print(f"Fill error: {e}")

            elif tool == "text":
                text_active = True
                text_pos = canvas_pos
                text_input = ""

        elif event.type == pygame.MOUSEBUTTONUP:
            if tool in ("line", "rect", "circle", "square", "triangle", "rhombus") and drawing and start_pos:
                mx, my = pygame.mouse.get_pos()
                end_canvas = (mx, my - TOOLBAR_HEIGHT)
                draw_shape(canvas, current_color, start_pos, end_canvas, tool, brush_size)
                drawing = False
                start_pos = None

            elif tool == "pencil":
                drawing = False
                last_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if drawing and tool == "pencil" and last_pos:
                mx, my = pygame.mouse.get_pos()
                cx = max(0, min(mx, CANVAS_WIDTH - 1))
                cy = max(0, min(my - TOOLBAR_HEIGHT, CANVAS_HEIGHT - 1))
                new_pos = (cx, cy)
                pygame.draw.line(canvas, current_color, last_pos, new_pos, brush_size)
                last_pos = new_pos

    clock.tick(60)

pygame.quit()
sys.exit()