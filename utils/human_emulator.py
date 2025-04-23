import random
import asyncio
from playwright.async_api import Page

async def emulate_human_delay(min_ms=300, max_ms=1500):
    await asyncio.sleep(random.uniform(min_ms / 1000, max_ms / 1000))

async def type_like_human(page: Page, selector: str, text: str):
    await page.click(selector)
    for char in text:
        await page.keyboard.type(char, delay=random.randint(40, 150))
    await emulate_human_delay()

async def emulate_mouse_move(page: Page):
    box = await page.locator("textarea").bounding_box()
    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2
    await page.mouse.move(x + random.randint(-10, 10), y + random.randint(-10, 10), steps=random.randint(5, 15))