.. GOPS documentation master file, created by
   sphinx-quickstart on Sat Feb 25 15:24:01 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



.. _wrapping_utils:

Environment Wrapping Utils
================================

.. note:: GOPS provides a number of additional functions through environment wrappers, such as observation scaling, observation noising, action clipping, and reward shaping. You can wrap an environment with certain functions by defining the corresponding parameters in the training configuration file as follows:

.. code-block:: python

 parser.add_argument("--obs_shift", type=float, default=0.0)
 parser.add_argument("--obs_scale", type=float, default=1.0)
 parser.add_argument("--obs_noise_type", type=str, default="normal")
 parser.add_argument("--obs_noise_data", type=list, default=[0.0, 1.0])
 parser.add_argument("--clip_action", type=bool, default=True)
 parser.add_argument("--reward_shift", type=float, default=0.0)
 parser.add_argument("--reward_scale", type=float, default=1.0)
 parser.add_argument("--max_episode_steps", type=int, default=200)

.. autofunction:: gops.env.wrapper.wrapping_utils.wrapping_env

.. autofunction:: gops.env.wrapper.wrapping_utils.wrapping_model




