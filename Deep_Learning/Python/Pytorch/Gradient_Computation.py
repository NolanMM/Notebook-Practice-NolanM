"""
This file contains the implementation for calculating Gradient in Pytorch - NolanM - 2024-05-15

Note:
    Gradient is very important for our model optimization. It is used to update the weights of the model
    to minimize the loss function. Pytorch provides a module called autograd for automatic differentiation
    which helps us to calculate the gradient of the tensor.
    
    Gradient is the derivative of the loss function with respect to the weights of the model.
    Formula: Gradient = d(loss)/d(weights)
    
    Pytorch provides a module called autograd for automatic differentiation. It is used to calculate the
    gradient of the tensor. The autograd module keeps track of all the operations performed on the tensor
    and calculates the gradient of the tensor using the chain rule.
    
"""
import torch

"""
Important Note:

- When we do the loop for each epoch and we calculate the loss and we call the backward() function
the gradient will be accumulated in the grad attribute of the tensor (sum of the gradients has been calculated)
- So, we need to set the gradient to zero before we calculate the gradient for the next epoch when we train the model
    
    Sample wrong code:
weights = torch.randn(4, requires_grad=True)

for epoch in range(10):
    model_output = (weights * 3).sum()
    model_output.backward()
    print(weights.grad)
    
# Output:
# tensor([3., 3., 3., 3.])
# tensor([6., 6., 6., 6.])
# tensor([9., 9., 9., 9.])
# tensor([12., 12., 12., 12.])
...
    
    Sample correct code:
weights = torch.randn(4, requires_grad=True)

for epoch in range(10):
    model_output = (weights * 3).sum()
    model_output.backward()
    print(weights.grad)
    weights.grad.zero_()
    
# Output:
# tensor([3., 3., 3., 3.])
# tensor([3., 3., 3., 3.])
# tensor([3., 3., 3., 3.])
...

"""


# Create a tensor with requires_grad=True
x = torch.randn(3, requires_grad=True, dtype=torch.float32)
print(x)

y = x + 2
print(y)

"""
# Output:
    tensor([ 0.0195, -0.6111, -0.0393], requires_grad=True)
    tensor([2.0195, 1.3889, 1.9607], grad_fn=<AddBackward0>) # Because the operation is addition so called AddBackward0 
    else it could be MulBackward0 or DivBackward0 etc.
"""

z = y * y * 2
z = z.mean()
print(z)

# Calculate the gradient of z with respect to x and store it in x.grad  Formula: Gradient = d(loss)/d(weights)
z.backward()    # If the requires_grad=False it will throw an error
print(x.grad)
"""
# In background it will create a vector Jacobian product to calculate the gradient
# Formulas Jacobian Product = J * v where J is the Jacobian matrix and v is the vector
# Jacobian Matrix process sample

    Jacobian Matrix:
    x = [x1, x2, x3]
    y = [y1, y2, y3]
    z = [z1, z2, z3]
    
    z1 = x1 + x2 + x3
    z2 = x1 * x2 * x3
    z3 = x1^2 + x2^2 + x3^2
        
    J = [[dz1/dx1, dz1/dx2, dz1/dx3],
        [dz2/dx1, dz2/dx2, dz2/dx3],
        [dz3/dx1, dz3/dx2, dz3/dx3]]
            
    v = [1, 1, 1]
    
    J * v = [dz1/dx1 + dz1/dx2 + dz1/dx3, dz2/dx1 + dz2/dx2 + dz2/dx3, dz3/dx1 + dz3/dx2 + dz3/dx3]
    
    J * v = [1 + 1 + 1, x2 * x3 + x1 * x3 + x1 * x2, 2 * x1 + 2 * x2 + 2 * x3]
    
    J * v = [3, x2 * x3 + x1 * x3 + x1 * x2, 2 * x1 + 2 * x2 + 2 * x3]
"""

# We can specify the vector v in the backward() function
v = torch.tensor([0.1, 1.0, 0.001], dtype=torch.float32)
y.backward(v)
print(x.grad)

# Stop autograd from tracking history on tensors with requires_grad=True
x.requires_grad_(False)
print(x)

# or we can use the no_grad() function
with torch.no_grad():
    y = x + 2
    print(y)

# or we can use the detach() function to get a new tensor with requires_grad=False
y = x.detach()
print(y)
