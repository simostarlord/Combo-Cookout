import pygame
import os
import sys
import asyncio

async def main():
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cooking Game")

    # Font
    font = pygame.font.SysFont(None, 36)

    # Load images (place your PNGs in the assets/ folder)
    ASSETS = "assets"

    INGREDIENTS = [
        "Egg", "Onion", "Carrot", "Apple", "Beef", "Chicken",
        "Cheese", "Banana", "Capsicum", "Bread", "Milk"
    ]

    # Load ingredient images
    ingredient_imgs = {name: pygame.image.load(os.path.join(ASSETS, f"{name.lower()}.png")) for name in INGREDIENTS}

    # Load dish images
    dish_imgs = {
        "Omelette": pygame.image.load(os.path.join(ASSETS, "omelette.png")),
        "Stew": pygame.image.load(os.path.join(ASSETS, "stew.png")),
        "Pie": pygame.image.load(os.path.join(ASSETS, "pie.png")),
        "Smoothie": pygame.image.load(os.path.join(ASSETS, "smoothie.png")),
        "Sandwich": pygame.image.load(os.path.join(ASSETS, "sandwich.png")),
        "Cupcake": pygame.image.load(os.path.join(ASSETS, "cupcake.png")),
        "Salad": pygame.image.load(os.path.join(ASSETS, "salad.png")),
    }

    # Recipe mapping
    def create_bidirectional_recipes(raw):
        r = {}
        for (a, b), result in raw.items():
            r[(a, b)] = result
            r[(b, a)] = result
        return r

    raw_recipes = {
        ("Egg", "Carrot"): "Omelette", ("Egg", "Apple"): "Pie", ("Egg", "Beef"): "Stew", ("Egg", "Chicken"): "Stew", ("Egg", "Cheese"): "Omelette", ("Egg", "Banana"): "Cupcake", ("Egg", "Capsicum"): "Omelette", ("Egg", "Bread"): "Sandwich", ("Egg", "Milk"): "Omelette",
        ("Onion", "Carrot"): "Stew", ("Onion", "Apple"): "Salad", ("Onion", "Beef"): "Stew", ("Onion", "Chicken"): "Stew", ("Onion", "Cheese"): "Sandwich", ("Onion", "Banana"): "Cupcake", ("Onion", "Capsicum"): "Stew", ("Onion", "Bread"): "Sandwich", ("Onion", "Milk"): "Stew",
        ("Carrot", "Apple"): "Smoothie", ("Carrot", "Beef"): "Stew", ("Carrot", "Chicken"): "Stew", ("Carrot", "Cheese"): "Salad", ("Carrot", "Banana"): "Cupcake", ("Carrot", "Capsicum"): "Omelette", ("Carrot", "Bread"): "Sandwich", ("Carrot", "Milk"): "Smoothie",
        ("Apple", "Beef"): "Stew", ("Apple", "Chicken"): "Stew", ("Apple", "Cheese"): "Pie", ("Apple", "Banana"): "Smoothie", ("Apple", "Capsicum"): "Salad", ("Apple", "Bread"): "Pie", ("Apple", "Milk"): "Smoothie",
        ("Beef", "Chicken"): "Stew", ("Beef", "Cheese"): "Stew", ("Beef", "Banana"): "Stew", ("Beef", "Capsicum"): "Stew", ("Beef", "Bread"): "Sandwich", ("Beef", "Milk"): "Stew",
        ("Chicken", "Cheese"): "Sandwich", ("Chicken", "Banana"): "Cupcake", ("Chicken", "Capsicum"): "Stew", ("Chicken", "Bread"): "Sandwich", ("Chicken", "Milk"): "Stew",
        ("Cheese", "Banana"): "Cupcake", ("Cheese", "Capsicum"): "Sandwich", ("Cheese", "Bread"): "Sandwich", ("Cheese", "Milk"): "Cupcake",
        ("Banana", "Capsicum"): "Cupcake", ("Banana", "Bread"): "Pie", ("Banana", "Milk"): "Smoothie",
        ("Capsicum", "Bread"): "Sandwich", ("Capsicum", "Milk"): "Stew",
        ("Bread", "Milk"): "Pie",("Egg", "Onion"): "Omelette"

    }

    recipes = create_bidirectional_recipes(raw_recipes)

    # State
    selected = []
    dish_result = None

    # Button positions
    button_rects = {}
    x, y = 50, 50
    for i, name in enumerate(INGREDIENTS):
        rect = pygame.Rect(x, y, 120, 120)
        button_rects[name] = rect
        x += 140
        if (i + 1) % 5 == 0:
            x = 50
            y += 140

    def draw():
        screen.fill((255, 245, 230))  # Lighter kitchen color

        # Draw ingredient buttons
        for name, rect in button_rects.items():
            screen.blit(pygame.transform.scale(ingredient_imgs[name], (120, 120)), rect.topleft)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        # Show result dish in center, slightly lower
        if dish_result:
            dish_img = dish_imgs[dish_result] if dish_result in dish_imgs else None
            if dish_img:
                dish_big = pygame.transform.scale(dish_img, (200, 200))
                screen.blit(dish_big, (WIDTH // 2 - 100, HEIGHT // 2))
            label = font.render(dish_result, True, (0, 0, 0))
            screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 + 220))

        # Show selected ingredients
        if selected:
            text = font.render(" + ".join(selected), True, (0, 0, 0))
            screen.blit(text, (50, HEIGHT - 50))

        pygame.display.flip()

    # Game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for name, rect in button_rects.items():
                    if rect.collidepoint(pos):
                        if name in selected:
                            continue
                        selected.append(name)
                        if len(selected) == 2:
                            if selected[0] == selected[1]:
                                dish_result = None
                            else:
                                dish_result = recipes.get(tuple(selected), "Unknown")
                            pygame.time.set_timer(pygame.USEREVENT, 1500)

            elif event.type == pygame.USEREVENT:
                selected = []
                dish_result = None
                pygame.time.set_timer(pygame.USEREVENT, 0)

        await asyncio.sleep(0)  # very important for WebAssembly
        clock.tick(60)


    pygame.quit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
