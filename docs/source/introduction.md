# Introduction
Copyright © 2022 Intelligent Driving Laboratory (iDLab). All rights reserved.

## Description
Solving optimal control problems serves as the basic demand of industrial control tasks. Existing methods like model predictive control often suffer from heavy online computational burdens. Reinforcement learning (RL) has shown promise in computer and board games but has yet to be widely adopted in industrial applications due to a lack of accessible and high-accuracy solvers. Current RL solvers are often developed for academic research and require a significant amount of theoretical knowledge and programming skills. Besides, many of them only support Python-based environments and limit to model-free algorithms. To address this gap, we develop General Optimal control Problems Solver (GOPS), an easy-to-use RL solver package that aims to build real-time and high-performance controllers in industrial fields. GOPS is built with a highly modular structure that retains a flexible framework for secondary development. Considering the diversity of industrial control tasks, GOPS also includes a conversion tool that allows for the use of Matlab/Simulink to support environment construction, controller design, and performance validation. To handle large-scale problems, GOPS can automatically create various serial and parallel trainers by flexibly combining embedded buffers and samplers. It offers a variety of common approximate functions for policy and value functions, including polynomial, multilayer perceptron, convolutional neural network, etc. Additionally, constrained and robust algorithms for special industrial control systems with state constraints and model uncertainties are also integrated into GOPS.

GOPS provides a variety of algorithms for solving optimal control problems. These built-in algorithms cover the mainstream RL algorithms, including model-free/model-based, on-policy/off-policy, and direct/indirect. Currently supported algorithms are shown as follows:
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
- [Ternary Policy Iteration Algorithm for Nonlinear Robust Control (RPI)](https://arxiv.org/abs/2007.06810)
- [Separated Proportional-Integral Lagrangian (SPIL)](https://arxiv.org/abs/2102.08539)

## Features
The main features of GOPS are summarized as follows:
1. GOPS adopts a highly modular configuration that allows for easy secondary development of environments and algorithms, making it accessible for users without professional RL knowledge or programming skills.
2. GOPS supports multiple training modes for handling complex and large-scale problems, including serial and parallel modes for on-policy and off-policy, model-free and model-based, and direct and indirect algorithms. It can handle special requirements from industrial control, such as explicit policies, state constraints, and model uncertainties.
3. Considering the widespread use of Matlab/Simulink in industry control, GOPS offers a convenient conversion tool to support high-performance controller design for Simulink models. This tool enables the transformation of existing Simulink models into GOPS-compatible environments and allows for performance validation and controller deployment by sending the learned policy back to Simulink.

## Installation
Installation requirements:
1. Operating system: GOPS is compatible with Windows 7 or any later version, as well as Ubuntu 18.04 or any later version. Please make sure that your system meets these specifications.
2. Python version: GOPS requires Python 3.6 or a more recent version. For the proper functioning of the precompiled Simulink models in GOPS V1.0, it is necessary to have Python 3.8 installed. We highly recommend using Python 3.8 to ensure the best user experience.
3. Matlab/Simulink (Optional): To utilize the full capabilities of GOPS, you may choose to have Matlab/Simulink 2018a or a more recent version installed. This is not mandatory for the installation process, but it enables seamless integration and enhanced functionality with Matlab/Simulink.
4. Installation Path: It is crucial to note that the installation path for GOPS should be in English and does not contain any special characters.

Installation steps:
1. Clone the GOPS repository and change to the GOPS directory:
```bash
git clone https://github.com/Intelligent-Driving-Laboratory/GOPS.git
cd gops
```
2. Create and activate the conda environment for GOPS:
```bash
conda env create -f gops_environment.yml
conda activate gops
```
3. Install GOPS and its required packages:
```bash
pip install -e .
```

## Quick Start
To demonstrate the usage of GOPS, we give an example of training a policy using Finite-Horizon Approximate Dynamic Programming (FHADP) algorithm in the inverted double pendulum environment. 

We train the policy by running the following command:
```bash
python example_train/fhadp/fhadp_mlp_idpendulum_serial.py
```

After training, we test the policy by running the following command:
```bash
python example_run/run_idp_fhadp.py
```

We can record a video by setting `save_render`=`True` in the file `run_idp_fhadp.py`. A video of testing a policy trained by FHADP in this environemnt is shown as follows:

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

[Jingliang Duan](https://www.researchgate.net/profile/Jingliang-Duan) is the co-leader of this project.

**Team Members (in alphabetical order)**

[Baiyu Peng](https://baiyu6666.github.io),
[Congsheng Zhang](https://www.researchgate.net/profile/Congsheng-Zhang),
[Genjin Xie](https://www.researchgate.net/profile/Xie-Genjin-2),
[Ziqing Gu](https://scholar.google.com/citations?user=B8Ys1-0AAAAJ),
[Hao Sun](https://gitee.com/roshandaddy),
[Jiaxin Gao](https://www.researchgate.net/profile/Jiaxin_Gao5),
[Jie Li](https://www.researchgate.net/profile/Jie-Li-216),
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
[Zhilong Zheng](https://www.researchgate.net/profile/Zhilong-Zheng-4).

