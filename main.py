from flask import Flask, Response
import io
import zlib
from urllib.parse import unquote

# spacy
import spacy
import numpy as np

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

    return Response(response=compress_numpy_array(result), status=200,
                    mimetype="application/octet_stream")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
