# import imp
# import os
import torch
import torch.nn as nn
# import torch.optim as optim
# import torch.nn.functional as F
# from torchvision import transforms, datasets

from game import BOARD_LENGTH

USE_CUDA = torch.cuda.is_available()
DEVICE = torch.device('cuda' if USE_CUDA else 'cpu')

KERNEL_SIZE = 128
RESIDUAL_BLOCK_NUM = 16
OUTPUT_SIZE = BOARD_LENGTH * BOARD_LENGTH

class ResidualBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(2, 8, kernel_size=3, padding='same', bias=False)
        self.rb = nn.Sequential(
        )