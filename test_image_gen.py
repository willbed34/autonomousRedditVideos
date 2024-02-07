import tensorflow as tf
from safetensors import safe_open

model_path = r"picxReal_10.safetensors"

tensors = {}
with safe_open(model_path, framework="pt", device=0) as f:
    for k in f.keys():
        tensors[k] = f.get_tensor(k)

print(tensors)