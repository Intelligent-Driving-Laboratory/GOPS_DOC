(simulink)=
# Simulink to GOPS

GOPS uses slxpy to convert Simulink models to Python environments.
Slxpy is a toolchain for seamlessly generating efficient Simulink-to-Python binding and gym-like environment wrapper.

## Documentation structure
The sidebar on the right roughly corresponds to your learning process. Follow instructions in Prerequisities, Installation and Quick start to use this package.

For Simulink modeling guide, see Modeling guide.  
For Gym and `env.toml` config documentation, see Gym-like environment.  
For development notes and todos, see Development.  
To build for multiple Python versions, try Multi target build.

The flowchart serves as an overview and briefly describes the common workflow for your smoother integration. You could refer to relevant sections in the wiki for details.
(conversion)=
```{figure} ./figures&videos/simulink_conversion.png
:alt: conversion
:align: center
:width: 600px
```

## Prerequisities
Due to the nature of native compilation, certain preparation is needed before using this package.

> A quick preview into Quick start page for information about `Step x`

### MATLAB

- Only needed for `Step 2` (Simulink to C++)

- **Version**: >= R2018a ( >= **R2021a** recommended )

  - **R2021a** may be the first version actually suitable for RL environment as it allows `instance parameters`. Previous versions of Embedded Coder will generates static parameters which might be difficult to use in a program (shared by all instances).
  - For version >= R2018a, limited support is added.

    MATLAB prior to R2021a will inline parameters defined in model workspace when C++ interface is chosen. The script has some logic to allow you to code as R2021 workflow, and maintain tunability on prior to R2021a releases, but the script may fail on the first run and work for following runs due to unknown reasons. (In R2021a it's far easier)

  - For version <= R2017b, some Simulink internal error prohibits proper code generation, thus unsupported.

  - MATLAB since **R2022a** supports **reusable Simscape model**, and slxpy provides corresponding support. Simscape enables powerful non-causal system modeling, which may be very useful for environment design.

    After Mathworks ticket 05353942 & 05373346, reusable C++ class in this release is an unintended bug, and only reusable C interface is officially supported. So, it may not yet work as expected. (Bug/Enhancement Submitted)

  - MATLAB **R2022b** fixes some code generation errors (with ticket 05703735) with complex VDBS models. It's recommended to upgrade.

- **Toolbox**: Simulink, Embedded Coder, MATLAB Coder, Simulink Coder

### Python

- Almost always needed, except for `Step 2`
- **Version**: >= 3.8 (but generated binding can target Python 3.7)

  Slxpy uses a bunch of features added in Python 3.8. **Anaconda** or **Miniconda** based installation recommended.

### C++ toolchain

- Needed for `Step 4` (Building C++)

  For `Step 2`, Embedded Coder does not depend on a C++ toolchain to generate code, but may display a warning for failing to generate build files, which is OK.

  For some MATLAB versions, however, if you are facing error like this:
  > The model is configured for C++ code generation, but the C-only compiler, LCC, is the default compiler. To allow code generation, on the Code Generation pane:
  >
  > 1. Select the 'Generate code only' check box.
  > 2. In the Toolchain field, select a toolchain from the drop-down list.

  it may be a logic error in Embedded Coder. Just select an alternative C++ toolchain other than LCC, even if it does not exist in your system.

- C++ 17 compatible compiler (one of)
  - for Windows, Visual Studio 2019 16.11 or newer (16.7 is broken with `std::functional`)
  - Clang 5 or newer
  - GCC 7 or newer

### Knowledge

- General MATLAB/Simulink knowledge
- Basic Simulink code generation knowledge
- Basic C++ compiler knowledge is helpful to diagnose potential issues

## Installation
You need to install two packages, one Python package for Python main logic, one MATLAB toolbox for MATLAB interop.

1. Install Python package with `pip install slxpy`

    It is recommanded to use slxpy with conda (to enable multi-target build) and install slxpy in an dedicated conda environment, i.e.
    ```bash
    conda create -n slxpy python=3.9
    conda activate slxpy
    ```
    Then install package with
    ```bash
    pip install slxpy
    ```
    or
    ```bash
    pip install slxpy[gym]
    ```
    if you wish to build gym-wrapper directly in this environment.

    Slxpy does not come with a conda package yet. If you prefer to install dependencies through conda, create environment with
    ```bash
    conda create -n slxpy -c conda-forge --override-channels python=3.9 pybind11 pybind11-stubgen Jinja2 tomli importlib_resources packaging click numpy gym
    ````

2. Install MATLAB toolbox

    Downloading toolbox from [File Exchange link](https://www.mathworks.com/matlabcentral/fileexchange/100416-slxpy) and double-click it in MATLAB to install.

## Quick start
0. Prepare a Simulink model `foo.slx` suitable for code generation (See Modeling guide)

1. Project creation

   The project folder is a **dedicated** folder for slxpy to configure, generate and build for a specific model. For simple use, you need to create an empty folder as the project folder.

   **Run in command line**

   ```bash
   mkdir bar   ## Create slxpy project folder, choose any name you like
   cd bar
   conda activate slxpy   ## Needed if you install slxpy in a dedicated environment
   slxpy init  ## Interactively fill up basic information
   ```
   Interactively fill up basic information
   ```
   Simulink model name [bar]: <The Simulink model name without .slx suffix>
   Code generation C++ class name [barModelClass]: <A valid C++ identifier you like>
   Code generation C++ namespace []: <Leave empty for simple use>
   ```

   Then adjust `model.toml` and `env.toml` as needed (See comments in file, and also Gym-like environment).

2. Simulink code generation

   **Run in MATLAB command line | cwd: wherever the model is on search path**

   ```matlab
   workdir = '/path/to/bar';    % Absolute path to slxpy project folder
   slxpy.setup_config(workdir)  % Only need to be run for the first time, or after tuned model.toml
   slxpy.codegen(workdir)       % Code generation
   ```

3. Slxpy asset generation

   **Run in command line | cwd: project folder**

   ```bash
   ## Assuming still in bar folder
   slxpy generate
   ```

4. Build extension

   **Run in command line | cwd: project folder**

   ```bash
   ## Assuming still in bar folder
   python setup.py build
   ```

5. Test extension

   **Run in command line | cwd: project folder**

   ```bash
   ## Assuming still in bar folder
   cd build/lib<platform-suffix>
   python
   ```

   **Run in Python REPL | cwd: build folder**

   ```python
   ## Substitute foo & bar to your corresponding model & project name
   import bar
   a = bar.fooModelClass()
   b = bar.RawEnv()
   c = bar.RawEnvVec(16)
   d = bar.GymEnv()
   e = bar.GymEnvVec(16)

   ## Could also provide an EnvSpec similar to Gym's EnvSpec
   ## Check stub or call help(bar._env.EnvSpec) for more options.
   spec = bar._env.EnvSpec(
       id='bar-v0',
       max_episode_steps=100,
       strict_reset=True,
   )
   env = bar.GymEnv(spec)
   ```


## Modeling guide
Slxpy follows standard Simulink code generation process. If your model follows standard, minimal adjustments are required for proper code generation. So, detailed discussion about Simulink modeling is out of scope for this guide, you shall refer to Simulink documentation for instructions.

If you need some learning materials about modeling and code generation, see [Reference materials](#reference-materials) section.

To support gym environment generation, see Gym-like environment.

A example model `example_model.slx` is available at the [Release](https://github.com/jjyyxx/slxpy/releases) section, with some extra tips and best practices annotated in the model. You can download and try it out.

### Tunable parameter

The computer execution model is inherently deterministic, all randomness relies on at least one external source.
To give environment randomness, we must make some parameters tunable, so, model parameters (physical parameters, random seed, initial state of intergrator, etc.) shall be created with following two steps.

- Set them in `Model workspace` as `Simulink Parameter`. If it's a `MATLAB variable` rather than a `Simulink Parameter`, right-click entries, select `Convert to parameter object` to convert.
- Tick the `Argument` checkbox.

Parameter tunability has certain limitations, see the "Limitations by Embedded Coder" section for details.

### Recipes

#### Model with existing controller
If you have a model with an existing closed-loop controller, you could separate all other blocks into a **Plant** subsystem (tip: selecting all blocks except the controller, right-click and choose "Create subsystem from selection"), deleting (or commenting out) the controller, and connecting **Plant** subsystem's input and outport ports to root inports and outports. If you need to create a Gym-like environment, you could preprocess action, postprocess observation and calculating rewards and done signals at root level according to requirements in Gym-like environment.

#### Action switching
Both _Variant Source_ and _Multiport Switch_ are sensible choices for switching between multiple inputs (e.g. one inport and one closed-loop controller). The fundamental difference between them is (I call) the choice happens at compile-time vs run-time.
- If you do not need to switch between different inputs at run-time, _Variant Source_ is the correct choice, because it completely eliminates the other branch. Thus, even if your closed-loop controller does not support code generation (e.g. with an S-function), you can still generate code with external input. Efficiency, visual clearance and prevention of the signal broadcasting bug (see below) are its additional benefits.
- If you DO need to switch between different inputs at run-time, you have to use Multiport Switch, with an additional inport or tunable parameter as driver. **Extra care shall be taken to specify inport dimension explicitly, as inport may erroneously be considered as a scalar then broadcast to the same size as the closed-loop controller.**

### Limitations

#### Limitations by Embedded Coder

- S Function: You have to provide a `.tlc` file for S Function code generation, but `.tlc` is a difficult topic. So, I recommend using `MATLAB Function` block when possible.
- Fixed-step Solver: Variable-step solver do not support code generation in Embedded Coder. (Some models may get wrong simulation result in Fixed-step Solver if numeric condition is bad. Make sure to validate before code generation for proper results.)
- Algebraic Loop: Simulink could partially handle algebraic loop, but code generation does not. Try avoiding it using a `Unit Delay` or `Memory` block, or solve it iteratively in a `MATLAB Function` block.
- Variable-sized input: Embedded Coder C++ interface do not support it.
- Parameter tunability: See [Limitations for Block Parameter Tunability in Generated Code](https://www.mathworks.com/help/rtw/ug/limitations-for-block-parameter-tunability-in-the-generated-code.html)
- Other blocks not supported by code generation, refer to Simulink documentation.

#### Limitations by Slxpy

- Variable-sized output / Fixed-point data / Bitfield / Event & function-call based system: difficult to handle properly, currently not considered
- String: string-related blocks are not supported. String `std::string` lead to non-POD struct in C++, breaking a fundemental assumption for Slxpy

Luckily, entries mentioned above might rarely be used in modeling, especially physics-related ones.

### Reference materials
If you are not familiar with Simulink modeling, you could take a look at [Simulink Onramp](https://www.mathworks.com/learn/tutorials/simulink-onramp.html) tutorial.

If you are not familiar with general process of preparing a Simulink model for code generation, you could see
1. https://www.mathworks.com/help/ecoder/ug/standard-methods-to-prepare-a-model-for-code-generation.html
2. https://www.mathworks.com/help/ecoder/product-fundamentals.html

## Gymlike environment
If modeling properly, Slxpy could generate gym environment with minimal configuration. If you find the configurations insufficient for your needs, take a look at the [Advanced wrapping](#advanced-wrapping) section and consider submitting an issue or PR.

### Model requirement

- One inport of data type `double` (default) as **action**. Recommend to have exactly one inport, as additional inports will get zero input (meaningless).
- One output of data type `double` (default) as **observation**. Recommend to be the first outport.
- One **scalar** output of data type `double` (default) as **reward**. Recommend to be the second outport.
- One **scalar** output of data type `logical` as **done**. Recommend to be the third outport.
- Any additional outports of data type `double` (default) to be included in **info** dict.

### env.toml

Configuration file `env.toml` can be used to control various aspects of environment wrapping, including action_space, observation_space, initial observation and parameter initialization.

The following sections are taken from the template file.

#### Basic setting
Control features to be generated for the module.

```toml
### Config version. DO NOT CHANGE.
__version__ = "1.0.0"

### Generate raw environment wrapper.
use_raw = true

### Generate gym-flavor environment wrapper (tensor action, tensor observation).
### NOTE: gym-flavor environment has to meet certain criteria. See "gym" section below.
use_gym = true

### Environment initialization needs randomness (generally true).
use_rng = true

### Generate vectorized wrapper over raw/gym environment.
use_vec = true

### Vectorized wrapper use parallel execution.
### Benificial when the env is computationally intensive (CPU-bounded).
### For memory-bounded tasks, this is not very effective.
vec_parallel = false
```

#### Configure gym-simulink mapping and gym space
Control the mapping between:
1. Simulink inport and Python method argument `act`
2. Simulink outports and Python method return value `obs`, `rew`, `done` and `info`

Also control `action_space`, `observation_space` and `reward_range`.
```toml
### Configure gym-simulink mapping.
[gym]
    ### Action key in model inport(s).
    ### Data MUST be a double scalar or array.
    ### By default, the 1st inport is taken (Generally only one inport is sensible).
    ### Uncomment the line below to provide an alternative key.
    ## action_key = "act"

    ### Observation key in model outports.
    ### Data MUST be a double scalar or array.
    ### By default, the 1st outport is taken.
    ### Uncomment the line below to provide an alternative key.
    ## observation_key = "obs"

    ### Reward key in model outports.
    ### Data MUST be a double scalar.
    ### By default, the 2nd outport is taken.
    ### Uncomment the line below to provide an alternative key.
    ## reward_key = "rew"

    ### Done key in model outports.
    ### Data MUST be a boolean (or logical in MATLAB) scalar.
    ### By default, the 3rd outport is taken.
    ### Uncomment the line below to provide an alternative key.
    ## done_key = "done"

    ### Put additional outports to info dict.
    ### Option: true -> all additional outports are included
    ###         false -> empty info dict
    ###         list of keys -> selected outports are included, e.g. ["foo", "bar"]
    info = true

    ### Implicit type coercion for observation and action
    type_coercion = false

    ### Reward range, e.g. ["-inf", "inf"] | ["-inf", 0] | [-10, 10]
    reward_range = ["-inf", "inf"]

    ### Action space, similar to gym.space
    ### "type" includes: Box, Discrete, MultiDiscrete, MultiBinary
    [gym.action_space]
        type = "Discrete"
        n = 2

    ### Observation space, see action_space above
    [gym.observation_space]
        type = "Box"
        low = 0.0
        high = 1.0
        shape = [2, 2]
        dtype = "float64"
```

#### Control reset behavior to get initial observation

```toml
## Options controlling reset behavior
[reset]
    ### Take one step after environment initialization to get initial observation.
    ### If set to true/false, optionally provide a initializer for initial action/observation.
    first_step = true

    ### Only valid when "first_step = true".
    ### By default, initial action is initialized with "default initialization".
    ### Uncomment the line below to provide an "aggregate initialization" list.
    action = "{ 1.0 }"

    ### Only valid when "first_step = false".
    ### By default, initial observation is initialized with "default initialization"
    ### and might be affected by const block output optimization.
    ### Uncomment the line below to provide an "aggregate initialization" list.
    ## observation = "{ 1.0 }"
```

#### Define how parameters are initialized on each reset
Environment randomness is crucial for reinforcement learning.
Because program execution is inherently deterministic, all randomness comes from parameters. This section demonstrates some commonly used (limited set of) random mechanisms while maintaining reproducibility with `seed()` method.

Parameter names must be a subset of the Simulink model tunable parameters.

```toml
### A table to define individual parameter initialization policy
[parameter]
[parameter.seed_1]
    type = "seed"

[parameter.seed_2]
    type = "seed"

[parameter.constant_1]
    type = "constant"
    value = 1.0

[parameter.constant_2]
    type = "constant"
    value = "{ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 }"

[parameter.uniform_1]
    type = "uniform"
    low = 0.0
    high = 1.0

[parameter.uniform_2]
    type = "uniform"
    low = 0.0
    high = 1.0

[parameter.uniform_3]
    type = "uniform"
    low = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    high = 1.0

[parameter.uniform_4]
    type = "uniform"
    low = 0.0
    high = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

[parameter.uniform_5]
    type = "uniform"
    low = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    high = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

[parameter.custom]
    type = "custom"
    code = "std::fill_n(params.custom, 6, -1);"
```

### Advanced wrapping
Some highly costomized needs are non-trivial to cover in a config file.
Also, going through the whole building process may be inefficient for environment tuning. Instead, you could wrap the `GymEnv` with a Python-class wrapper and implement your logic.

Instead of using inheritance, you should use composition as follows:
```python
class EnvWrap(gym.Env):
    def __init__(self, *args):
        spec = foo._env.EnvSpec(
            id='foo-v0',
            max_episode_steps=100.0,
            terminal_bonus_reward=0.0,
            strict_reset=True
        )
        self.env = brvm.GymEnv(spec)

        ## Inherit or override with a user provided space
        self.observation_space = self.env.observation_space
        self.action_space = self.env.action_space

        ## Split RNG, if randomness is needed
        self.rng = np.random.default_rng()

    def reset(self):
        def callback():
            """Custom reset logic goes here."""
            ## Modify your parameter
            ## e.g. self.env.model_class.foo_InstP.your_parameter

        ## Reset takes an optional callback
        ## This callback will be called after model & parameter initialization
        ## and before taking first step.
        return self.env.reset(callback)

    def step(self, action):
        ## Preprocess action here
        obs, reward, done, info = self.env.step(action)
        ## Postprocess (obs, reward, done, info) here
        return obs, reward, done, info

    def seed(self, seed: Optional[int] = None) -> List[int]:
        self.rng = np.random.default_rng(seed)
        return self.env.seed(seed) if seed is not None else self.env.seed()
```
One shortcoming is if you provided a reset callback, you should set `vec_parallel` to `false`, otherwise the callback and Python GIL may lead to deadlock.


## Multi target build
To help build a model for multiple Python versions, slxpy provides a command to automatically build for multiple Python versions and aggregate results.

0. It's required that slxpy is running with conda installation available to use this feature!

1. Setup builder environments (Need only once)

```bash
slxpy multi-build setup
## Or, for specific Python versions
## slxpy multi-build setup -v 3.7 -v 3.9

## If you want to remove builder environments, run
## slxpy multi-build clean
```

2. Build
Run the command in a slxpy project folder **after** calling `slxpy generate`.

```bash
slxpy multi-build run
## Or, for specific Python versions
## slxpy multi-build run -v 3.7 -v 3.9
```
Your binary targeting multiple versions shall now be generated in separate folders in `build/` and also `build/slxpy{plat}` if you does not disable aggregation.

For other options, see command line `--help`.


## FAQ

### Numerous compiler errors about undefined identifier 'creal_T' with Simscape
Try to set simulink feature `complex` to `true` in `model.toml`.
Though Embedded Coder did not complain, some Simscape (multibody) functions may implicitly depend on complex structs `c*_T`.
This may be a flaw of Mathworks product design.

### What if code generation / transformation / compilation fails?
Do not panic and read the error message carefully. It's often a small mistake instead of fatal error. Catching a bug at compiling time is always better than a runtime error after deployment.

If you fail to locate the problem or are confident it's a Slxpy bug, it's welcome to submit an issue!
