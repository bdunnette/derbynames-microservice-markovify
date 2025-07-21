import random
from pathlib import Path
import bz2

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
STRIP_PERIODS = True


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
    prompt = request.args.get(key="prompt", default=None)
    strip_periods = request.args.get(key="strip_periods", default=STRIP_PERIODS)
    strip_exclamation = request.args.get(
        key="strip_exclamation", default=random.choice([True, False])
    )
    model_file = Path("model") / f"{model_type}_{state_size}.bz2"
    if model_type == "char":
        model = SentencesByChar.from_json(json_str=bz2.open(model_file, "rt").read())
    else:
        model = markovify.Text.from_json(json_str=bz2.open(model_file, "rt").read())
    if prompt:
        generated = model.make_sentence_with_start(
            beginning=prompt, max_chars=output_size, test_output=False, strict=False
        )
        while generated is None:
            generated = model.make_sentence_with_start(
                beginning=prompt, max_chars=output_size, test_output=False, strict=False
            )
    else:
        generated = model.make_short_sentence(
            max_chars=output_size, test_output=False, tries=int(tries)
        )
        while generated is None:
            generated = model.make_short_sentence(
                max_chars=output_size, test_output=False, tries=int(tries)
            )
    if strip_periods:
        generated = generated.rstrip(".")
    if strip_exclamation:
        generated = generated.rstrip("!")
    app.logger.info(msg=generated)
    return jsonify(
        {
            "name": generated,
            "state_size": state_size,
            "output_size": output_size,
            "model_type": model_type,
            "tries": tries,
            # For compatibility with django-docker
            "temperature": 0,
            "prompt": prompt,
            "strip_periods": strip_periods,
            "strip_exclamation": strip_exclamation,
        }
    )
