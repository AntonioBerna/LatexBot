import requests
import json


class Bot:
    offset = 0

    def __init__(self, token: str, admins: list):
        self.api_url = f'https://api.telegram.org/bot{token}/'
        self.admins = admins
        self.url = "https://e1kf0882p7.execute-api.us-east-1.amazonaws.com/default/latex2image"  # Sito Web: https://latex2image.joeraut.com

    def status(self, update_id):
        r = requests.get(f"{self.api_url}getUpdates").json()
        results = r["result"]
        for result in results:
            if result["update_id"] == update_id:
                return result

    def getChatId(self, update_id):
        try:
            update = self.status(update_id)
            return update["message"]["chat"]["id"]
        except KeyError:
            return None

    def getMessageText(self, update_id):
        try:
            update = self.status(update_id)
            return update["message"]["text"]
        except KeyError:
            return None

    def getUserName(self, update_id):
        try:
            update = self.status(update_id)
            return update["message"]["chat"]["username"]
        except KeyError:
            return None

    def latestUpdate(self):
        try:
            r = requests.get(f"{self.api_url}getUpdates", params={"offset": self.offset}).json()
            if len(r["result"]) == 0:
                return 0
            update_id = r["result"][len(r["result"]) - 1]["update_id"]
            self.offset = update_id - 1
            return update_id
        except KeyError:
            return None

    def isAdmin(self, update_id):
        username = self.getUserName(update_id)
        if username in self.admins:
            return True
        return False

    def sendMessage(self, chat_id, messageText):
        payload = {
            "chat_id": chat_id,
            "parse_mode": "HTML",
            "text": messageText,
        }
        requests.post(f'{self.api_url}sendMessage', params=payload)

    def sendPhoto(self, chat_id, photo_url):
        payload = {
            "chat_id": chat_id,
            "parse_mode": "HTML",
            "photo": photo_url
        }
        requests.post(f'{self.api_url}sendPhoto', params=payload)

    def addUser(self, username):
        users = json.load(open("users.json"))

        if username not in users["users"]:
            users["users"].append(username)

        with open("users.json", "w") as file:
            json.dump(users, file, indent=2)

    def addAdmin(self, username):
        config = json.load(open("config.json"))

        if username not in config["admins"]:
            config["admins"].append(username)

        with open("config.json", "w") as file:
            json.dump(config, file, indent=2)

    def removeAdmin(self, username):
        config = json.load(open("config.json"))

        if username in config["admins"]:
            config["admins"].remove(username)
            with open("config.json", "w") as file:
                json.dump(config, file, indent=2)
            return True
        return False

    def scrape(self, latex):
        try:
            print("Scraping...")
            img_url = requests.post(self.url, data=json.dumps({"latexInput": "\\begin{align*}\n" + latex + "\n\\end{align*}\n", "outputFormat": "PNG", "outputScale": "500%"})).json()["imageUrl"]
            print("Finish.")
            return img_url
        except Exception as e:
            print(f"Il Bot ha generato il seguente errore:\n{e}")

# client = Bot("token", ["CleverCode"])
# print(client.scrape("f(x) = \\frac{1}{x}"))
