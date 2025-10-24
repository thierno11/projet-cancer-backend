
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms



class DoubleConv(torch.nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.conv = torch.nn.Sequential(
            torch.nn.Conv2d(in_ch, out_ch, 3, padding=1),
            torch.nn.BatchNorm2d(out_ch),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(out_ch, out_ch, 3, padding=1),
            torch.nn.BatchNorm2d(out_ch),
            torch.nn.ReLU(inplace=True)
        )
    def forward(self,x):
        return self.conv(x)

class UNetLight(torch.nn.Module):
    def __init__(self, in_channels=1, out_channels=1, features=[32,64,128,256]):
        super().__init__()
        self.downs = torch.nn.ModuleList()
        self.ups = torch.nn.ModuleList()
        self.pool = torch.nn.MaxPool2d(2)

        for f in features:
            self.downs.append(DoubleConv(in_channels,f))
            in_channels = f

        self.bottleneck = DoubleConv(features[-1], features[-1]*2)

        for f in reversed(features):
            self.ups.append(torch.nn.ConvTranspose2d(f*2,f,2,2))
            self.ups.append(DoubleConv(f*2,f))

        self.final_conv = torch.nn.Conv2d(features[0], out_channels,1)

    def forward(self,x):
        skip = []
        for down in self.downs:
            x = down(x)
            skip.append(x)
            x = self.pool(x)
        x = self.bottleneck(x)
        skip = skip[::-1]
        for i in range(0,len(self.ups),2):
            x = self.ups[i](x)
            s = skip[i//2]
            if x.shape!=s.shape:
                x = F.interpolate(x, size=s.shape[2:])
            x = torch.cat([s,x],1)
            x = self.ups[i+1](x)
        return torch.sigmoid(self.final_conv(x))







device = torch.device("cpu")
model = UNetLight().to(device)
model.load_state_dict(torch.load("unet_mammo_cpu.pth", map_location=device))
model.eval()