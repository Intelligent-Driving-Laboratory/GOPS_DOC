# Model Predictive Control (MPC) Module

An optimal controller based on MPC is implemented in GOPS to offer a baseline for comparing different algorithms. This module provides simple but also flexible interfaces for other modules to call. The current version offers the following features:
- nonlinear model predictive control
- support for environment models implemented in PyTorch, compatible to the existed GOPS codes
- support for two solving methods: direct collocation and direct shooting
- user-assigned control interval for move blocking strategy
- support for passing user-defined functions as terminal cost (including neural networks)
- specifiable discounting factor that enables a unified problem formulation with RL community
- flexible optimization options for tuning

We adopt [IPOPT (Interior Point Optimizer)](https://coin-or.github.io/Ipopt), an open source software package for large-scale nonlinear optimization, to solve the nonlinear programming problem constructed at each timestep.

This page illustrates the meaning of the parameters for instantiating a `gops.sys_simulator.opt_controller.OptController` class.

## Parameters

- `model` (`gops.env.env_ocp.pyth_base_model.PythBaseModel`): model of the environment to work on
- `num_pred_step` (int): Total steps of prediction, specifying how far to look into the future.
- `ctrl_interval` (Optional[int]): Optimal control inputs are computed every `ctrl_interval` steps. For example, if `num_pred_step` equals 10, and `ctrl_interval` equals 2, then control inputs will be computed at timestep 0, 2, 4, 6 and 8. Control inputs at rest timesteps are set in a zero-order holder manner. Default to `1`.
:::{note}
`ctrl_interval` should be a factor of `num_pred_step`.
:::
- `gamma` (Optional[int]): Discounting factor. Valid range: [0, 1]. Default to `1.0`.
- `use_terminal_cost` (Optional[bool]): Whether to use terminal cost. Default to `False`.
- `terminal_cost` (Optional[Callable[[torch.Tensor], torch.Tensor]]): Self-defined terminal cost function returning a Tensor of shape [] (scalar). If `use_terminal_cost` is `True` and `terminal_cost` is `None`, `OptController` will use default terminal cost function of the environment model (if exists). Default to `None`.
- `minimize_options` (Optional[dict]): Options for minimizing to be passed to IPOPT. See [IPOPT Options](https://coin-or.github.io/Ipopt/OPTIONS.html) for details. Default to `None`.
- `verbose` (Optional[int]): Whether to print summary statistics. Valid value: {0, 1}. Default to `0`.
- `mode` (Optional[str]): Specify the method to be used to solve optimal control problem. Valid value: {"shooting", "collocation"}. Default to `"collocation"`.

## Usage
The MPC controller is meant to be used by a `gops.sys_simulator.sys_run.PolicyRunner`, for offering an optimal baseline while simulating trained policies. See [Simulation Configuration](./simulation.md) for details.