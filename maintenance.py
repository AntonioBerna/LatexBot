from bot import Bot
import json


def main():
    config = json.load(open("config.json"))
    client = Bot(config["token"], config["admins"])
    update_id = client.latestUpdate()

    print("Manutenzione Bot in esecuzione.")
    while True:
        new_id = client.latestUpdate()
        if new_id != update_id:
            update_id = new_id
            message_text = client.getMessageText(new_id)
            chat_id = client.getChatId(new_id)
            username = client.getUserName(new_id)

            if client.isAdmin(new_id):
                if message_text == "/start" or message_text == "/latex":
                    client.sendMessage(chat_id, f"Ciao {username}, @LatextBot è attualmente in manutenzione...\n\nPer maggiori informazioni contatta lo sviluppatore digitando /sviluppatore")

                if message_text == "/sviluppatore":
                    client.sendMessage(chat_id, "🔥Informazioni Sviluppatore🔥\n\nTelegram: @CleverCode\nYoutube: https://www.youtube.com/c/CleverCode\nInstagram: https://www.instagram.com/clever_code/\nGithub: https://github.com/AntonioBerna")

                if message_text == "/help":
                    client.sendMessage(chat_id, "Ecco alcuni esempi di utilizzo corretto di @LatextBot 🔥:\n\n1) /latex \int x dx\n2) /latex \int_a^b f(x) dx = F(b) - F(a)\n3) /latex \\frac{1}{x^2}\n\nBene, ora riprova, altrimenti contatta lo sviluppatore /sviluppatore😎🔥")

            else:
                client.sendMessage(chat_id, "Non sei abilitato ad utilizzare questo bot!🔥")


if __name__ == '__main__':
    main()
