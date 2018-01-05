import torch.nn as nn
import torch.nn.init as init

from move_translator import TOTAL_MOVES
from state_generator import BOARD_SIZE


class ChessEngine(nn.Module):
    def __init__(
        self,
        in_channels,
        out_channels,
        hidden_conv_layers,
        batch_norm=False
    ):
        super(ChessEngine, self).__init__()
        self.batch_norm = batch_norm
        self.conv1 = self.create_conv_layer(
            in_channels,
            out_channels,
            5,
            padding=4
        )
        self.hidden_conv_layers = nn.Sequential(*(self.create_conv_layer(
            out_channels,
            out_channels,
            3,
            padding=2
        ) for _ in range(hidden_conv_layers)))
        self.fc = nn.Linear(BOARD_SIZE[0] * BOARD_SIZE[1], TOTAL_MOVES)
        self.softmax = nn.SoftMax()
        self.initialize_weights()

    def initialize_weights(self):
        for m in self.modules():
            if type(m) in (nn.Conv2d, nn.BatchNorm2d, nn.Linear):
                init.kaiming_normal(m.weight)
                m.bias.data.zero_()

    def create_conv_layer(self, *args, **kwargs):
        layers = [nn.Conv2d(*args, **kwargs)]
        if self.batch_norm:
            layers.append(nn.BatchNorm2d(args[1]))
        layers.append(nn.ReLU())
        return nn.Sequential(*layers)

    def forward(self, x):
        # x.shape = (batch_size, in_channels, 8, 8)
        x = self.conv1(x)
        x = self.hidden_conv_layers(x)
        x = self.fc(x)
        return self.softmax(x)
