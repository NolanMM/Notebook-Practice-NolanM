"""
Note on Gradient Computation and Optimizer in Pytorch

Pytorch buult-in optimizer:
- SGD (Stochastic Gradient Descent)
- Adam (Adaptive Moment Estimation)
- RMSprop (Root Mean Square Propagation)
- Adadelta (Adaptive Delta)
- Adagrad (Adaptive Gradient Algorithm)
- Adamax (Adam with infinity norm)
- ASGD (Averaged Stochastic Gradient Descent)
- LBFGS (Limited-memory Broyden-Fletcher-Goldfarb-Shanno)
...

Optimizer helps to update the weights of the model in order to minimize the loss function. The optimizer
uses the gradient of the loss function to update the weights of the model. The optimizer uses the gradient
to update the weights of the model in the opposite direction of the gradient to minimize the loss function.

"""

import torch

weights = torch.randn(4, requires_grad=True)

optimizer = torch.optim.SGD(weights, lr=0.01)

optimizer.step()

# Note: We need to set the gradient to zero before we calculate the gradient for the next epoch
optimizer.zero_grad()

"""
Another example:

weights = torch.randn(4, requires_grad=True)

z = torch.randn(4, requires_grad=True)
z.backward()

weights.grad.zero_()

"""
