import json
import torch
import argparse
from PIL import Image
import torch.nn.functional as F
import torchvision.transforms as transforms
from torchvision.models import shufflenet_v2_x0_5


def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str)
    parser.add_argument('--model-path', type=str, default='imagenet_class_index.json')
    return parser.parse_args()


DEVICE = torch.device('cpu')
ARGS = make_args()


def main():

    # load a lightweight classifier trained on imagenet
    model = shufflenet_v2_x0_5(pretrained=True)
    model = model.eval().to(DEVICE)

    preprocessing = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    class_index = json.load(open(ARGS.model_path))
    class_decoder = {k: class_index[str(k)][1] for k in range(len(class_index))}

    image = Image.open(ARGS.path)
    width, height = image.size
    assert width > 0 and height > 0

    x = preprocessing(image)
    x = x.unsqueeze(0)
    x = x.to(DEVICE)

    with torch.no_grad():
        logits = model(x)

    probabilities = F.softmax(logits, dim=1)
    probabilities = probabilities.squeeze(0)
    probabilities = probabilities.cpu()
    values, indices = probabilities.sort(descending=True)

    print('five most probable classes:')
    for j, i in enumerate(indices[:5]):
        class_name = class_decoder[i.item()]
        class_probability = values[j].item()
        print(f'{j + 1}. {class_name}, {class_probability:.3f}')


main()
