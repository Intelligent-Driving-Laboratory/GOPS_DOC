# Introduction
Copyright © 2022 Intelligent Driving Laboratory (iDLab). All rights reserved.

## Description
Optimal control is an important theoretical framework for sequential decision-making and control of industrial objects, especially for complex and high-dimensional problems with strong nonlinearity, high randomness, and multiple constraints.
Solving the optimal control input is the key to applying this theoretical framework to practical industrial problems.
Taking Model Predictive Control as an example, computation time solving its control input relies on receding horizon optimization, of which the real-time performance greatly restricts the application and promotion of this method.
In order to solve this problem, iDLab has developed a series of full state space optimal strategy solution algorithms and the set of application toolchain for industrial control based on Reinforcement Learning and Approximate Dynamic Programming theory.
The basic principle of this method takes an approximation function (such as neural network) as the policy carrier, and improves the online real-time performance of optimal control by offline solving and online application.
The GOPS toolchain will cover the following main links in the whole industrial control process, including control problem modeling, policy network training, offline simulation verification, controller code deployment, etc.
GOPS currently supports the following algorithms:

- [Deep Q Network (DQN)](https://arxiv.org/abs/1312.5602)
- [Deep Deterministic Policy Gradient (DDPG)](https://arxiv.org/abs/1509.02971)
- [Twin Delayed DDPG (TD3)](https://arxiv.org/abs/1802.09477)
- [Asynchronous Advantage Actor-Critic (A3C)](https://arxiv.org/abs/1602.01783)
- [Soft Actor-Critic (SAC)](https://arxiv.org/abs/1801.01290)
- [Distributional Soft Actor-Critic (DSAC)](https://arxiv.org/abs/2001.02811)
- [Trust Region Policy Optimization (TRPO)](https://arxiv.org/abs/1502.05477)
- [Proximal Policy Optimization (PPO)](https://arxiv.org/abs/1707.06347)
- [Infinite-Horizon Approximate Dynamic Programming (INFADP)](https://link.springer.com/book/10.1007/978-981-19-7784-8)
- [Finite-Horizon Approximate Dynamic Programming (FHADP)](https://link.springer.com/book/10.1007/978-981-19-7784-8)
- [Mixed Actor-Critic (MAC)](https://ieeexplore.ieee.org/document/9268413)
- [Mixed Policy Gradient (MPG)](https://arxiv.org/abs/2102.11513)
- [Separated Proportional-Integral Lagrangian (SPIL)](https://arxiv.org/abs/2102.08539)

## Features

GOPS has the following features:

- Adopt a **highly modular structure** that allows for easy secondary development of environments and algorithms.

- Support mainstream **model-free** and **model-based**, **direct** and **indirect** reinforcement learning algorithms.

- Support both **serial** and **parallel** training modes.

- Support handling of special industrial control issues, such as **explicit policies**, **state constraints**, **model uncertainties**, etc.

- Support conversion from **Matlab/Simulink** models to GOPS-compatible environments and from GOPS-learned policies back to Matlab/Simulink.

- Support **model predictive control (MPC)** for environments with analytical models.

- Support evaluation of **state and action curves** and comparison of different policies.

## Installation

GOPS requires:
1. Windows 7 or greater or Linux.
2. Python 3.6 or greater (GOPS V1.0 precompiled Simulink models use Python 3.8). We recommend using Python 3.8.
3. (Optional) Matlab/Simulink 2018a or greater.
4. The installation path must be in English.

You can install GOPS through the following steps:
```bash
# clone GOPS repository
git clone https://github.com/Intelligent-Driving-Laboratory/GOPS.git
cd gops
# create conda environment
conda env create -f gops_environment.yml
conda activate gops
# install GOPS
pip install -e .
```

## Quick Start
This is an example of running finite-horizon Approximate Dynamic Programming (FHADP) on inverted double pendulum environment. 
Train the policy by running:

```bash
python example_train/fhadp/fhadp_mlp_idpendulum_serial.py
```
After training, test the policy by running:
```bash
python example_run/run_idp_fhadp.py
```
You can record a video by setting `save_render=True` in the test file. Here is a video of running a trained policy on the task:

(idpendulum)=
```{figure} ./figures&videos/idp.mp4
:alt:
:align: center
:width: 600px
```
## Cite GOPS
If you use GOPS in your research, please cite [the following paper](https://doi.org/10.1016/j.commtr.2023.100096):

```bibtex
@article{gops,
    title={GOPS: A general optimal control problem solver for autonomous driving and industrial control applications},
    author={Wenxuan Wang, Yuhang Zhang, Jiaxin Gao, Yuxuan Jiang, Yujie Yang, Zhilong Zheng, Wenjun Zou, Jie Li,
Congsheng Zhang, Wenhan Cao, Genjin Xie, Jingliang Duan, Shengbo Eben Li}
    journal={Communications in Transportation Research},
    volume = {3},
    pages = {100096},
    year={2023},
    issn={2772-4247},
    doi = {https://doi.org/10.1016/j.commtr.2023.100096},
    }
```

## Download GOPS
You can download the newest version of GOPS from [this page](https://github.com/Intelligent-Driving-Laboratory/GOPS/releases).

## Contributors
The contributors of GOPS are as follows:

**Team Leader**

[Shengbo Eben Li](https://www.researchgate.net/profile/Shengbo-Li-2) leads the development of this project.


**Team Members (in alphabetical order)**

[Baiyu Peng](https://baiyu6666.github.io),
[Congsheng Zhang](https://www.researchgate.net/profile/Congsheng-Zhang),
[Genjin Xie](https://www.researchgate.net/profile/Xie-Genjin-2),
[Ziqing Gu](https://scholar.google.com/citations?user=B8Ys1-0AAAAJ).
[Hao Sun](https://gitee.com/roshandaddy),
[Jiaxin Gao](https://www.researchgate.net/profile/Jiaxin_Gao5),
[Jie Li](https://www.researchgate.net/profile/Jie-Li-216),
[Jingliang Duan](https://www.researchgate.net/profile/Jingliang-Duan),
[Letian Tao](https://github.com/tlt18),
[Tong Liu](https://www.researchgate.net/profile/Tong-Liu-94),
[Wenhan Cao](https:wenhancao.github.io),
[Wenjun Zou](https://www.researchgate.net/profile/Wenjun-Zou-6),
[Wenxuan Wang](https://www.researchgate.net/profile/Wenxuan_Wang10),
[Weixian He](https://github.com/HWXian),
[Xujie Song](https://www.linkedin.com/in/xujie-song/),
[Yang Guan](https://www.researchgate.net/profile/Yang-Guan-2),
[Yinuo Wang](https://github.com/happy-yan),
[Yuhang Zhang](https://www.researchgate.net/profile/Yuhang-Zhang-27),
[Yuheng Lei](https://sites.google.com/view/yuhenglei),
[Yujie Yang](https://yangyujie-jack.github.io/),
[Yuxuan Jiang](https://github.com/jjyyxx),
[Zhilong Zheng](https://www.researchgate.net/profile/Zhilong-Zheng-4)

