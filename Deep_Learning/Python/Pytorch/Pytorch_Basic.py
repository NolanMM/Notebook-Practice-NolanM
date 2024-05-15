"""
This file contains the basic operations of Pytorch - NolanM - 2024-05-15
"""

import torch
import numpy as np

"""
Note:
    1. Pytorch is a library for tensor computation like numpy but with strong GPU acceleration
    2. Pytorch is a deep learning research platform that provides maximum flexibility and speed
    3. Pytorch is a python package that provides two high-level features:
        - Tensor computation (like numpy) with strong GPU acceleration
        - Deep Neural Networks built on a tape-based autograd system
    
    x  = torch.ones(5, requires_grad=True) # requires_grad=True is used to track computation and tell
    pytorch to compute gradients for this tensor later during backpropagation or optimization phase
    When ever you have a variable in the model want to optimize it, you should set requires_grad=True
    because it will be used to compute the gradients 
"""


if torch.cuda.is_available():
    device = torch.device("cuda")
    # Running on GPU
    print("Running on GPU")

    print("_________________________________________________________")

    # Run on GPU
    x = torch.ones(5, 3)
    print(x)
    x = x.to(device)
    print(x)

    x = torch.ones(5, 3, device=device)
    print(x)

    y = torch.rand(5, 3)
    y = y.to(device)
    print(y)

    z = x + y
    print(z)

    # Note: If we call z.numpy() it will throw an error because numpy does not support GPU tensors we need to
    # move the tensor to CPU first
    z = z.to("cpu")
    print(z.numpy())


print("_________________________________________________________")

# Create a tensor
x = torch.tensor([5.5, 3])
print(x)

# Create a tensor with random values
x = torch.rand(5, 3)
print(x)

# Get the size of the tensor
print(x.size())

print("_________________________________________________________")
# Resizing: If you want to resize/reshape tensor, you can use torch.view
x = torch.randn(4, 4)
print(x)
y = x.view(16)
print(y)
z = x.view(-1, 8)  # the size -1 is inferred from other dimensions
print(z)
print(x.size(), y.size(), z.size())

x = torch.empty(2, 2, 2, 2, 3)
print(x)

x = torch.ones(2, 2, 3, 1)
print(x)

print("_________________________________________________________")

x = torch.ones(2,2,dtype=torch.int)     # can be int, float16, double...
print(x.dtype)
x = x.float()
print(x.dtype)

print("_________________________________________________________")

x = torch.tensor([1.0, 2.0, 3.0])
print(x)

print("_________________________________________________________")

x = torch.randn(4, 4)
print(x)
y = torch.randn(4, 4)
print(y)

z = x + y
print(z)
z = torch.add(x, y)

# Addition
y = torch.rand(5, 3)
print(x + y)

# Addition: providing an output tensor as argument
result = torch.empty(5, 3)
torch.add(x, y, out=result)
print(result)

# Addition: in-place
y.add_(x)
print(y)

# Subtraction
print(x - y)
print(torch.sub(x, y))
result = torch.empty(5, 3)
print(torch.sub(x, y, out=result))

# Multiplication
print(x * y)
print(torch.mul(x, y))
result = torch.empty(5, 3)
print(torch.mul(x, y, out=result))

# Division
print(x / y)
print(torch.div(x, y))
result = torch.empty(5, 3)
print(torch.div(x, y, out=result))

# Slicing
x = torch.randn(4, 4)
print(x)
print(x[:, 1])

print("_________________________________________________________")

# Converting to numpy to tensor
a = torch.ones(5)
print(a)
b = a.numpy()
print(b)
print(type(b))

# Add to tensor
a.add_(1)
print(a)
print(b)

# Note if you change the numpy array, the tensor will change as well (When running on CPU) and vice versa

# Converting numpy array to tensor
a = np.ones(5)
b = torch.from_numpy(a)
print(a)
print(b)

a += 1
print(a)
print(b)



