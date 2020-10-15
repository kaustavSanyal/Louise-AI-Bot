from flask import Flask, render_template, request
import numpy,random
import speech_recognition as sr
import chatbot as bot
app = Flask(__name__)

#For voice recording
r = sr.Recognizer()
mic = sr.Microphone()

# english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# trainer = ChatterBotCorpusTrainer(english_bot)
# trainer.train("chatterbot.corpus.english")


@app.route("/")
def home():
    return render_template("template_for_testing.html")
    #return render_template("not_used_home.html")


@app.route("/voice")
def get_voice_response():
    userText = request.args.get('msg')
    with mic as source:
        print("Speak anything")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said", str(text))
        return (str(text))

    except Exception as Error:
        print(Error)
        return  Error

    return ("Code error : Try Block Not Executed")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    try:
        print("You typed", str(userText))

        results = bot.model.predict([bot.bag_of_words(userText, bot.words)])[0]
        results_index = numpy.argmax(results)

        tag = bot.labels[results_index]

        if results[results_index] > 0.7:

            for tg in bot.data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            global output
            output=(random.choice(responses))
        else:
            output="I didn't get that plz try try reframing your query else raise a new error registration request from the pane above"

        print(str(output))
        return (str(output))

    except Exception as Error:
        print(Error)
        return  Error

    return userText
    return str(english_bot.get_response(userText))



if __name__ == "__main__":
    app.run(port=8080)