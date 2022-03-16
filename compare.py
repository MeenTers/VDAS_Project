#Import Function

import torch
from torch import nn, load, utils
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from torchvision import datasets, transforms, models
from torchvision.models.vgg import model_urls
from os import path, listdir
import os
model_urls['vgg19'] = model_urls['vgg19'].replace('https://', 'http://')

from scipy.spatial import distance_matrix
from scipy.spatial import distance
import pandas as pd
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import argparse
#import cv2

#VGG model
class VGG:
	def __init__(self):
		model = models.vgg19(pretrained=True, progress=True)
		model.classifier = nn.Sequential(*list(model.classifier.children())[:3])
		self.model = model.cuda().eval()

	def __call__(self, x):
		return self.model(x)
vgg = VGG()
def get_features(model, loader):
    features = []
    with torch.no_grad():
        for batch, _ in tqdm(loader):
            if torch.cuda.is_available():
                batch = batch.cuda()
            b_features = model(batch).detach().cpu().numpy()
            for f in b_features:
                features.append(f)

    return features
def get_dataset(images_path):
  transform = transforms.Compose([
    transforms.Resize(size=32),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
  ])

  dataset = datasets.ImageFolder(images_path, transform=transform)
  loader = utils.data.DataLoader(dataset, batch_size=100, shuffle=False, num_workers=1, pin_memory=True)
  return loader
def get_euclidean(base_car,diff_view):
    dist = []
    for i in range(len(diff_view)):
        x = distance.euclidean(base_car[i],diff_view[i])
        dist.append(x)
    return(dist)
def get_damage(distance):
    f_car = ((distance[0] - 0.2)/(55 - 0.2)*100)
    r_car = ((distance[1] - 0.2)/(55 -0.2)*100)
    b_car = ((distance[2] - 0.2)/(55 -0.2)*100)
    l_car = ((distance[3] - 0.2)/(55 -0.2)*100)
    dmgs = [f_car,r_car,b_car,l_car]
    return dmgs


    
if __name__ == '__main__':
   
    parser = argparse.ArgumentParser(description='test program to learn about argparse ')
    parser.add_argument(
        '--c',
        type = str,
        help = 'path model')
    args = parser.parse_args()
    f  = args.c
    # f = 'กข6531/'
    dict = {
    0:"ด้านหน้า",
    1:"ด้านซ้าย",
    2:"ด้านหลัง",
    3:"ด้านขวา"
    }

    base_path = os.path.join('static/images/data/base/'+str(f))
    dmg_path = os.path.join('static/images/data/dmg/'+str(f))
    car_loader = get_dataset(base_path)
    dmg_loader = get_dataset(dmg_path)
    base_feat = get_features(vgg,car_loader)
    dmg_feat = get_features(vgg,dmg_loader)
    eucli= get_euclidean(base_feat,dmg_feat)
    show = get_damage(eucli)

    for j in range(4):
        if round(eucli[j]) < 0.5:
            print('N')
        elif   0.5 <= round(eucli[j]) <= 10.5:
            print('L')
        elif 10.5 < round(eucli[j]) <= 30:
            print('M')
        elif round(eucli[j]) > 30:
            print('H')
   



   #  print(f'The front of  the  car was damaged {round(show[0],2)}%')
   #  print(f'The Right of  the  car was damaged {round(show[1],2)}%')
   #  print(f'The Back  of  the  car was damaged {round(show[2],2)}%')
   #  print(f'The Left  of  the  car was damaged {round(show[3],2)}%')


    # for i in range(0, 4):
    #     if show_out[i] < 1:
    #         print(f'{(dict[i])}ของรถยนต์ไม่มีความเสียหาย')
    #     elif 1 <= show_out[i] < 21:
    #         print(f'{(dict[i])}ของรถยนต์เสียหายน้อยมาก')
    #     elif 21 <= show_out[i]< 41:
    #         print(f'{(dict[i])}ของรถยนต์เสียหายน้อย')
    #     elif 41 <= show_out[i] < 61:
    #         print(f'{(dict[i])}ของรถยนต์เสียหายปานกลาง')
    #     elif 61 <= show_out[i] < 81:
    #         print(f'{(dict[i])}ของรถยนต์เสียหายรุนแรง')
    #     elif show_out[i] >= 81:
    #         print(f'{(dict[i])}ของรถยนต์เสียหายรุนแรงมาก')



   # #45
   #  if show[0] <1:
   #     print(f'The front of the car was not damaged.             ')
   #  elif 1 <= show[0] < 21:
   #     print(f'The front of the car was damaged very little.     ')
   #  elif 21 <= show[0] < 41:
   #     print(f'The front of the car was slightly damaged.        ')
   #  elif 41 <= show[0] < 61:
   #     print(f'The front of the car was moderately damaged.      ')
   #  elif 61 <= show[0] < 81:
   #     print(f'The front of the car was damaged a lot.           ')
   #  else:
   #     print(f'The front of the car was severely damaged.        ')
   #  #50
   #  if show[1] <1:
   #     print(f'The left side of the car was not damaged.         ')
   #  elif 1 <= show[3] < 21:
   #     print(f'The left side of the car was damaged very little. ')
   #  elif 21 <= show[3] < 41:
   #     print(f'The left side of the car was slightly damaged.    ')
   #  elif 41 <= show[3] < 61:
   #     print(f'The left side of the car was moderately damaged.  ')
   #  elif 61 <= show[3] < 81: 
   #     print(f'The left side of the car was damaged a lot.       ')
   #  else:
   #     print(f'The left side of the car was severely damaged.    ')
   #  #44
   #  if show[2] <1:
   #     print(f'The back of the car was not damaged.              ')
   #  elif 1 <= show[2] < 21:
   #     print(f'The back of the car was damaged very little.      ')
   #  elif 21 <= show[2] < 41:
   #     print(f'The back of the car was slightly damaged.         ')
   #  elif 41 <= show[2] < 61:
   #     print(f'The back of the car was moderately damaged.       ')
   #  elif 61 <= show[2] < 81:
   #     print(f'The back of the car was damaged a lot.            ')
   #  else:
   #     print(f'The back of the car was severely damaged.         ')
   #  #49
   #  if show[3] <1:
   #     print(f'The right side of the car was not damaged.        ')
   #  elif 1 <= show[1] < 21:
   #     print(f'The right side of the car was damaged very little.')
   #  elif 21 <= show[1] < 41:
   #     print(f'The right side of the car was slightly damaged.   ')
   #  elif 41 <= show[1] < 61:
   #     print(f'The right side of the car was moderately damaged. ')
   #  elif 61 <= show[1] < 81:
   #     print(f'The right side of the car was damaged a lot.      ')
   #  else:
   #     print(f'The right side of the car was severely damaged.   ')
  