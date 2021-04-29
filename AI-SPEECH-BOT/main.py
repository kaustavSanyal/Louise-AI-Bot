from flask import Flask, render_template, request
import numpy,random
#import speech_recognition as sr
import chatbot as bot
app = Flask(__name__)


current_user = "Jane"

questions_db = {"Syntax Error": [3, "Q1", "Q2", "Q3"]}




@app.route("/")
def home():
    return render_template("template_for_testing.html")
    #return render_template("not_used_home.html")

@app.route("/saveAnswer")
def get_bot_response_save_answer():
    userText = request.args.get('msg')
    print("saving : ", userText)
    return "Saved"

@app.route("/ask")
def get_bot_question():
    userText = request.args.get('msg')
    tag = request.args.get('question_tag')
    question_no = request.args.get('question_number')
    print("msg", userText)
    print("Question No",question_no)
    print("TAG ", tag)
    print("tag in db", tag in questions_db)
    print(questions_db[tag][int(question_no)])
    return questions_db[tag][int(question_no)]

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
                    responses = random.choice(responses)
                    if tag in questions_db:
                        responses += "|true|" + str(questions_db[tag][0]) + "|" + tag
                    else:
                        responses += "|false|0|empty"

            global output
            output=responses
        else:
            output="I didn't get that plz try try reframing your query else raise a new error registration request from the pane above|false|0|empty"

        print(str(output))
        return (str(output))

    except Exception as Error:
        print(Error) 
        return  Error

    return userText
    



if __name__ == "__main__":
    app.run(port=8080)