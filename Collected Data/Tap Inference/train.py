import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import os, sys
sys.path.append(".")

# from model_6_2000.model_def_small import Net
# from model_6_2000.model_def_mid import Net
# from model_6_2000.model_def_mid import Net
from train111.model_6_2000.model_def_mid import Net

import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# fcsv = "collected_data/not_expand_desktop3_2hour/data.csv"
# ff = "collected_data/not_expand_hand"
# ff = "collected_data/not_expand_desktop3_2hour"
ff = "collected_data/expand_2h_regression"
# fcsv = "collected_data/expand_2h_regression/data.csv"
# ff =  "collected_data/mix_P30_2h_regression"
fcsv = f"./{ff}/data.csv"

data = pd.read_csv(fcsv, header=None)

features = data.iloc[:, :12000].values
labels = data.iloc[:, 12000:].values


features = torch.tensor(features, dtype=torch.float32).reshape(-1, 6, 2000).to(device) # features.shape torch.Size([4136, 6, 2000])
labels = torch.tensor(labels, dtype=torch.float32).to(device) # labels.shape torch.Size([4136, 2])

# features, labels = data_strong(features, labels)

print("features.shape", features.shape)
print("labels.shape", labels.shape)

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.25, random_state=42)
train_data = TensorDataset(X_train, y_train)
test_data = TensorDataset(X_test, y_test)

bs = 64 

train_loader = DataLoader(train_data, batch_size=bs, shuffle=True)
test_loader = DataLoader(test_data, batch_size=bs, shuffle=False)

model = Net().to(device)

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

from torch.optim.lr_scheduler import StepLR
scheduler = StepLR(optimizer, step_size=50, gamma=0.9)

# def evaluate_model():
#     model.eval()
#     total_loss = 0
#     num_batches = 0

#     with torch.no_grad():
#         for data, targets in test_loader:
#             data, targets = data.to(device), targets.to(device)
#             outputs = model(data)
#             loss = criterion(outputs, targets)

#             total_loss += loss.item()
#             num_batches += 1

#     average_loss = total_loss / num_batches
#     # print(f'Average Loss: {average_loss}')
#     return average_loss

def evaluate_model():
    model.eval()
    total_distance = 0
    total_x_distance = 0
    total_y_distance = 0
    num_samples = 0

    with torch.no_grad():
        for data, targets in test_loader:
            data, targets = data.to(device), targets.to(device)
            outputs = model(data)
   
            distance = torch.sqrt(torch.sum((outputs - targets) ** 2, dim=1))
            total_distance += distance.sum().item()

            x_distance = torch.abs(outputs[:, 0] - targets[:, 0])
            y_distance = torch.abs(outputs[:, 1] - targets[:, 1])
            total_x_distance += x_distance.sum().item()
            total_y_distance += y_distance.sum().item()
            num_samples += targets.size(0)

    average_distance = total_distance / num_samples
    average_x_distance = total_x_distance / num_samples
    average_y_distance = total_y_distance / num_samples
    
    return average_distance, average_x_distance, average_y_distance

def train_model(num_epochs):
    model.train()
    for epoch in range(num_epochs):
        for data, targets in train_loader: # data: [batch_size, 6, 2000], targets: [batch_size, 2]
            data, targets = data.to(device), targets.to(device)
            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

        scheduler.step()
        epoch_i = epoch + 1
        xue = optimizer.param_groups[0]['lr']

        xy, x, y = evaluate_model()

        print(f'{xue:020f}, Epoch {epoch_i:03d}, Loss: {loss.item():020f}, in test:  {xy:1f} {x:1f} {y:1f}')
        model.train()

        # lo = int(loss.item())
        # if lo <= 5000:
        #     torch.save(model.state_dict(), f"train111/model_hand_{epoch_i}_{lo:07d}.pth")
        #     break


def evaluate_model_to_file(id):
    w = []
    model.eval()
    total_loss = 0
    num_batches = 0
    results = []  # List to store predictions and possibly the targets

    with torch.no_grad():
        for data, targets in test_loader:
            data, targets = data.to(device), targets.to(device)
            outputs = model(data)
            loss = criterion(outputs, targets)
            total_loss += loss.item()
            num_batches += 1

            outputs = outputs.cpu()  # Move outputs to CPU for processing if necessary
            targets = targets.cpu()  # Move targets to CPU for processing if necessary

            # Assuming each output and target is in the format [batch_size, 2]
            for out, tgt in zip(outputs, targets):
                predicted = out.tolist()  # Convert tensor to list                
                true_label = tgt.tolist()  # Convert tensor to list
                results.append((true_label, predicted))

                w.append([])
                w[-1] += predicted
                w[-1] += true_label

    # Write results to a file
    with open(f"{ff}/res_{id}_pos_compare.txt", "w") as f:
        for true, pred in results:
            f.write(f"True labels: {true}, Predicted labels: {pred}\n")

    average_loss = total_loss / num_batches
    return w, average_loss


import matplotlib.pyplot as plt
def f(coordinates, id):
    dxs = []
    dys = []

    for (x1, y1, x2, y2) in coordinates:
        dx = x2 - x1
        dy = y2 - y1
        dxs.append(dx)
        dys.append(dy)

    plt.figure(figsize=(8, 6))
    plt.scatter(dxs, dys, color='blue')
    plt.title('Differences in Coordinates (dx, dy)')
    plt.xlabel('dx')
    plt.ylabel('dy')
    plt.grid(True)
    # plt.savefig(f"{ff}/res_{id}_dxdy.pdf", format='pdf', bbox_inches='tight')
    # plt.show()

for i in range(30):
    train_model(7)
    dxdys, _ = evaluate_model_to_file(i)
    f(dxdys, i)
