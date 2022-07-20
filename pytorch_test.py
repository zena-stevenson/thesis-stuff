from __future__ import print_function
import torch
#x = torch.rand(5, 3)
#print(x)
x = torch.empty(5, 3)
x = torch.ones_like(x)
y = torch.randn_like(x)
result = torch.empty_like(x)

#torch.add(x, y, out=result)
result = y.add(x)

print (result)
