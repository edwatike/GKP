from utils.human_emulator import type_like_human, emulate_mouse_move
import asyncio

class GrokDriver:
    def __init__(self, page):
        self.page = page
        self.prompt_selector = "textarea"
        self.submit_selector = "div.relative.aspect-square.flex.flex-col.items-center.justify-center.rounded-full"
        self.response_selector = "div[class*='prose']"

    async def send_prompt(self, prompt):
        await self.page.wait_for_selector(self.prompt_selector)
        await type_like_human(self.page, self.prompt_selector, prompt)
        await emulate_mouse_move(self.page)
        await self.page.click(self.submit_selector)

    async def wait_for_response(self, timeout=20):
        try:
            await self.page.wait_for_selector(self.response_selector, timeout=timeout*1000)
        except:
            await self.page.reload()
            await self.send_prompt(prompt)

    async def extract_response(self):
        element = await self.page.query_selector(self.response_selector)
        return await element.inner_text() if element else "[NO RESPONSE]"