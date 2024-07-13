import re
from playwright.sync_api import Playwright, sync_playwright

# 指定要访问的页面列表
url_list = ["https://open-uat.nwplatform.com.cn/",
            "https://open-uat.nwplatform.com.cn/appStore",
            "https://open-uat.nwplatform.com.cn/open-capability",
            "https://open-uat.nwplatform.com.cn/developer/doc",
            "https://open-uat.nwplatform.com.cn/developer/search",
            "https://open-uat.nwplatform.com.cn/account/notify-message",
            "https://open-uat.nwplatform.com.cn/account/info",
            "https://open-uat.nwplatform.com.cn/developer/console",
            "https://open-uat.nwplatform.com.cn/appStore/f13d6a9626ea4b25aaf46819616c14b6",
            "https://open-uat.nwplatform.com.cn/developer/doc?docCode=b5798f2e&category=GENERAL_ABILITY"]

result_list = {}
lang = {"简体中文": r'[\u4e00-\u9fa5]',
        "繁体中文": r'[\u4e00-\u9fa5\u3400-\u4DBF\uFA0E-\uFA2D]',
        "韩语": r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F\uA960-\uA97F\uD7B0-\uD7FF]',
        "日语": r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u3005\u3099\u309A\u31F0-\u31FF]'}


class TextChecker:
    def __init__(self, playwright: Playwright):
        self.browser = playwright.chromium.launch()
        self.page = self.browser.new_page()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()

    def goto(self, url: str):
        self.page.goto(url)

    def check_east_asian_text(self):
        body_text = self.page.inner_text('body')
        results = {
            'simplified_chinese': bool(re.search(r'[\u4e00-\u9fa5]', body_text)),
            'traditional_chinese': bool(re.search(r'[\u4e00-\u9fa5\u3400-\u4DBF\uFA0E-\uFA2D]', body_text)),
            'korean': bool(
                re.search(r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F\uA960-\uA97F\uD7B0-\uD7FF]', body_text)),
            'japanese': bool(
                re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u3005\u3099\u309A\u31F0-\u31FF]', body_text))
        }
        return results

    def find_text_positions(self, lang):
        selectors = ['h1', 'h2', 'h3', 'p', 'li', 'span', 'a']
        results = {k: [] for k in selectors}
        for selector in selectors:
            elements = self.page.query_selector_all(selector)
            for element in elements:
                text = element.inner_text()
                if re.search(lang, text):
                    results[selector].append(text)
        return results


with sync_playwright() as playwright:
    checker = TextChecker(playwright)
    for url in url_list:
        checker.goto(url)
        # presence_results = checker.check_east_asian_text()
        # print("Presence of East Asian texts:", presence_results)

        position_results = checker.find_text_positions(lang=lang.get('简体中文'))
        # print("Positions containing East Asian texts:", position_results)
        result_list[url] = position_results
        pass
