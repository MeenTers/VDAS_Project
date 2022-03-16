import json
import argparse
import os

def updata_json(size,dist,ele,azim,obj,path):
    data = open("params_car.json", "r")
    json_object = json.load(data)
    data.close()
    json_object["image_size"]  = size
    json_object["camera_dist"] = dist
    json_object["elevation"]   = ele
    json_object["azim_angle"]  = azim
    json_object["obj_filename"] = obj
    json_object["path"] = path
    data = open("params_car.json", "w")
    json.dump(json_object, data)
    data.close()

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='test json ')
    parser.add_argument(
        '--size',
        type=int,
        default=512,
        help='value of image size ')
    parser.add_argument(
        '--dist',
        type=int,
        default=5,
        help='value of camera distance  ')
    parser.add_argument(
        '--ele',
        type=list,
        default=[0],
        help='value of elevation  ')
    parser.add_argument(
        '--azim',
        type=list,
        default=[0,90,180,270],
        help='value of azim_angle  ')
    parser.add_argument(
        '--obj',
        type=str,
        help='path to object file ')
        
    parser.add_argument(
        '--path',
        type=str,
        help='path to images file ')
        
    args = parser.parse_args()
    size = args.size
    dist = args.dist
    ele  = args.ele
    azim = args.azim
    path = os.path.join('static/images/data/'+str(args.path)+'/'+str(args.obj)+'/'+str(args.obj))
    obj  = os.path.join('file/'+str(args.obj)+'/'+str(args.obj)+'.obj')
    updata_json(size,dist,ele,azim,obj,path)