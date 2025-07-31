from strands import Agent,tool
from bedrock_agentcore.tools.browser_client import BrowserClient
from playwright.sync_api import sync_playwright


region="us-west-2"

@tool
def capture_page(url: str) -> str:
    """
    URL Access the URL and capture a screenshot.
    Return the file path of the captured screenshot.
    """

    file_name = "pokemon.png"

    client = BrowserClient(region)
    client.start()

    ws_url, headers = client.generate_ws_headers()

    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(
            endpoint_url=ws_url, headers=headers
        )
        default_context = browser.contexts[0]
        page = default_context.pages[0]

        page = browser.new_page()
        page.goto(url)
        print(page.title())

        page.screenshot(path=file_name)

        browser.close()

    client.stop()

    return file_name


# 创建包含两个工具的Agent
agent = Agent(tools=[ capture_page])
result = agent("Capture Top 5 pokemon game in google play")

print("📋 Search Results:",result)
