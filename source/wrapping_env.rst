.. GOPS documentation master file, created by
   sphinx-quickstart on Sat Feb 25 15:24:01 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



.. _wrapping_utils:

Environment Wrapping Utils
================================

.. note:: You can use the following functions to wrap your environment simply by adding some thing like the following lines to your training configuration file:

.. code-block:: python

 parser.add_argument("--reward_scale", type=float, default=2)
 parser.add_argument("--reward_shift", type=float, default=1)



.. autofunction:: gops.env.wrapper.wrapping_utils.wrapping_env

.. autofunction:: gops.env.wrapper.wrapping_utils.wrapping_model




