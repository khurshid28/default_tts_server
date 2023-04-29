import base64
from flask import (
    Flask,
    request,
    json,
    render_template
)

import torch
import sounddevice as sd
import time

language = "uz"
model_id = 'v3_uz'
sample_rate = 48000
speaker = 'dilnavoz'
put_accent = True
put_yoo = True
device = torch.device('cpu') ######  Agar videokarta kuchli bo'sa shuni 'gpu' ga almashtirsa tezro sintez bo'ladi
# text = "Assalomu alaykum,janob Xurshid o'n @@@@@@  100" ####### Mana shu yerga kiritilgan text o`qiladi

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
# model.to(device)

# audio = model.apply_tts(text=text,
#                         speaker=speaker,
#                         sample_rate=sample_rate,
#                         put_accent=put_accent)

def make_audio(text):
    audio_paths = model.save_wav(text=text,
                                speaker=speaker,
                                sample_rate=sample_rate)
    print(audio_paths)



app = Flask(__name__, template_folder="templates")
app.config['ENV'] = 'development'


@app.route('/getVoice',methods=['POST'])
def getVoice(): 
    print(request.json["text"])
    text = request.json["text"]
    make_audio(text)
    with open("./test.wav", "rb") as binary_file:
        data = binary_file.read()
        wav_file = base64.b64encode(data).decode('UTF-8')
    
    response = app.response_class(
        response=json.dumps({"audio":wav_file}),
        status=200,
        mimetype='application/json'
    )
    return response

    

    
if __name__ == '__main__': 
    app.run(debug=True)



