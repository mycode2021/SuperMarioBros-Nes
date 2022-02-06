from torch.nn import Conv2d, ReLU, Linear
import torch.nn as nn
import numpy as np


class PPO(nn.Module):
    def __init__(self, num_inputs, num_actions):
        super(PPO, self).__init__()
        self.num_input, self.channels, self.kernel, self.stride, self.padding = num_inputs, 32, 3, 2, 1
        self.fc = 32 * 6 * 6
        self.conv0 = Conv2d(out_channels=self.channels, 
                            kernel_size=self.kernel, 
                            stride=self.stride, 
                            padding=self.padding, 
                            dilation=[1, 1], 
                            groups=1, 
                            in_channels=num_inputs)
        self.relu0 = ReLU()
        self.conv1 = Conv2d(out_channels=self.channels, 
                            kernel_size=self.kernel, 
                            stride=self.stride, 
                            padding=self.padding, 
                            dilation=[1, 1], 
                            groups=1, 
                            in_channels=self.channels)
        self.relu1 = ReLU()
        self.conv2 = Conv2d(out_channels=self.channels, 
                            kernel_size=self.kernel, 
                            stride=self.stride, 
                            padding=self.padding, 
                            dilation=[1, 1], 
                            groups=1, 
                            in_channels=self.channels)
        self.relu2 = ReLU()
        self.conv3 = Conv2d(out_channels=self.channels, 
                            kernel_size=self.kernel, 
                            stride=self.stride, 
                            padding=self.padding, 
                            dilation=[1, 1], 
                            groups=1, 
                            in_channels=self.channels)
        self.relu3 = ReLU()
        self.linear0 = Linear(in_features=int(self.fc), out_features=512)
        self.linear1 = Linear(in_features=512, out_features=num_actions)
        self.linear2 = Linear(in_features=512, out_features=1)
        self._initialize_weights()

    def _initialize_weights(self):
        for module in self.modules():
            if isinstance(module, nn.Conv2d) or isinstance(module, nn.Linear):
                nn.init.orthogonal_(module.weight, nn.init.calculate_gain('relu'))
                nn.init.xavier_uniform_(module.weight)
                # nn.init.kaiming_uniform_(module.weight)
                nn.init.constant_(module.bias, 0)
    
    def forward(self, x):
        x = self.relu0(self.conv0(x))
        x = self.relu1(self.conv1(x))
        x = self.relu2(self.conv2(x))
        x = self.relu3(self.conv3(x))
        x = self.linear0(x.reshape([x.shape[0], -1]))
        return self.linear1(x), self.linear2(x)
