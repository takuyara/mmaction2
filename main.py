import torch
from mmaction.apis import init_recognizer, inference_recognizer

device = 'cpu'
device = torch.device(device)

model = init_recognizer("myconfig_full.py", device=device)

res = inference_recognizer(model, 'demo/demo.mp4')

print(res)
