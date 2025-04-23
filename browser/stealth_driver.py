from playwright.async_api import async_playwright
import yaml
import os

with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)

async def launch_browser_with_profile():
    playwright = await async_playwright().start()
    
    # Ensure profile directory exists and is empty
    os.makedirs(settings["profile_path"], exist_ok=True)
    
    args = [
        "--disable-blink-features=AutomationControlled",
        "--start-maximized",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--disable-extensions",
        "--disable-default-apps",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-networking",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-breakpad",
        "--disable-component-extensions-with-background-pages",
        "--disable-features=TranslateUI,BlinkGenPropertyTrees",
        "--disable-ipc-flooding-protection",
        "--disable-renderer-backgrounding",
        "--enable-features=NetworkService,NetworkServiceInProcess",
        "--force-color-profile=srgb",
        "--metrics-recording-only",
        "--password-store=basic",
        "--use-mock-keychain",
        "--window-size=1920,1080",
        "--new-window",
        "--user-data-dir=" + settings["profile_path"],
        "--no-startup-window",
        "--no-resume-session",
        "--no-session-restore"
    ]
    
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir=settings["profile_path"],
        headless=False,
        args=args,
        ignore_default_args=["--enable-automation", "--enable-background-networking"],
        locale="en-US",
        viewport={"width": 1920, "height": 1080},
        channel="chrome"
    )
    
    page = await context.new_page()
    
    # Close any existing pages
    for p in context.pages:
        if p != page:
            await p.close()

    await page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    window.chrome = {runtime: {}};
    Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3]});
    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(param) {
        if (param === 37445) return "Intel Inc.";
        if (param === 37446) return "Intel Iris OpenGL";
        return getParameter.call(this, param);
    };
    HTMLCanvasElement.prototype.toDataURL = function() {
        return "data:image/png;base64,fakecanvasdata123...";
    };
    """)

    return playwright, context, page