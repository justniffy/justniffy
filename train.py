# CREATE TRAINING DATA
import json
# import nltk
# nltk.download('punkt')
# import re
# import webbrowser
#from urllib.parse import urlparse
#from bs4 import BeautifulSoup
#import Dataloader as Dataloader

from nltk_utils import stem,tokenize,bag_of_words
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet
'''def make_clickable_and_open(url):
    clickable_url= f'<a href="{url}"target="_blank">{url}</a>'
    webbrowser.open(url)
    return clickable_url'''
with open('intents.json', 'r') as f:   # intent = f.read() to read the file
    intents = json.load(f) # load the json file
# Access the json data directly
'''intent = intents.get("intents",[])
# process and print the clickable urls in responses
for inten in intent:
    #print(f"Tag:{inten.get('tag','')}")
    #print("Responses: ")
    for response in inten.get('responses',[]):
        clickable_response=re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\),]|%[0-9a-fA-F][0-9a-fA-F])+',
                                  lambda x: make_clickable_and_open(x.group()), response)
        print(f"- {clickable_response}")'''




#rec_patterns = intents[2]['patterns']
#print(intents)

all_words =[]
tags =[]
xy = []
for intent in intents["intents"]:
    tag = intent["tag"]
    tags.append(tag)
    for pattern in intent["patterns"]:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))
ignore_words = ["?","!",".",","]
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))
#print(all_words)
#print(tags)

x_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    x_train.append(bag)

    label = tags.index(tag)
    y_train.append(label) # CrossEntropyLoss

x_train = np.array(x_train)
y_train = np.array(y_train)

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train
   #dataset[idx]
    def __getitem__(self, index):
        return self.x_data[index],self.y_data[index]
    
    def __len__(self):
        return self.n_samples


# Hyperparameters
batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(x_train[0])
learning_rate = 0.001
num_epochs = 1000
#print(input_size, len(all_words))
#print(output_size, tags)
dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size = batch_size,shuffle = True, num_workers =0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

#loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr =learning_rate)
for epoch in range(num_epochs):
    for(words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device, dtype=torch.int64)

        # forward
        outputs = model(words)
        loss = criterion(outputs, labels)

        # backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if(epoch + 1) % 100 == 0:
        print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')
print(f'final loss, loss={loss.item():.4f}')
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}
file = "data.pth"
torch.save(data, file)
print(f'training complete. file saved to {file}')
