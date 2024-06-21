from helperfunctions import *
from flask import Flask, render_template, request, Response, redirect

app = Flask(__name__)
language, raw_address, customer_address, raw_order, pizza_size, pizza_topping, play_audio = None, None, None, None, None, None, None

def clean_text(text):
    stop_words = stopwords.words("english")
    stop_words.extend(["gimme", "lemme", "cause", "cuz", "imma", "gonna", "wanna", "please", "the", "and",
                       "gotta", "hafta", "woulda", "coulda", "shoulda", "howdy", "day", "can", "could",
                       "my", "mine", "I" "hey", "yoo", "deliver", "delivery", "delivered", "piece", "want",
                       "send", "sent", "order", "pizza", "piz", "pizze", "address", "addrez", "to", "too"])
    clean_texts = " ".join([word.replace("X", "").replace("/", "") for word in text.split() if word.lower() not in stop_words])
    return clean_texts

@app.route("/")
def root():
    global language, raw_address, customer_address, raw_order, pizza_size, pizza_topping, play_audio
    language, raw_address, customer_address, raw_order, pizza_size, pizza_topping, play_audio = None, None, None, None, None, None, None

    file = ["info.wav", "info_record.wav", "info_repeat.wav", "topping.wav", "topping_record.wav", "topping_repeat.wav"]
    for i in file:
        bash_command = str(r"find . -path \*/" + i + " -delete")
        os.system(bash_command)
    return render_template("main.html")

@app.route('/about')
def about():
    return render_template("about.html")


#----------- INFORMATION
@app.route("/get_info", methods=["POST"])
def get_info():
    global play_audio
    play_audio = "info.wav"
    result = "Welcome to Pizza AI Plaza, how's it going? Where should we send your delicious pizza order to?"
    text_to_speech(result,play_audio)
    return render_template("getinfo.html")

@app.route("/get_info_redirect", methods=["GET", "POST"])
def get_info_redirect():
    global customer_address, play_audio
    customer_address = clean_text(raw_address)  # clean the stop words from audio files
    play_audio = "info_repeat.wav"
    result = "Just want to confirm, did you ask for the pizza to be dropped off at " + customer_address + \
             "? If not, no worries, just give the recording again button a tap."
    
    if customer_address is not None:
        print("\n\n\n------------" + customer_address + "-------------\n\n\n")
    else:
        print("\n\n\n------------customer_address is None-------------\n\n\n")

    text_to_speech(result, play_audio)
    return render_template("getInfoRedirect.html", customerAddress=customer_address)

@app.route("/get_info_record_wav", methods=["POST"])
def get_info_record_wav():
    global raw_address

    if raw_address is not None:
        print("\n\n\n------------" + raw_address + "-------------\n\n\n")
    else:
        print("\n\n\n------------customer_address is None-------------\n\n\n")

    if "info_record_wav" not in request.files:
        return "No audio file found"
    else:
        file = request.files["info_record_wav"]
        if file.filename == "":
            return "No audio file selected"
        else:
            save_audio(file, "info_record.wav")
            raw_address = speech_to_text("info_record.wav")
            if raw_address is None:
                return "Could not process audio file"
            print(raw_address)

            if raw_address is not None:
                print("\n\n\n------------" + raw_address + "-------------\n\n\n")
            else:
                print("\n\n\n------------customer_address is None-------------\n\n\n")
    return render_template("getInfoRedirect.html")



#---------- TOPPINGS
@app.route("/get_topping", methods=["POST"])
def get_topping():
    global play_audio
    play_audio = "topping.wav"
    result = "At Pizza AI Plaza, we offer a mouth-watering selection of giant, large, and medium pizzas, piled high with 8 delectable toppings to choose from. " \
             "See the options in the picture below and indulge in the perfect pizza for you!"
    text_to_speech(result, play_audio)
    return render_template("getTopping.html")


@app.route("/get_topping_record_wav", methods=["POST"])
def get_topping_record_wav():
    global raw_order
    if "topping_record_wav" not in request.files:
        return "No audio file found"
    else:
        file = request.files["topping_record_wav"]
        if file.filename == "":
            return "No audio file selected"
        else:
            save_audio(file, "topping_record.wav")
            raw_order = speech_to_text("topping_record.wav")
            if raw_order is None:
                return "Could not process audio file (@get_topping_record_wav)"
            
            if raw_order is not None:
                print("\n\n\n------------" + raw_order + "-------------\n\n\n")
            else:
                print("\n\n\n------------customer_address is None-------------\n\n\n")


            print(raw_order)


    return redirect("/get_topping_redirect")


@app.route("/get_topping_redirect", methods=["GET", "POST"])
def get_topping_redirect():
    global pizza_size, pizza_topping, play_audio
    clean_order = clean_text(raw_order)  # clean the stop words from audio files
    pizza_size, pizza_topping = get_keywords(clean_order)

    print(pizza_size,pizza_topping)

    play_audio = "topping_repeat.wav"
    result = "Just wanted to make sure, did you order a " + pizza_size[0] + " pizza with: " + " ".join(map(str, pizza_topping)) + \
             " on it? If not, no worries, just give the recording again button another press."
    text_to_speech(result, play_audio)
    return render_template("getToppingRedirect.html", pizzaSize=pizza_size[0], pizzaTopping=pizza_topping)



@app.route("/get_order", methods=["POST"])
def get_order():
    global play_audio
    play_audio = "order.wav"
    if not customer_address:
        print("\n\n\n--------missing address----------\n\n\n")
    elif not pizza_size:
        print("\n\n\n------------missing pizza size-----------\n\n\n")
        order_size = ["Not defined"]
    elif not pizza_topping:
        print("\n\n\n------------missing pizza topping---------\n\n\n")

    result = str("Thanks for using the PizzAI Plaza to place your order. Just wanted to double check that I got it right, you want a " +
                 pizza_size[0] + " pizza with " + " ".join(map(str, pizza_topping)) + ". And the delivery address is " + customer_address +
                 ", is that correct?")
    text_to_speech(result, play_audio)
    return render_template("getOrder.html", customerAddress=customer_address, orderSize=pizza_size[0], orderTopping=pizza_topping)


@app.route("/play_local_wav")
def play_local_wav():
    return Response(play_local_wav_file(play_audio), mimetype="audio/mpeg")

if __name__=="__main__":
    app.run(debug=True)
