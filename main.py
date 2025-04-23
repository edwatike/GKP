import asyncio
from automation.grok_actions import GrokDriver
from utils.human_emulator import emulate_human_delay
import os
import sys
from playwright.async_api import async_playwright
from browser_manager import BrowserManager
import random

PROMPT_FILE = "prompt_queue.txt"
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

async def run_bot(prompt):
    browser_manager = BrowserManager()
    
    for attempt in range(MAX_RETRIES):
        try:
            profile_dir = browser_manager.prepare_profile(use_random=False)
            async with async_playwright() as p:
                # Запускаем браузер с улучшенными параметрами для обхода защиты
                browser = await p.chromium.launch_persistent_context(
                    user_data_dir=profile_dir,
                    headless=False,
                    args=browser_manager.get_stealth_args()
                )
                try:
                    # Создаем новую страницу
                    page = await browser.new_page()
                    
                    # Устанавливаем случайные размеры viewport
                    await page.set_viewport_size({
                        "width": random.randint(1050, 1200),
                        "height": random.randint(800, 900)
                    })
                    
                    # Эмулируем случайный User-Agent
                    await page.set_extra_http_headers({
                        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500, 600)}.{random.randint(1, 99)} (KHTML, like Gecko) Chrome/{random.randint(90, 120)}.0.0.0 Safari/{random.randint(500, 600)}.{random.randint(1, 99)}"
                    })
                    
                    await page.goto("https://grok.com", wait_until="networkidle", timeout=60000)
                    await emulate_human_delay()
                    
                    # Добавляем случайные движения мыши для эмуляции человеческого поведения
                    await page.mouse.move(random.randint(100, 500), random.randint(100, 500))
                    await emulate_human_delay()
                    
                    grok = GrokDriver(page)
                    await grok.send_prompt(prompt)
                    await grok.wait_for_response()
                    result = await grok.extract_response()
                    print("Ответ Grok:", result)
                    return result
                except Exception as e:
                    print(f"Ошибка при работе с браузером (попытка {attempt + 1}/{MAX_RETRIES}): {e}")
                    if attempt < MAX_RETRIES - 1:
                        print(f"Ожидание {RETRY_DELAY} секунд перед следующей попыткой...")
                        await asyncio.sleep(RETRY_DELAY)
                    else:
                        raise
                finally:
                    await browser.close()
        except Exception as e:
            print(f"Критическая ошибка при запуске браузера (попытка {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Ожидание {RETRY_DELAY} секунд перед следующей попыткой...")
                await asyncio.sleep(RETRY_DELAY)
            else:
                sys.exit(1)

async def main():
    try:
        if os.path.exists(PROMPT_FILE):
            with open(PROMPT_FILE) as f:
                prompt = f.read().strip()
                if prompt:
                    await run_bot(prompt)
                    # Очищаем файл после обработки
                    with open(PROMPT_FILE, "w") as f:
                        f.write("")
    except Exception as e:
        print("Ошибка в main:", e)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)