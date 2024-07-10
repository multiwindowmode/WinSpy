import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

sys.path.append(os.path.abspath('.'))
batch_size = 64
max_class = 4
# input_length = 500
input_length = 400
# input_length = 300
epochs = 400

folder_path = os.path.join(".", "inner_app_data", "inner_app_chat_background")
# folder_path = os.path.join(".", "inner_app_data", "inner_app_chat_res")
filename = os.path.join(folder_path, f"data_by_random_selection.csv")

df = pd.read_csv(filename)
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

def min_num_reserve(X, y):
    unique, counts = np.unique(y, return_counts=True)
    class_counts = dict(zip(unique, counts))
    min_class_count = min(class_counts.values())
    
    X_balanced = []
    y_balanced = []
    for class_label in class_counts.keys():
        class_indices = np.where(y == class_label)[0]
        if len(class_indices) > min_class_count:
            class_indices = np.random.choice(class_indices, min_class_count, replace=False)
        else:
            class_indices = np.random.choice(class_indices, min_class_count, replace=True)
        
        X_balanced.extend(X[class_indices])
        y_balanced.extend(y[class_indices])
    X_balanced = np.array(X_balanced)
    y_balanced = np.array(y_balanced)
    
    return X_balanced, y_balanced

for i in range(len(y)):
    # def map_to_num_label(s):
    #     w = {"VoiceSwipeAt": 1, 
    #         "CameraSwipeAt": 2,
    #         "MsgBoxClickAt": 3,
    #         "other": 0}
        
    #     return w[s]
    def map_to_num_label(s):
        w = {"VoiceSwipeAt": 0, 
            "CameraSwipeAt": 1,
            "MsgBoxClickAt": 2,
            "other": 3}
        
        return w[s]
    y[i] = map_to_num_label(y[i])

y = np.array(y, dtype=np.int64)

X, y = min_num_reserve(X, y)

print(y.shape, type(y[0]))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

train_indices = (y_train >= 0) & (y_train < max_class)
test_indices = (y_test >= 0) & (y_test < max_class)

X_train = X_train[train_indices]
y_train = y_train[train_indices]

X_test = X_test[test_indices]
y_test = y_test[test_indices]

# print("X_train shape:", X_train.shape)
# print("X_test shape:", X_test.shape)
# print("y_train shape:", y_train.shape)
# print("y_test shape:", y_test.shape)

import torch
import torch.nn as nn
import torch.nn.functional as F

# from process_data_pair.net1800.net_v1 import Simple1DCNN
from process_data_pair.net200.net_stablema import Simple1DCNN

# model = OptimizedSimple1DCNN(num_classes=max_class, input_length=1800)
model = Simple1DCNN(num_classes = max_class, input_length=input_length)
# print(model)

from torch.utils.data import TensorDataset, DataLoader

X_train_tensor = torch.Tensor(X_train).unsqueeze(1)  # Shape: [n_samples, channels, seq_len]

X_test_tensor = torch.Tensor(X_test).unsqueeze(1)
y_train_tensor = torch.LongTensor(y_train)
y_test_tensor = torch.LongTensor(y_test)


train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

def show_test_acc(is_detail):
    correct_pred = {classname: 0 for classname in range(max_class)}
    total_pred = {classname: 0 for classname in range(max_class)}
    model.eval()
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predictions = torch.max(outputs, 1)
            for label, prediction in zip(labels, predictions):
                if label == prediction:
                    correct_pred[label.item()] += 1
                total_pred[label.item()] += 1
    
    accuracy_list = []

    for classname, correct_count in correct_pred.items():
        accuracy = 100 * float(correct_count) / (total_pred[classname] + 0.001)
        accuracy_list.append(accuracy)
        if is_detail:
            print(f"Accuracy for class {classname} is: {accuracy:.2f}%")

    avg_accuracy = sum(accuracy_list) / len(accuracy_list)
    print(f"avg accuracy: {avg_accuracy:.2f}%, {str(accuracy_list)}")
    return min(accuracy_list)


def show_test_metrics():
    # dict for TP, FP, TN, FN
    class_metrics = {
        0: {"TP": 0, "FP": 0, "TN": 0, "FN": 0},
        1: {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
    }

    model.eval()
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predictions = torch.max(outputs, 1)
            for label, prediction in zip(labels, predictions):
                if label == 0:
                    if prediction == 0:
                        class_metrics[0]["TP"] += 1
                        class_metrics[1]["TN"] += 1
                    else:
                        class_metrics[0]["FN"] += 1
                        class_metrics[1]["FP"] += 1
                elif label == 1:
                    if prediction == 1:
                        class_metrics[1]["TP"] += 1
                        class_metrics[0]["TN"] += 1
                    else:
                        class_metrics[1]["FN"] += 1
                        class_metrics[0]["FP"] += 1

    for classname, metrics in class_metrics.items():
        print(f"Metrics for class {classname}:")
        print(f"  True Positives: {metrics['TP']}")
        print(f"  False Positives: {metrics['FP']}")
        print(f"  True Negatives: {metrics['TN']}")
        print(f"  False Negatives: {metrics['FN']}")
        TP = metrics['TP']
        FP = metrics['FP']
        TN = metrics['TN']
        FN = metrics['FN']

        accuracy = (TP + TN) / (TP + TN + FP + FN) # ACC
        precision = TP / (TP + FP) # PPV
        recall = TP / (TP + FN) # TPR
        specificity = TN / (TN + FP) # TNR
        npv = TN / (TN + FN) # NPV

        print(f"{100 * accuracy:.1f}\\%")
        print(f"{100 * precision:.1f}\\%")
        print(f"{100 * recall:.1f}\\%")
        print(f"{100 * specificity:.1f}\\%")
        print(f"{100 * npv:.1f}\\%")

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
# for epoch in range(epochs):
#     model.train()
#     total_loss = 0
#     for inputs, labels in train_loader:
#         inputs, labels = inputs.to(device), labels.to(device)
#         optimizer.zero_grad()
#         outputs = model(inputs)
#         loss = criterion(outputs, labels)
#         loss.backward()
#         optimizer.step()
#         total_loss += loss.item()

for epoch in range(epochs):
    model.train()
    total_loss = 0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader)}")
    # show_test_metrics()
    if show_test_acc(0) > 98:
        break


model.eval()
show_test_acc(1)
show_test_metrics()