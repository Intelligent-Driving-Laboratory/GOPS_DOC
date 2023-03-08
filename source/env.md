# Environment
## Overview
The environment module contains a series of pre-built environment models with reward signals, each corresponding to a standard optimal control problem. Users also have the option to create their own environments and add them to the GOPS library. Additionally, GOPS has a user-friendly tool that can transform Simulink models into GOPS environments to train a control policy. After that, the tool can convert the trained policy into an S-function and send it back to Matlab/Simulink for performance validation or controller deployment. 

All environments in GOPS follow a uniform Gym-style interface, which contains an observation space, an action space, a reset function, and a step function. The observation space and action space specify the dimensions, bounds, and data types of observation (i.e., state) and action. The reset function generates an initial state randomly with a user-specified state distribution. The step function takes action as input, runs the environment one step forward, and returns the next observation, reward, and episode termination signal.

## Classification

### Benchmark environments

GOPS contains commonly used RL benchmarks from OpenAI Gym (Brockman et al., 2016), Atari (Bellemare et al., 2013), and Mujoco (Todorov et al., 2012). 

### Simulink environments

Matlab/Simulink is a widely used software in industrial control, and many of its models can be highly complex and costly to recreate in Python. To address this issue, GOPS offers a utility tool that can convert standard Simulink models into GOPS-compatible environments and then sends the trained policy back to Simulink for validation. 

After properly configuring the Simulink model, GOPS uses MATLAB Embedded Coder to generate C++ codes, reads model metadata to extract model I/O and parameters, and generates pybind11 binding codes with templates to become Python-compatible environments. The compiled environment is data-typed, which has exact input and output equivalence with the Simulink model. The new environment retains the ability to manually tune critical parameters, which avoids repeatedly rebuilding the binary file and simplifies the environment setups. It preserves features such as cross-platform support, high execution efficiency, and type hint generation. Once an optimal control policy is found, the tool can send it back to Simulink by wrapping it in an S-Function block, which can be easily integrated into a Simulink model for performance evaluation or controller deployment.

### Optimal control environments

GOPS also includes typical industrial optimal control environments such as vehicle control, aircraft control, and robotic control. This module also contains special environments that consider state constraints and model uncertainties.

## Define custom environments

### Benchmark environments

To create a benchmark environment, first create a file named after the environment. For example, to create the Gym environment `Acrobot-v1`, first create a file `gym_acrobot_data.py`. Then, define an environment creator function in the file:
```python
def env_creator(**kwargs):
    return gym.make("Acrobot-v1")
```
In this way, the environment will be created when passing `env_id="Acrobot-v1"` in training configurations.

### Simulink environments

See [](simulink).

### Optimal control environments

#### Naming conventions

Class names should be named in Pascal naming convention (PascalCase), which means that the first letter of each word should be capitalized and the rest of the letters should be lowercase. Specifically, for abbreviations, all letters should be capitalized.

- Correct examples: `ReplayBuffer`, `ValueDiracDistribution`, `DQN`, `InfADP`

- Incorrect examples: `replaybuffer`, `valueDiracDistribution`, `Dqn`, `InfAdp`

Functions and methods should be named according to snake naming convention (snake_case), which means all letters are in lowercase and connected by underscores (_). If a function is only used within a module, or a method is only used within a class, an underscore can be added at the beginning of the word as appropriate.

- Correct examples: `store`, `add_batch`, `_get_conv_out_size`

- Incorrect examples: `Store`, `addBatch`

Variables should be named according to snake naming convention (snake_case), which means all letters are in lowercase and connected by underscores (_). If a variable is only used within a module or class, an underscore can be added at the beginning of the word as appropriate. Specifically, if a variable represents a type rather than a specific value (often seen in getattr), Pascal naming convention used in class naming can be used. 

- Correct examples: `hidden_sizes`, `log_save_interval`, `ApproxContainer`

- Incorrect examples: `hiddenSizes`, `logSaveInterval`

Constants should be named according to SNAKE naming convention (SNAKE_CASE), which means all letters are in uppercase and connected by underscores (_).

- Correct example: `CONSTANT_CASE`

#### Initial state space

Optimal control environments need specification of the range and distribution of the initial state through the following three arguments:

`work_space`: `Optinal[Sequence]` = `None`. The range of the initial state in test mode.

`train_space`: `Optional[Sequence]` = `None`. The range of the initial state in training mode.

`initial_distribution`: `str` = `"uniform"`. The type of initial state distribution, in ['uniform', 'normal'].

#### Additional information

The `step()` method of an environment returns a 4-tuple (`obs`, `reward`, `done`, `info`). The `info` is a dictionary which contains additional information of the environment. For example, some environment has an internal state that is different from the observation, and the state is returned in `info`. All the keys and values in `info` can be stored in the replay buffer so that they are available to the algorithms. To enable this, a custom method `additional_info()` should be defined in the environment, which returns a dictionary that specifies the shape and data type of each additional information item. The replay buffer will read the `additional_info()` and create the corresponding places for these items.

For example, the `additional_info()` of an environment with an internal state should be:

```python
{
    "state": {"shape": (self.state_dim,), "dtype": np.float32},
}
```

For trajectory tracking environments, the information of the reference trajectory is also returned. The additional info of a 2DOF vehicle trajectory tacking environment is:

```python
{
    "state": {"shape": (self.state_dim,), "dtype": np.float32},
    "ref_points": {"shape": (self.pre_horizon + 1, 2), "dtype": np.float32},
    "path_num": {"shape": (), "dtype": np.uint8},
    "u_num": {"shape": (), "dtype": np.uint8},
    "ref_time": {"shape": (), "dtype": np.float32},
    "ref": {"shape": (2,), "dtype": np.float32},
}
```

For constrained environments, an additional item `constraint` is returned:

```python
{
    "constraint": {"shape": (1,), "dtype": np.float32},
}
```

#### Special environments

Here are some special parameters for vehicle trajectory tracking environments:

`pre_horizon`: `int` = `10`. The number of observed reference points.

`path_para`: `Optional[Dict[str, Dict]]` = `None`. Parameters for reference path, see `gops.env.env_ocp.resources.ref_traj_data`.

`u_para`: `Optional[Dict[str, Dict]]` = `None`. Parameters for reference speed, see `gops.env.env_ocp.resources.ref_traj_data`.

Here are some special parameters for vehicle constrained trajectory tracking environments:

`surr_veh_num`: `int` = `4`. Number of surrounding vehicles.
