from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from nfateev_corpus1 import train_corpus_full
#train_corpus_full = train_corpus_full.split(', ')
#print(train_corpus_full, '\n\n\n')
# Create a new instance of a ChatBot
bot = ChatBot(
    'train',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database-chatbot.db' #use sqlite
    #database_uri = "postgresql://rusbot:rusbot@localhost/rus_bot"  #use postgres
)

# Create a new trainer for the chatbot, using corpus trainer - uncomment, if demand
trainer = ListTrainer(bot)

# Train the chatbot based on the english corpus - uncomment, if demand
#trainer.train("chatterbot.corpus.english")

#print('Type something to begin...')
for dialog in train_corpus_full:
    trainer.train(dialog)
trainer.export_for_training('./attempt1.json')


# if __name__ =='__main__':
#     # The following loop will execute each time the user enters input
#     trainer.train(train_corpus_full)
#     while True:
#         try:
#             user_input = input()

#             bot_response = bot.get_response(user_input)

#             print(bot_response)

#         # Press ctrl-c or ctrl-d on the keyboard to exit
#         except (KeyboardInterrupt, EOFError, SystemExit):
#             break