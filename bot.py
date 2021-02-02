from TelegramBot import Bot
import json
import time


def main():
    config = json.load(open("config.json"))
    client = Bot(config["token"], config["admins"])
    update_id = client.latestUpdate()

    print("Bot in esecuzione.")
    time.sleep(5)
    while True:
        new_id = client.latestUpdate()
        if new_id != update_id:
            update_id = new_id
            message_text = client.getMessageText(new_id)
            chat_id = client.getChatId(new_id)
            username = client.getUserName(new_id)

            client.addUser(username)

            config = json.load(open("config.json"))
            client = Bot(config["token"], config["admins"])
            if client.isAdmin(new_id):
                if message_text == "/start":
                    client.sendMessage(chat_id, f'Ciao {username}, {config["description"]}')

                if message_text.startswith("/latex"):
                    try:
                        message_text_splitted = message_text[0:6].split()
                        message_text_splitted.append(message_text[7:])
                        print("Latex Command: ", message_text_splitted)

                        if len(message_text_splitted) == 2 and message_text_splitted[1] != "":
                            client.sendMessage(chat_id, "🔥Attendi qualche secondo...🔥")
                            client.sendPhoto(chat_id, client.scrape(message_text_splitted[1]))
                        else:
                            client.sendMessage(chat_id, "Il comando è stato utilizzato in modo errato!🔥\nSe hai bisogno di aiuto digita /help")
                    except Exception as e:
                        print(f"Il Bot ha generato il seguente errore:\n{e}")

                if message_text == "/sviluppatore":
                    client.sendMessage(chat_id, config["developer"])

                if message_text == "/help":
                    client.sendMessage(chat_id, config["helper"])

                if username == config["admins"][0]:  # CleverCode
                    if message_text.startswith("/aggiungi_admin"):
                        try:
                            message_text_splitted = message_text.split()
                            if len(message_text_splitted) == 2:
                                client.addAdmin(message_text_splitted[1])
                                client.sendMessage(chat_id, f"L'admin {message_text_splitted[1]} è stato aggiunto.")
                            else:
                                client.sendMessage(chat_id, "Il comando è stato utilizzato in maniera errata.")
                        except Exception as e:
                            print(f"Il Bot ha generato il seguente errore:\n{e}")

                    if message_text.startswith("/rimuovi_admin"):
                        try:
                            message_text_splitted = message_text.split()
                            if len(message_text_splitted) == 2:
                                if client.removeAdmin(message_text_splitted[1]):
                                    client.sendMessage(chat_id, f"L'admin {message_text_splitted[1]} è stato rimosso.")
                                else:
                                    client.sendMessage(chat_id, "Nessun admin trovato con questo username.")
                            else:
                                client.sendMessage(chat_id, "Il comando è stato utilizzato in maniera errata.")
                        except Exception as e:
                            print(f"Il Bot ha generato il seguente errore:\n{e}")

                    if message_text == "/lista_admin":
                        try:
                            config = json.load(open("config.json"))

                            if config["admins"]:
                                message = "Lista Admins:"
                                count_admins = 0
                                for admin in config["admins"]:
                                    message += f"\n{count_admins + 1}) {admin}"
                                    count_admins += 1
                            else:
                                message = "La lista è attualmente vuota."

                            client.sendMessage(chat_id, message)
                        except Exception as e:
                            print(f"Il Bot ha generato il seguente errore:\n{e}")

                    if message_text == "/lista_utenti":
                        try:
                            users = json.load(open("users.json"))

                            if users["users"]:
                                message = "Lista Utenti:"
                                count_users = 0
                                for user in users["users"]:
                                    message += f"\n{count_users + 1}) {user}"
                                    count_users += 1
                            else:
                                message = "La lista è attualmente vuota."

                            client.sendMessage(chat_id, message)
                        except Exception as e:
                            print(f"Il Bot ha generato il seguente errore:\n{e}")

            else:
                client.sendMessage(chat_id, "Non sei abilitato ad utilizzare questo bot!🔥")
