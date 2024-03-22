import random
from pathlib import Path

import markovify
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(import_name=__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
CORS(app=app)

MIN_LENGTH = 3
MAX_LENGTH = 50
MIN_STATE_SIZE = 2
MAX_STATE_SIZE = 5
MAX_TRIES = 10

class SentencesByChar(markovify.Text):
    def word_split(self, sentence):
        return list(sentence)

    def word_join(self, words):
        return "".join(words)
    
@app.route("/")
def home(name=None):
    return render_template("index.html", name=name)


@app.route("/name")
def generate_name():
    output_size = request.args.get(
        key="max_length", default=random.randint(MIN_LENGTH, MAX_LENGTH)
    )
    state_size = request.args.get(
        key="state_size", default=random.randint(MIN_STATE_SIZE, MAX_STATE_SIZE)
    )
    model_type = request.args.get(
        key="model_type", default=random.choice(seq=["word", "char"])
    )
    tries = request.args.get(key="tries", default=MAX_TRIES)
    model_file = Path("model") / f"{model_type}_{state_size}.json"
    if model_type == "char":
        model = SentencesByChar.from_json(json_str=model_file.read_text())
    else:
        model = markovify.Text.from_json(json_str=model_file.read_text())
    generated = model.make_short_sentence(
        max_chars=output_size, test_output=False, tries=int(tries)
    )
    while generated is None:
        generated = model.make_short_sentence(
            max_chars=output_size, test_output=False, tries=int(tries)
        )
    app.logger.info(msg=generated)
    return jsonify(
        {
            "name": generated,
            "state_size": state_size,
            "output_size": output_size,
            "model_type": model_type,
            "tries": tries,
        }
    )
