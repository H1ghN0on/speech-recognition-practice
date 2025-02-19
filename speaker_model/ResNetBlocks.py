# The script creates different ResNet blocks


# Import of modules
import torch
import torch.nn as nn


def conv3x3(in_planes, out_planes, stride=1, groups=1, dilation=1):
    # 3x3 convolution with padding

    return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride, padding=dilation, groups=groups, bias=False, dilation=dilation)


def conv1x1(in_planes, out_planes, stride=1):
    # 1x1 convolution
    
    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False)

# Обычный блок ResNet
# слой свертки 3x3
# batch-нормализация
# ReLU
# x
class BasicBlock(nn.Module):
    # Create basic ResNet block

    expansion = 1 # во сколько матрица расширяется / сжимается после прохождения блока

    def __init__(self, inplanes, planes, stride=1, downsample=None, dilation=1, norm_layer=None, activation=nn.ReLU):
        
        super(BasicBlock, self).__init__()

        if norm_layer is None:
            norm_layer = nn.BatchNorm2d

        # Both self.conv1 and self.downsample layers downsample the input when stride != 1
        self.conv1      = conv3x3(inplanes, planes, stride)
        self.bn1        = norm_layer(planes)
        self.relu       = activation(inplace=True)
        self.conv2      = conv3x3(planes, planes)
        self.bn2        = norm_layer(planes)
        self.downsample = downsample
        self.stride     = stride

    def forward(self, x):
        
        identity = x
        
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out

# Боттлнэк ResNet
# слой свертки 1x1
# batch-нормализация
# ReLU
# слой свертки 3x3
# batch-нормализация
# ReLU
# слой свертки 1x1
# batch-нормализация
# ReLU
class Bottleneck(nn.Module):
    # Create bottleneck ResNet block

    expansion = 4 # во сколько матрица расширяется / сжимается после прохождения блока

    def __init__(self, inplanes, planes, stride=1, downsample=None, groups=1, base_width=64, dilation=1, norm_layer=None, activation=nn.ReLU):
        
        super(Bottleneck, self).__init__()
        
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        
        width = int(planes*(base_width/64.))*groups
        
        # Both self.conv2 and self.downsample layers downsample the input when stride != 1
        self.conv1      = conv1x1(inplanes, width)
        self.bn1        = norm_layer(width)
        self.conv2      = conv3x3(width, width, stride, groups, dilation)
        self.bn2        = norm_layer(width)
        self.conv3      = conv1x1(width, planes*self.expansion)
        self.bn3        = norm_layer(planes*self.expansion)
        self.relu       = activation(inplace=True)
        self.downsample = downsample
        self.stride     = stride

    def forward(self, x):
        
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out