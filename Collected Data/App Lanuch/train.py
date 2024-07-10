import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

sys.path.append(os.path.abspath('.'))
# which, data_file = "app_cmd5", "data"
# which, data_file = "app_cmd5", "data_afterinter"
# which, data_file = "app_cmd10", "data"
# which, data_file = "app_cmd15", "data"
# which, data_file = "app_cmd15", "data_afterinter"
# which, data_file = "app_cmd15", "data_testPriority"
# which, data_file = "app_cmd15", "data_testPriority_afterinter"
# which, data_file = "app_cmd15", "data_testPriority2_afterinter"

# which, data_file = "app_cpu5", "data"
# which, data_file = "app_cpu5", "data_2"
# which, data_file = "app_cpu10", "data"
# which, data_file = "app_cpu10", "data_2"
# which, data_file = "app_cpu15", "data"
# which, data_file = "app_cpu15", "data_2"

# which, data_file = "cmd5", "data"
# which, data_file = "cmd10", "data"
# which, data_file = "cmd15", "data"
# which, data_file = "cpu5", "data5"
# which, data_file = "cpu5", "data_2_trim"
# which, data_file = "cpu10", "data10"
# which, data_file = "cpu10", "data10_2"
# which, data_file = "cpu15", "data15"
# which, data_file = "cpu15", "data15_2"

# which, data_file = "background_cpu10", "data_afterinte"

# which, data_file = "app21_cpu10", "data"
# which, data_file = "honor_final_web21_cpu5", "data"

which, data_file = "honor_background_cpu5_2", "data"
# working_in_folder_path = "process_data_pair/honor_compare_cpu"
# filename = f'./process_data_pair/honor_compare_cpu/{which}/{data_file}.csv'

# working_in_folder_path = "process_data_pair/honor_compare_cpu"
# working_in_folder_path = "process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10"
working_in_folder_path = "process_data_pair/compare_multi_device_mode"
# working_in_folder_path = "process_data_pair/honor_final_app21_web21"

filename = f'./{working_in_folder_path}/{which}/{data_file}.csv'
epochs = 100
batch_size = 64
# max_class = 21
max_class = 7

df = pd.read_csv(filename)

X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)


# def transform_sequences(X, window_size=6):
#     new_seq_length = X.shape[1] // window_size

#     X_transformed = np.zeros((X.shape[0], new_seq_length))
    
#     for i in range(new_seq_length):
#         X_transformed[:, i] = X[:, i * window_size : (i + 1) * window_size].sum(axis=1)
    
#     return X_transformed
# X_train = transform_sequences(X_train)
# X_test = transform_sequences(X_test)

# print("X_train shape:", X_train.shape)
# print("X_test shape:", X_test.shape)
# print("y_train shape:", y_train.shape)
# print("y_test shape:", y_test.shape)


train_indices = (y_train >= 0) & (y_train < max_class)
test_indices = (y_test >= 0) & (y_test < max_class)

X_train = X_train[train_indices]
y_train = y_train[train_indices]

X_test = X_test[test_indices]
y_test = y_test[test_indices]

print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)

import torch
import torch.nn as nn
import torch.nn.functional as F
# from process_data_pair.net1800.net_v1 import Simple1DCNN
from process_data_pair.net1800.net_stablema import Simple1DCNN

# model = OptimizedSimple1DCNN(num_classes=max_class, input_length=1800)
model = Simple1DCNN(num_classes=max_class)
print(model)

from torch.utils.data import TensorDataset, DataLoader

X_train_tensor = torch.Tensor(X_train).unsqueeze(1)  # Shape: [n_samples, channels, seq_len]

print(X_train_tensor.shape)

X_test_tensor = torch.Tensor(X_test).unsqueeze(1)
y_train_tensor = torch.LongTensor(y_train)
y_test_tensor = torch.LongTensor(y_test)


train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader)}")

model.eval()
# correct = 0
# total = 0
# with torch.no_grad():
#     for inputs, labels in test_loader:
#         inputs, labels = inputs.to(device), labels.to(device)
#         outputs = model(inputs)
#         _, predicted = torch.max(outputs, 1)
#         total += labels.size(0)
#         correct += (predicted == labels).sum().item()

# accuracy = 100 * correct / total
# print(f"Accuracy on the test set: {accuracy:.2f}%")



correct_pred = {classname: 0 for classname in range(max_class)}
total_pred = {classname: 0 for classname in range(max_class)}


with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, predictions = torch.max(outputs, 1)

        for label, prediction in zip(labels, predictions):
            if label == prediction:
                correct_pred[label.item()] += 1
            total_pred[label.item()] += 1


for classname, correct_count in correct_pred.items():
    accuracy = 100 * float(correct_count) / (total_pred[classname] + 0.001)
    print(f"Accuracy for class {classname} is: {accuracy:.2f}%")

sum_correct_pred = sum(correct_pred.values())
sum_total_pred = sum(total_pred.values())

# Calculate overall average accuracy
overall_accuracy = 100 * float(sum_correct_pred) / (sum_total_pred + 0.001)  # Added a small number to avoid division by zero

# Print overall average accuracy
print(f"Overall average accuracy is: {overall_accuracy:.2f}%")

# python -u "e:\android_mwm_attack_projects\website_fingerprinting\python_scripts\process_data_pair\honor_compare_cpu\train.py"
