import requests


class Scraper:

    def __init__(self):
        self.url = "https://latex2image.joeraut.com/"

    def scrape(self, latex):
        print("Scraping...")
        img_url = requests.post(self.url + "convert", data={"latexInput": latex, "outputFormat": "PNG", "outputScale": "500%"}).json()["imageURL"]
        print("Finish.")
        return self.url + img_url


# scraper = Scraper()
# scraper.scrape("\\frac{1}{x}")