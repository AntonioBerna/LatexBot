from webscraping import Scraper
from bot import Bot
import json


def main():
    scraper = Scraper()
    config = json.load(open("config.json"))
    client = Bot(config["token"], config["admins"])
    update_id = client.latestUpdate()

    print("Bot in esecuzione.")
    while True:
        new_id = client.latestUpdate()
        if new_id != update_id:
            update_id = new_id
            message_text = client.getMessageText(new_id)
            chat_id = client.getChatId(new_id)
            username = client.getUserName(new_id)

            if client.isAdmin(new_id):
                if message_text == "/start":
                    client.sendMessage(chat_id, f'Ciao {username}, {config["description"]}')

                if message_text.startswith("/latex"):
                    try:
                        message_text_splitted = message_text[0:6].split()
                        message_text_splitted.append(message_text[7:])
                        print("Latex Command: ", message_text_splitted)

                        if checkMessage(message_text_splitted):
                            client.sendMessage(chat_id, "🔥Attendi qualche secondo...🔥")
                            client.sendPhoto(chat_id, scraper.scrape(message_text_splitted[1]))
                        else:
                            client.sendMessage(chat_id, "Il comando è stato utilizzato in modo errato!🔥\nSe hai bisogno di aiuto digita /help")
                    except:
                        pass

                if message_text == "/sviluppatore":
                    client.sendMessage(chat_id, "🔥Informazioni Sviluppatore🔥\n\nTelegram: @CleverCode\nYoutube: https://www.youtube.com/c/CleverCode\nInstagram: https://www.instagram.com/clever_code/\nGithub: https://github.com/AntonioBerna")

                if message_text == "/help":
                    client.sendMessage(chat_id, "Ecco alcuni esempi di utilizzo corretto di @LatextBot 🔥:\n\n1) /latex \int x dx\n2) /latex \int_a^b f(x) dx = F(b) - F(a)\n3) /latex \\frac{1}{x^2}\n\nBene, ora riprova, altrimenti contatta lo sviluppatore /sviluppatore😎🔥")

            else:
                client.sendMessage(chat_id, "Non sei abilitato ad utilizzare questo bot!🔥")


def checkMessage(message_text_splitted):
    return len(message_text_splitted) == 2 and message_text_splitted[1] != ""


if __name__ == '__main__':
    main()
