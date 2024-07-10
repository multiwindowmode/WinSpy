import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

sys.path.append(os.path.abspath('.'))

# which = "./process_data_pair/honor_final_app21_web21/honor_final_web21_cpu5"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10/app21_cpu10"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10/app21_cpu10_merge12345"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10/app21_cpu10_foreach"
which = "./process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10/app21_cpu10_foreach2"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_background_app21/"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_background_web21/"
# which = "./process_data_pair/honor_final_app21_web21/honor_final_app21_cpu10/app21_cpu10_without_netacc"
# which = "./process_data_pair/compare_multi_device_mode/honor_background_cpu5"
# which = "./process_data_pair/compare_multi_device_mode/honor_background_cpu5_2"
# which = "./process_data_pair/compare_multi_device_mode/P30_background_cpu5"
# which = "./process_data_pair/compare_multi_device_mode/honor_large_app7_web7/honor_large_web7_cpu5"
filename = f"{which}/data.csv"
# filename = f"{which}/data_2.csv"
# filename = f"{which}/data_inter.csv"

epochs = 100
batch_size = 64
max_class = 21
# max_class = 7

df = pd.read_csv(filename)
X = df.iloc[:, :600].values
y = df.iloc[:, -1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)

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
from torch.utils.data import TensorDataset, DataLoader

# from process_data_pair.net1800.net_v1 import Simple1DCNN
# from process_data_pair.net1800.net_stablema_temp import Simple1DCNN
# from process_data_pair.net1800.net_stablema import Simple1DCNN
# from process_data_pair.net600.net_stablema import Simple1DCNN
from process_data_pair.net600.net_stablema2 import Simple1DCNN
# from process_data_pair.net600.net_v1 import Simple1DCNN

# model = OptimizedSimple1DCNN(num_classes=max_class, input_length=1800)
model = Simple1DCNN(num_classes=max_class)

X_train_tensor = torch.Tensor(X_train).unsqueeze(1)  # Shape: [n_samples, channels, seq_len]

print(X_train_tensor.shape)

X_test_tensor = torch.Tensor(X_test).unsqueeze(1)
y_train_tensor = torch.LongTensor(y_train)
y_test_tensor = torch.LongTensor(y_test)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
model.to(device)

def evaluate_model_accuracy():
    model.eval()
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

    accuracies = []
    for classname, correct_count in correct_pred.items():
        accuracy = 100 * float(correct_count) / (total_pred[classname] + 0.001)
        accuracies.append(accuracy)
        print(f"Accuracy for class {classname} is: {accuracy:.2f}%")

    min_accuracy = min(accuracies)
    average_accuracy = sum(accuracies) / len(accuracies)
    print(f"Minimum accuracy across classes is: {min_accuracy:.2f}%")
    print(f"Average accuracy across classes is: {average_accuracy:.2f}%")

    sum_correct_pred = sum(correct_pred.values())
    sum_total_pred = sum(total_pred.values())
    overall_accuracy = 100 * float(sum_correct_pred) / (sum_total_pred + 0.001)
    print(f"Overall average accuracy is: {overall_accuracy:.2f}%")
    print(f"Overall average accuracy is: {overall_accuracy:.2f}%", file=open(f"{which}/temp_log.txt", 'a'))

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        model.train()
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()

    print(f"Epoch {epoch + 1}/{epochs}, Loss: {running_loss / len(train_loader)}")
    evaluate_model_accuracy()
