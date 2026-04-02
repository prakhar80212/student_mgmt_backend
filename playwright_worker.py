import sys
import base64
import random
import time
import json

from playwright.sync_api import sync_playwright

USER_AGENTS = json.loads(sys.argv[1])
url = sys.argv[2]
ua  = random.choice(USER_AGENTS)

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--window-size=1920,1080",
        ],
    )
    context = browser.new_context(
        user_agent=ua,
        viewport={"width": 1920, "height": 1080},
        locale="en-IN",
        timezone_id="Asia/Kolkata",
        extra_http_headers={
            "Accept-Language": "en-IN,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        },
    )
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'plugins',   { get: () => [1,2,3,4,5] });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-IN','en'] });
        window.chrome = { runtime: {} };
    """)
    page = context.new_page()
    try:
        time.sleep(random.uniform(0.5, 1.5))
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # Inject MutationObserver BEFORE the modal appears — auto-clicks close the moment it's added
        page.evaluate("""
            () => {
                const dismiss = () => {
                    const btn = document.querySelector('[aria-label="Best deal Modal Close Icon"], .jd_modal_close_bd, .bestdeal_box .jd_modal_close');
                    if (btn) { btn.click(); return true; }
                    return false;
                };
                if (!dismiss()) {
                    const observer = new MutationObserver(() => {
                        if (dismiss()) observer.disconnect();
                    });
                    observer.observe(document.body, { childList: true, subtree: true });
                }
            }
        """)

        time.sleep(6)

        # Force-remove any remaining modal just in case
        page.evaluate("""
            () => {
                document.querySelectorAll('[class*="bestdeal"], [class*="jd_modal"]').forEach(el => el.remove());
                document.body.style.overflow = 'auto';
                document.documentElement.style.overflow = 'auto';
            }
        """)
        time.sleep(0.5)

        # Scroll to trigger lazy-loaded content
        page.evaluate("""
            () => new Promise(resolve => {
                let total = 0;
                const step = () => {
                    window.scrollBy(0, 300);
                    total += 300;
                    if (total < document.body.scrollHeight) setTimeout(step, 100);
                    else { window.scrollTo(0, 0); resolve(); }
                };
                step();
            })
        """)
        time.sleep(random.uniform(1.0, 2.0))

        data = page.screenshot(full_page=True, type="png")
        print(base64.b64encode(data).decode("utf-8"))
    finally:
        browser.close()
