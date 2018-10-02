from chatterbot import ChatBot

chatbot = ChatBot('Star Planet Robot', trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
trained = False


def train():
    chatbot.train('chatterbot.corpus.chinese')
    global trained
    trained = True


def get_response(text):
    if not trained:
        train()
    return chatbot.get_response(text)
