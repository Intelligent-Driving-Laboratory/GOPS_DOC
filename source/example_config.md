# Training Configuration

This doc illustrates how to set arguments in training process. There are several pre-defined training examples using specific algorithm in dir  `example_train/algorithm`. You can create a new training configuration based on existing example.

GOPS use `argparse` package to pass and parse arguments, the arguments will be passed to ```init_args() ``` function in `gops/utils/init_args.py` to create corresponding components such like sampler or trainer.

:::{important}
Some arguments are coupling with others. Change them separately may cause error or incorrect results. **Please carefully read this doc before make any change.** 
::: 



## Environment Variables
`OMP_NUM_THREADS` : This environment variable controls the num  of threads of each process when using `ray` package for parallel computing. The default value is `1`. 


## User Parameters
Key parameters in user level:

- `env_id` (str): the ID of the environment
- `algorithm` (str): the name of the reinforcement learning algorithm to use
- `enable_cuda` (bool): whether to use CUDA for computation
- `seed` (Optional[int]): assign the global seed for training, using a random value by default 

  
## Environment Parameters
Basic and extra parameters for environment.

- `action_type` (str): the type of environment action: 'continu' or 'discret' 
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


- `value_func_name` (str): value function structure, depended on the  used algorithm, refer to
- `algorithm` (str): the name of the reinforcement learning algorithm to use
- `enable_cuda` (bool): whether to use CUDA for computation
- `seed` (Optional[int]): assign the global seed for training, using a 

##  RL Algorithm Parameters

## Trainer Parameters

## Buffer Parameters

## Sampler Parameters

## Evaluator Parameters

## Data Saving Parameters 