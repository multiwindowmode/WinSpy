import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import torch
import random

sys.path.append(os.path.abspath('.'))

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

def gogo(data_file, batch_size, max_class = 7, input_length = 500, epochs = 50):
    # folder_path = os.path.join(".", "inner_app_data", "inner_app_pay_res")
    folder_path = os.path.join(".", "inner_app_data", "inner_app_pay_background")
    # filename = os.path.join(folder_path, f"data_{data_file}.csv")
    filename = os.path.join(folder_path, f"data.csv")

    df = pd.read_csv(filename)

    X = df.iloc[:, :-1].values
    print(X.shape)

    def map_string_to_int(s):
        if s == "tapConfirmRechargeAt":
            return 0
        elif s == "tapConfirmWithdrawalAt":
            return 1
        elif s == "other":
            return 2
        else:
            assert 0

    df.iloc[:, -1] = df.iloc[:, -1].apply(map_string_to_int).astype(int)

    y = df.iloc[:, -1].values
    y = np.array(y, dtype=np.int64)

    X, y = min_num_reserve(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=31)

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

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    def ev():
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

        w = []

        for classname, correct_count in correct_pred.items():
            accuracy = 100 * float(correct_count) / (total_pred[classname] + 0.001)
            w.append(accuracy)
            print(f"Accuracy for class {classname} is: {accuracy:.2f}%")

        print(f"Overall average accuracy is: {(w[0]+w[1])/2:.2f}%")

    def traiN():
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
        if random.randint(0, 9) >= 7:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader)}")


    for epoch in range(epochs):
        for i in range(10):
            traiN()
        ev()


if __name__ == "__main__":
    data_file = "tapConfirmRechargeAt"
    # data_file = "tapConfirmWithdrawalAt
    batch_size = 64
    max_class = 2
    input_length = 400
    epochs = 30
    gogo(data_file, batch_size, max_class, input_length, epochs)
