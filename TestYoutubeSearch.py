import pytest
from playwright.sync_api import Playwright, sync_playwright


@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, channel="chrome")
        yield browser
        browser.close()
        search_data = "Niki Minaj"


def test_youtube_search(browser: Playwright):
    page = browser.new_page()
    website = "https://www.youtube.com/"
    search_data = "Niki Minaj"
    page.goto(website)
    page.type('input[id="search"]', search_data)
    page.press("#search", "Enter")
    page.wait_for_timeout(3000)
    videos = page.locator("#video-title")

    if not videos.count() >=10:
        print("Please, change search value")
    assert videos.count() >= 10
    links = []
    for link in videos.all():
        url = link.get_attribute('href')
        if url:
            if '/watch' in url:
                links.append(f'{website}{url}')

        if len(links) ==10:
            break

    print(*links, sep = "\n")

