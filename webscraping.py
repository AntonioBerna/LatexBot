from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class Scraper:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    def __init__(self):
        self.browser = webdriver.Chrome("/Users/clevercode/Desktop/LatexBot/chromedriver", options=self.options)
        self.url = "http://www.sciweavers.org/free-online-latex-equation-editor"

    def scrape(self, text):
        try:
            self.browser.get(self.url)
            print("Scraping...")
            self.browser.find_element_by_id("texEqnEditor").send_keys(text)
            self.browser.find_element_by_xpath("//select[@name='eq_font']/option[text()='78']").click()
            self.browser.find_element_by_xpath("//select[@name='eq_imformat']/option[text()='PNG']").click()
            self.browser.find_element_by_id("submit_tex2img").click()
            time.sleep(10)
            img_url = self.browser.find_element_by_xpath("//div[@id='iImgLoader']/img").get_attribute("src")
            print(img_url)
            self.browser.quit()
            print("Finish.")
            return img_url
        except Exception as e:
            print("Something Went Wrong...", e)


# scraper = Scraper()
# scraper.scrape("\\frac{1}{x}")