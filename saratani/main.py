import cv2
import numpy as np
from skimage.transform import resize
from keras.models import load_model
import telebot
API_KEY = "6160602075:AAGok7eexscvx4rCTX1Y8uZTHurYxeCh0V8"

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def poppes(message):
    bot.send_message(message.chat.id, "Hello {}! I am Dr Masikwe 👨🏼‍⚕️ from Saratani AI.".format(message.chat.first_name))
    #bot.send_message(message.chat.id, "Help me fill in the following details before diagonisis.")
    bot.send_message(message.chat.id,"Send me your paps smear image")

@bot.message_handler(content_types=["photo"])
def poppes(message):
    fileID = message.json['photo'][-1]['file_id']
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    image_bytes = np.array(downloaded_file)
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    img = resize(img, (64,64,3))
    X = np.asarray(img).astype('float32')
    model = load_model('saratani_predictive_model.h5')
    prediction = model.predict(X.reshape((1, 64, 64, 3)))
    target_values = list(prediction[0])
    _targets = {'normal_Superficial_Intermediate': 0,
                'abnormal_Koilocytotic': 1,
                'abnormal_Dyskeratotic': 2,
                'benign_Metaplastic': 3,
                'normal_Parabasal': 4,
                'abnormal_severe_dysplastic': 5,
                'abnormal_light_dysplastic': 6,
                'abnormal_carcinoma_in_situ': 7,
                'abnormal_moderate_dysplastic': 8,
                'normal_columnar': 9, 
                'normal_superficiel': 10,
                'normal_intermediate': 11}
    targets = list(_targets.keys())

    def stringfy_response(my_response):
        return my_response.replace("_"," ").title()

    response = dict()
    for i in range(0, len(targets)):
        response[str(targets[i])] = float(target_values[i])
    high_prob = dict(sorted(response.items(), key=lambda item: item[1]))
    bot.send_message(message.chat.id, "Highest Probable Feature is: " + "\n\n" + stringfy_response(str(list(high_prob.keys())[-1])) +"\n"+ str(high_prob[list(high_prob.keys())[-1]]))
    bot.send_message(message.chat.id,"Send me another paps smear image for prediction.")

bot.polling()
