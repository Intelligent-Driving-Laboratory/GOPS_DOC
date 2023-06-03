# Simulation Configuration

To test the performance of the trained models, GOPS offers a `gops.sys_simulator.sys_run.PolicyRunner` class which can automatically simulate a bunch of trained policies and visualize the results for intuitively comparing, including the reward curve, state curves and action curves, etc.

In addition, `PolicyRunner` allows comparing the trained policies with an optimal controller, for example the MPC-based optimal controller `gops.sys_simulator.opt_controller.OptController` (See [Model Predictive Control (MPC) Module](./mpc.md) for details).

This page illustrates how to use `PolicyRunner` for simulation.

## Parameters

- `log_policy_dir_list` (list): A list of strings, each representing a directory of a trained policy to be simulated.
- `trained_policy_iteration_list` (list): A list of strings indicating policy models saved at which iteration are used for simulation, each element of which specifies a saved policy model.
:::{note}
The elements of `log_policy_dir_list` and `trained_policy_iteration_list` have an one-to-one correspondence, and each pair, when joined together, leads to a specific policy model (i.e., a .pkl file). Thus, `log_policy_dir_list` and `trained_policy_iteration_list` should be of the same length. **Also note that the order matters!**
::: 
- `save_render` (bool): (Optional) Whether to save environment animation. Default to `False`.
- `plot_range` (list): (Optional) A list composed of two integrators customizing the plot range. If this is set to `[a, b]`, only time steps in :math:`[a, b]` will be plotted when visualizing the results. If `None`, the whole trajectories will be plotted. Default to `None`.
- `legend_list` (list): (Optional) A list of strings specifying legends in the result figures for each policy. Default to `None`.
:::{note}
Likewise, the elements of `legend_list` also correspond to those of `log_policy_dir_list` in an one-to-one manner. 
::: 
- `constrained_env` (bool): (Optional) A boolean indicating whether the simulating environment is a constrained environment. For example, for policies trained on the environment `gops.env.env_ocp.pyth_veh3dofconti_surrcstr_data.SimuVeh3dofcontiSurrCstr` which contains constraints, this should be set to `True`. Default to `False`.
- `is_tracking` (bool): (Optional) A boolean indicating whether the simulating environment is a tracking problem. For example, for policies trained on the environment `gops.env.env_ocp.pyth_veh3dofconti_data.SimuVeh3dofconti` where the goal is to control a vehicle following some reference paths, this should be set to `True`. Default to `False`.
- `use_dist` (bool): (Optional) A boolean indicating whether the simulating environment has adversarial actions. Default to `False`.
- `dt` (float): (Optional) Time interval between steps. If `None`, the result figures will use `Time step` for x-axis. Otherwise, the result figures will use `Time (s)` for x-axis, and the transformation from time steps to time is characterized by `dt`.
- `is_init_info` (bool): (Optional) Whether to customize initial information. Default to `False`.
- `init_info` (dict): (Optional) A dictionary specifying the initial information.
:::{note}
This parameter will be ignored if `is_init_info` is `False`. This parameter will be passed into the environment's `reset()` method. which you may want to check for supported initial information of each environment.
:::
- `use_opt` (bool): (Optional) Whether to use optimal controller for comparison. Default to `False`.
- `opt_args` (dict): (Optional) A dictionary specifying the arguments of the optimal controller. Default to `None`. See [Usage Example](#usage-example) for details.
- `obs_noise_type` (str): (Optional) Type of observation noise. Valid value: {"normal", "uniform", `None`}. If `None`, no noise is added to the observation, otherwise random noises either normally or uniformly distributed will be introduced. Default to `None`.
- `obs_noise_data` (list): (Optional) A list specifying the parameters for the noise distribution. This should contain two lists, the length of which should both equals the dimension of observations. For normally distributed noise, the first list represents the mean and the second list the standard deviation. For uniformly distributed noise, the first list represents the lower bound and the second list the upper deviation. Default to `None`.
- `action_noise_type` (str): (Optional) Type of action noise. Valid value: {"normal", "uniform", `None`}. If `None`, no noise is added to the action, otherwise random noises either normally or uniformly distributed will be introduced. Default to `None`.
- `action_noise_data` (list): (Optional) A list specifying the parameters for the noise distribution. This should contain two lists, the length of which should both equals the dimension of actions. For normally distributed noise, the first list represents the mean and the second list the standard deviation. For uniformly distributed noise, the first list represents the lower bound and the second list the upper deviation. Default to `None`.


(usage-example)=
## Usage Example
A template for using `PolicyRunner` is offered in `gops.example_run.template_run_environ_alg.py`, showing the possible setting of all the parameters. The most complicated part is the setting of `opt_args`, which will be illustrated in details here.

To enable a optimal controller for comparison, first make sure to set 
```python
runner = PolicyRunner(
    # other parameters for calling PolicyRunner
    use_opt=True,
}
```
For some certain environments, the optimal control inputs can be computed analytically, so a theoretically optimal controller is implemented for each of these environments. To specify such optimal controller, you may set
```python
runner = PolicyRunner(
    # other parameters for calling PolicyRunner
    use_opt=True,
    opt_args={"opt_controller_type": "OPT"},
}
```
For most environments, only the MPC-based optimal controller `gops.sys_simulator.opt_controller.OptController` is available, under which condition the codes should be like
```python
runner = PolicyRunner(
    # other parameters for calling PolicyRunner
    use_opt=True,
    opt_args={
        "opt_controller_type": "MPC",
        "num_pred_step": 5,
        # other parameters for instantiating an OptController
    },
}
```
This will instantiate an `OptController` with a prediction step of 5.
:::{note}
The parameter `model` needed for `OptController`'s initialization is automatically created and passed according to your simulation environment, so it won't be necessary to specify a model in `opt_args`.
:::
To customize other parameters, just add a key-value pair into `opt_args`. You may refer to [Model Predictive Control (MPC) Module](./mpc.md) for the meaning of `OptController`'s parameters.

A tricky thing is the usage of terminal cost function. By default, no terminal cost function is introduced. To enable one, set
```python
runner = PolicyRunner(
    # other parameters for calling PolicyRunner
    use_opt=True,
    opt_args={
        "opt_controller_type": "MPC",
        "num_pred_step": 5,
        "use_terminal_cost": True,
        # other parameters for instantiating an OptController
    },
}
```
This works for environments whose models a default terminal cost function is integrated into. But for those environment models without a default terminal cost function, you need to define your own one and pass it to `OptController` by
```python
# Load value approximate function
value_net = load_apprfunc("../results/INFADP/lqs4a2_poly", "115000_opt").v

# Define terminal cost of MPC controller
def terminal_cost(obs):
    obs = obs.unsqueeze(0)
    return -value_net(obs).squeeze(-1)

runner = PolicyRunner(
    # other parameters for calling PolicyRunner
    use_opt=True,
    opt_args={
        "opt_controller_type": "MPC",
        "num_pred_step": 5,
        "use_terminal_cost": True,
        "terminal_cost": terminal_cost,
        # other parameters for instantiating an OptController
    },
}
```
In this example, a state value network learned by the reinforcement learning algorithm is used as a terminal cost function.

A whole example for using `PolicyRunner` for simulation is as follows.
```python
from gops.sys_simulator.call_terminal_cost import load_apprfunc
from gops.sys_simulator.sys_run import PolicyRunner

# Load value approximate function
value_net = load_apprfunc("../results/INFADP/lqs4a2_poly", "115000_opt").v

# Define terminal cost of MPC controller
def terminal_cost(obs):
    obs = obs.unsqueeze(0)
    return -value_net(obs).squeeze(-1)

runner = PolicyRunner(
    # Parameters for policies to be run
    log_policy_dir_list=["../results/INFADP/lqs4a2_mlp",
                         "../results/INFADP/lqs4a2_mlp",
                         "../results/INFADP/lqs4a2_mlp",
                         "../results/INFADP/lqs4a2_poly"],
    trained_policy_iteration_list=["4000",
                                   "5000",
                                   "6000",
                                   "115000_opt"],
    
    # Save environment animation or not
    save_render=False,
    
    # Customize plot range
    plot_range=[0, 100],

    # Legends for each policy in figures
    legend_list=["InfADP-4000-mlp",
                 "InfADP-5000-mlp",
                 "InfADP-6000-mlp",
                 "InfADP-115000-poly"],
    
    # Constrained environment or not
    constrained_env=False,

    # Tracking problem or not
    is_tracking=False,

    # Use adversarial action or not
    use_dist=False,

    # Parameter for time interval between steps
    dt=0.1,

    # Parameters for environment initial info
    is_init_info=True,
    init_info={"init_state": [0.5, 0.2, 0.5, 0.1]},

    # Parameters for optimal controller
    use_opt=True,
    opt_args={
        "opt_controller_type": "MPC",
        "num_pred_step": 5,
        "ctrl_interval": 1,
        "gamma": 0.99,
        "minimize_Options": {"max_iter": 200, "tol": 1e-4,
                             "acceptable_tol": 1e-2,
                             "acceptable_iter": 10,},
        "use_terminal_cost": True,
        "terminal_cost": terminal_cost,
        "verbose": 0,
        "mode": "collocation",
    },

    # Parameter for obs noise
    obs_noise_type="normal",
    obs_noise_data=[[0.] * 4, [0.1] * 4],

    # Parameter for action noise
    action_noise_type=None, 
    action_noise_data=None,
)

runner.run()
```