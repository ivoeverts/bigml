# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask
from flask import jsonify

# spacy
import spacy
import numpy as np

# load a couple of models, ready for serving
models = {
    'en_w2v': spacy.load('en_core_web_lg'),
    # 'nl_w2v': spacy.load('nl_core_news_sm'),
    'en_distilbert': spacy.load('en_trf_distilbertbaseuncased_lg')
}

# method for combining word vectors
pooling_operator = 'mean'

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/<text>')
@app.route('/<text>/<model>')
@app.route('/<text>/<model>/<pooling_operator>')
def enc(text: str, model: str = 'en_w2v', pooling_operator: str = 'mean'):
    result = None
    if pooling_operator == 'mean':
        result = models[model](text).vector
    else:
        raise ValueError(f'Unkown pooling_operator: {pooling_operator}')
    return jsonify(result.tolist())

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
