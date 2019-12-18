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
from flask import Flask, Response
import io
import zlib
from urllib.parse import unquote

# spacy
import spacy
import numpy as np

is_using_gpu = spacy.prefer_gpu()
print(f'GPU: {is_using_gpu}')

def compress_numpy_array(numpy_array):
    """
    Returns the given numpy array as compressed bytestring,
    the uncompressed and the compressed byte size.
    """
    bytestream = io.BytesIO()
    np.save(bytestream, numpy_array)
    return zlib.compress(bytestream.getvalue())

# load a couple of models, ready for serving
models = {
    'w2v_sm': spacy.load('en_core_web_sm'),
    'w2v_md': spacy.load('en_core_web_md'),
    'w2v_lg': spacy.load('en_core_web_lg'),
    'bert': spacy.load('en_trf_bertbaseuncased_lg'),
    'roberta': spacy.load('en_trf_robertabase_lg'),
    'distilbert': spacy.load('en_trf_distilbertbaseuncased_lg'),
    'xlnet': spacy.load('en_trf_xlnetbasecased_lg')
}

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/<text>')
@app.route('/<text>/<model>')
@app.route('/<text>/<model>/<pooling_operator>')
def enc(text: str, model: str = 'w2v_sm', pooling_operator: str = 'mean'):
    result = None
    if pooling_operator == 'mean':
        result = models[model](unquote(text)).vector
    else:
        raise ValueError(f'Unkown pooling_operator: {pooling_operator}')
    # return result
    return Response(response=compress_numpy_array(result), status=200,
                    mimetype="application/octet_stream")

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
# [END gae_python37_app]
