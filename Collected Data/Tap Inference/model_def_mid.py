import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=5, stride=1, padding=2, pool_size=2, pool_stride=2, isBn = True):
        super(ConvBlock, self).__init__()
        self.isBn = isBn
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size, stride, padding)
        self.bn = nn.BatchNorm1d(out_channels)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool1d(pool_size, pool_stride) # len = ceil((len - kernel_size + 1) / stride)

    def forward(self, x):
        x = self.conv(x)
        if self.isBn:
            x = self.bn(x)
        x = self.relu(x)
        x = self.pool(x)
        return x

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.layer1 = ConvBlock(6, 32)
        self.layer2 = ConvBlock(32, 64) #, pool_size=1, pool_stride=1, isBn=False)
        self.layer3 = ConvBlock(64, 128) #, pool_size=1, pool_stride=1, isBn=False)
        self.layer4 = ConvBlock(128, 256) #, pool_size=1, pool_stride=1)
        self.layer5 = ConvBlock(256, 512)
        self.layer6 = ConvBlock(256, 512)
        self.layer7 = ConvBlock(512, 1024, pool_size=1, pool_stride=1, isBn=True)
        self.layer8 = ConvBlock(1024, 512, pool_size=1, pool_stride=1, isBn=True)
        self.layer12 = ConvBlock(512, 256)

        self.fc1 = nn.Linear(7936, 512)
        self.dropout1 = nn.Dropout(0.51)
        self.fc2 = nn.Linear(512, 64)
        self.fc3 = nn.Linear(64, 2)

    def forward(self, x):
        # print(x.shape)
        x = self.layer1(x)
        # print(x.shape)
        x = self.layer2(x)
        # print(x.shape)
        x = self.layer3(x)
        # print(x.shape)
        x = self.layer4(x)
        # print(x.shape)
        x = self.layer5(x)
        # print(x.shape)
        x = self.layer12(x)
        # x = self.layer10(x)
        # print(x.shape)
        x = torch.flatten(x, 1)
        # print(x.shape)
    
        x = F.relu(self.fc1(x))
        x = self.dropout1(x)
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def test_model():
    test_input = torch.rand(1, 6, 2000)
    model = Net()
    output = model(test_input)

    print("Input shape:", test_input.shape)
    print("Output shape:", output.shape)

if __name__ == "__main__":
    test_model()
