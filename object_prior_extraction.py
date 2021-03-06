import json
import numpy as np
import pickle
import copy
import os
import os.path as osp


def save_obj(obj, filename):
    with open(filename + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(filename):
    with open(filename + '.pkl', 'rb') as f:
        return pickle.load(f)


relevant_classes = [u'__background__',u'field', u'zebra', u'sky', u'track', u'train', u'window', u'pole', u'windshield', u'background', u'tree', u'door', u'sheep', u'paint', u'grass', u'baby', u'ear', u'leg', u'eye', u'tail', u'head', u'nose', u'skateboarder', u'arm', u'foot', u'skateboard', u'wheel', u'hand', u'ramp', u'man', u'jeans', u'shirt', u'sneaker', u'writing', u'hydrant', u'cap', u'chain', u'sidewalk', u'curb', u'road', u'line', u'bush', u'sign', u'people', u'car', u'edge', u'bus', u'tire', u'lady', u'letter', u'leaf', u'boy', u'pocket', u'backpack', u'bottle', u'suitcase', u'word', u'ground', u'handle', u'strap', u'jacket', u'motorcycle', u'bicycle', u'truck', u'cloud', u'kite', u'pants', u'beach', u'woman', u'rock', u'dress', u'dog', u'building', u'frisbee', u'shoe', u'plant', u'pot', u'hair', u'face', u'shorts', u'stripe', u'bench', u'flower', u'cat', u'post', u'container', u'house', u'ceiling', u'seat', u'back', u'graffiti', u'paper', u'hat', u'tennisracket', u'tennisplayer', u'wall', u'logo', u'girl', u'clock', u'brick', u'white', u'elephant', u'mirror', u'bird', u'glove', u'oven', u'area', u'sticker', u'flag', u'surfboard', u'wetsuit', u'shadow', u'sleeve', u'tenniscourt', u'surface', u'finger', u'string', u'plane', u'wing', u'umbrella', u'snow', u'sunglasses', u'boot', u'coat', u'skipole', u'ski', u'skier', u'black', u'player', u'sock', u'racket', u'wrist', u'band', u'ball', u'light', u'shelf', u'stand', u'vase', u'horse', u'number', u'rug', u'goggles', u'snowboard', u'computer', u'screen', u'button', u'glass', u'bracelet', u'cellphone', u'mountain', u'phone', u'hill', u'fence', u'stone', u'cow', u'tag', u'bear', u'table', u'water', u'ocean', u'trashcan', u'circle', u'river', u'railing', u'design', u'bowl', u'food', u'spoon', u'tablecloth', u'plate', u'bread', u'tomato', u'kid', u'sand', u'dirt', u'mouth', u'hole', u'air', u'distance', u'board', u'feet', u'suit', u'wave', u'guy', u'reflection', u'bathroom', u'toilet', u'sink', u'faucet', u'floor', u'toiletpaper', u'towel', u'sandwich', u'knife', u'bolt', u'boat', u'engine', u'trafficlight', u'wine', u'cup', u'stem', u'base', u'top', u'bottom', u'sofa', u'counter', u'photo', u'frame', u'side', u'paw', u'branch', u'fur', u'forest', u'wire', u'headlight', u'rail', u'front', u'green', u'helmet', u'whiskers', u'pen', u'neck', u'net', u'necklace', u'duck', u'sweater', u'chair', u'horn', u'giraffe', u'spot', u'mane', u'airplane', u'beard', u'speaker', u'sun', u'shore', u'pillar', u'tower', u'jet', u'gravel', u'sauce', u'fork', u'tray', u'awning', u'tent', u'bun', u'teeth', u'camera', u'tile', u'lid', u'kitchen', u'curtain', u'drawer', u'knob', u'box', u'outlet', u'remote', u'couch', u'tie', u'book', u'ring', u'toothbrush', u'balcony', u'stairs', u'doorway', u'stopsign', u'bed', u'pillow', u'corner', u'trim', u'vegetable', u'orange', u'broccoli', u'rope', u'streetlight', u'name', u'pitcher', u'uniform', u'body', u'mouse', u'keyboard', u'desk', u'monitor', u'statue', u'collar', u'candle', u'animal', u'tv', u'donut', u'apple', u'child', u'licenseplate', u'catcher', u'umpire', u'banner', u'bat', u'batter', u'part', u'hotdog', u'object', u'cake', u'bridge', u'patch', u'belt', u'park', u'stick', u'bucket', u'runway', u'lamp', u'tip', u'carpet', u'blanket', u'cover', u'napkin', u'theoutdoors', u'stove', u'pizza', u'cheese', u'crust', u'van', u'beak', u'cord', u'poster', u'purse', u'laptop', u'shoulder', u'dish', u'can', u'pipe', u'key', u'arrow', u'surfer', u'controller', u'blinds', u'bluesky', u'whiteclouds', u'luggage', u'vehicle', u'streetsign', u'pan', u'baseball', u'baseballplayer', u'jersey', u'rack', u'cabinet', u'meat', u'watch', u'refrigerator', u'vest', u'skirt', u'hoof', u'label', u'teddybear', u'fridge', u'snowboarder', u'scarf', u'basket', u'cloth', u'shade', u'blue', u'spectator', u'knee', u'column', u'metal', u'steps', u'firehydrant', u'platform', u'jar', u'fruit', u'hood', u't-shirt', u'cone', u'weeds', u'treetrunk', u'room', u'red', u'television', u'scissors', u'gate', u'tennisball', u'court', u'log', u'star', u'lettuce', u'traincar', u'microwave', u'pepperoni', u'onion', u'chimney', u'concrete', u'mug', u'carrot', u'banana', u'cart', u'wood', u'bar', u'ripples', u'holder', u'pepper', u'tusk']
relevant_classes_ = copy.copy(relevant_classes)
print('Before filtering: ' + str(len(relevant_classes)))
print('After filtering: ' + str(len(relevant_classes)))

ind2key = {idx: item for idx, item in enumerate(relevant_classes)}
key2ind = {item: idx for idx, item in enumerate(relevant_classes)}
try:
    os.makedirs(osp.join('model', 'prior', 'preprocessed'))
except:
    pass
file = open('model/prior/raw/relationships.json').read()

data = json.loads(file)
print("Reading JSON completed!!")

joint_probability = np.zeros((len(relevant_classes), len(relevant_classes)))

i = 0
for datum in data:
    i += 1
    if i % 1000 == 0:
        print(str(i) + "th point processing")

    relations = datum['relationships']
    for rel in relations:
        obj, sub = rel['object']['name'], rel['subject']['name']

        if obj in relevant_classes and sub in relevant_classes:
            joint_probability[key2ind[obj], key2ind[sub]] += 1
            joint_probability[key2ind[sub], key2ind[obj]] += 1

save_obj(joint_probability, "model/prior/preprocessed/object_prior_prob")
save_obj(ind2key, "model/prior/preprocessed/object_prior_ind2key")
save_obj(key2ind, "model/prior/preprocessed/object_prior_key2ind")
