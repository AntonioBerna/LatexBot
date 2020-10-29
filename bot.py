import requests


class Bot:
    offset = 0

    def __init__(self, token: str, admins: list):
        self.api_url = f'https://api.telegram.org/bot{token}/'
        self.admins = admins

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
            update_id = r["result"][len(r["result"])-1]["update_id"]
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

    def sendPhoto(self, chat_id, url):
        payload = {
            "chat_id": chat_id,
            "parse_mode": "HTML",
            "photo": url
        }
        requests.post(f'{self.api_url}sendPhoto', params=payload)