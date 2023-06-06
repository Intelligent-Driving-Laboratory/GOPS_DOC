# Training Configuration

This doc illustrates how to set arguments in training process. There are several pre-defined training examples using specific algorithm in dir  `example_train/algorithm`. You can create a new training configuration based on existing example.

GOPS use `argparse` package to pass and parse arguments, the arguments will be passed to ```init_args() ``` function in `gops/utils/init_args.py` to create corresponding components such like sampler or trainer.

:::{important}
Some arguments are coupling with others. Change them separately may cause error or incorrect results. **Please carefully read this doc before making any change.** 
::: 



## Environment Variables
`OMP_NUM_THREADS` : This environment variable controls the num of threads of each process when using `ray` package for parallel computing. The default value is `1`. 


## User Parameters
Key parameters in user level:

- `env_id` (str): ID of the environment
- `algorithm` (str): name of the reinforcement learning algorithm to use
- `enable_cuda` (bool): whether to use CUDA for computation
- `seed` (int): (Optional): assign the global seed for training, using a random value by default 

  
## Environment Parameters
Basic and extra parameters for environment.

- `action_type` (str): type of environment action: 'continu' or 'discret' 
- `is_render` (bool): whether render the env when evaluation

:::{note}
In order to unify different type of environments, GOPS will add some extra environment wrappers for '_data' type or '_model' type environment by default. **You can also add or remove specific wrapper by adding corresponding argument here.** Refer to
{ref}`wrapping_utils` for more information.   
::: 
:::{note}
Some environments may need extra parameters, which should be added here.
::: 

## Approximate Function Parameters
Basic and extra parameters for value and policy function. 

- `value_func_name` (str): value function structure, depended on the used algorithm: `StateValue`, `ActionValue`, `ActionValueDis`, `ActionValueDistri`
- `value_func_type` (str): type of value function, depended on the used algorithm: `MLP`, `CNN`, `CNN_SHARED`, `RNN`, `POLY`, `GAUSS`
- `policy_func_name` (str): policy function structure, depended on the used algorithm: `None`, `DetermPolicy`, `FiniteHorizonPolicy`, `StochaPolicy`
- `policy_func_type` (str): type of policy function, depended on the used algorithm: `MLP`, `CNN`, `CNN_SHARED`, `RNN`, `POLY`, `GAUSS`
- `policy_act_distribution` (str): type of distribution for policy actions: `default`, `TanGaussDistribution`, `GaussDistribution`

:::{note}
Some arguments are coupling with others. Change them separately may cause error or incorrect results.   
::: 

There are 3 main ways to check for such errors. 
- You can check the `init_args()` function in `gops/utils/init_args.py` as all arguments will be passed here to create corresponding components. 
- For every type of function, you can find the complete configuration in `gops/appfunc`. 
- Different choice of the function type means specific parameters need to be set, details of which can be found in `get_appfunc_dict` function in `gops/utils/common_utils`. 

For example, if the function type is `MLP` or `RNN`, the following parameters need to be set:
- `hidden_sizes` (list): size of hidden layers in value or policy function.
- `hidden_activation` (str): activation function for hidden layers in value or policy function: `relu`, `gelu`, `elu`, `selu`, `sigmoid`, `tanh`
- `output_activation` (str): activation function for output in value or policy function: `linear`, `tanh`


##  RL Algorithm Parameters
Basic and extra parameters for algorithm. 

- `value_learning_rate` (float): learning rate of value iteration
- `policy_learning_rate` (float): learning rate of policy iteration

:::{note}
For some RL algorithms, extra parameters need to be set. Refer to `algorithm` module for detailed information.
:::

Take DSAC as an example:
```bash
parser.add_argument("--value_learning_rate", type=float, default=1e-3)
parser.add_argument("--policy_learning_rate", type=float, default=1e-3)
# special parameter
parser.add_argument("--alpha_learning_rate", type=float, default=1e-3)
parser.add_argument("--gamma", type=float, default=0.99)
parser.add_argument("--tau", type=float, default=0.2)
parser.add_argument("--alpha", type=float, default=0.2)
parser.add_argument("--auto_alpha", type=bool, default=True)
parser.add_argument("--delay_update", type=int, default=2)
parser.add_argument("--TD_bound", type=float, default=10)
parser.add_argument("--bound", default=True)
```

## Trainer Parameters
Basic and extra parameters for trainer. 

- `trainer` (str): type of trainer: `off_serial_trainer`, `off_async_trainer`, `off_sync_trainer`, `on_serial_trainer`, `on_sync_trainer`
- `max_iteration` (int): number of max iteration
- `ini_network_dir` (str): path of initial networks
- `num_algs` (int): number of algorithms if async trainer is used
- `num_samplers` (int): number of samplers to use
- `sample_interval` (int): period of sampling

## Buffer Parameters
Basic and extra parameters for buffer. 

- `buffer_name` (str): name of buffer to use: `replay_buffer`, `prioritized_replay_buffer`
- `buffer_warm_size` (int): size of collected samples before training
- `buffer_max_size` (int): max size of replay buffer
- `replay_batch_size` (int): batch size of replay samples from buffer
## Sampler Parameters
Basic and extra parameters for sampler. 

- `sample_name` (str): name of sampler to use: `off_sampler`, `on_sampler`
- `sample_batch_size` (int): batch size of sampler for buffer store
- `noise_params` (dict): add noise to action for better exploration, only used for continuous action space

## Evaluator Parameters
Basic and extra parameters for evaluator. 

- `evaluator_name` (str): name of evaluator to use: `evaluator`, `evaluator_filter`
- `num_eval_episode` (int): number of episodes for evaluation
- `eval_interval` (int): period of every evaluation episode
- `eval_save` (bool): whether to save evaluation data: `True`, `False`

## Data Saving Parameters 
Basic and extra parameters for data saving. 

- `save_folder` (str): directory of data to save
- `appfunc_save_interval` (int): save value/policy every N updates
- `log_save_interval` (int): save key information every N updates