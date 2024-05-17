"""
This file contains the implementation for calculating Gradient by Backpropagation in Pytorch - NolanM - 2024-05-15

Backpropagation is a technique used to calculate the gradient of the loss function with respect to the weights of
the model. The backpropagation algorithm is used to update the weights of the model in order to minimize
the loss function. The backpropagation algorithm uses the chain rule to calculate the gradient of the
loss function with respect to the weights of the model.

For example: We have simple concepts: we have 2 operations a and b
- function a take input x and output y
- function b take input y and output z
- function c take input z and output w...

    d(y)/d(x) *  d(z)/d(y) = d(z)/d(x)
       |            |           |
x -> a(x) --y--> b(y) --z--> c(z)

When we want to minimize c we have to know the relative of c respect to x
We have chain rule:
d(z)/d(y) * d(y)/d(x) = d(z)/d(x)

Computational Graph:
For every operation, we have a computational graph that represents the operation and the gradient of the operation.
The graph where the nodes represent the operations and the edges represent the gradient of the operation.

x: input
        \
         f(x. y) --z--> ...-> (Loss) at the end we want to minimize
        |
y: input

We can calculate the local gradient
1. The local Gradient respect to x: d(f)/d(x) = d(x.y)/d(x) = y
2. The local Gradient respect to y: d(f)/d(y) = d(x.y)/d(y) = x
Final we know the d(Loss)/d(z) so we can calculate the d(Loss)/d(x) = d(Loss)/d(z) * d(z)/d(x)

Backpropagation Algorithm:
1. Forward pass: Calculate the output of the model (Compute the loss)
2. Compute local gradients: Calculate the local gradient in each node
3. Backward pass: Calculate the gradient of the loss function with respect to the weights of the
model using the chain rule
4. Update the weights of the model using the gradient of the loss function
5. Repeat the process until the loss function converges

For example: We have a linear function y = wx
y = wx                  # w is the weight
Loss = (y - y_hat)^2    # y_hat is the predicted value

x: input
        \
         wx --y--> Loss = (y - y_hat)^2 = (y - (wx + b))^2
        |
w: weight

We want to minimize the Loss function, so we need to calculate the d(Loss)/d(w)
First, we do Forward pass: Calculate the output of the model (Compute the loss)
Second, we calculate the local gradient in each node
Third, we do Backward pass: Calculate the gradient of the loss function with respect to the weights of the model

The Backward pass:

d(Loss)/d(w) <- d(Loss)/d(y) * d(y)/d(w)
             = 2(y - y_hat) * x

"""

import torch

# Create a tensor with requires_grad=True
x = torch.tensor(1.0)
y = torch.tensor(2.0)

w = torch.tensor(1.0, requires_grad=True)

# Forward pass and compute the loss
y_hat = w * x
loss = (y_hat - y) ** 2
print(loss)

# Backward pass
loss.backward()
print(w.grad)

# Update the weights of the model
# next forward and backward pass
