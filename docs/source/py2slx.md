# GOPS to Simulink

Put the trained policy back into Simulink for closed-loop verification and deployment.
## Prerequisites
1. MATLAB with Simulink.

    We recommend the up-to-date MATLAB version. Since the bridge uses `pyrun`, the minimum MATLAB version is R2021b.

2. Python installation compatible with MATLAB. 

   Check MATLAB documentation [Configure Your System to Use Python](https://www.mathworks.com/help/releases/R2022a/matlab/matlab_external/install-supported-python-implementation.html), especially "Versions of Python Compatible with MATLAB Products by Release" in "Related Topics" section.

## Usage
1. Users can refer to the example of document `py2slx_example.py` to use the policy conversion tool.

    You need to set four parameters(`log_policy_dir_list`、`trained_policy_iteration_list`、`export_controller_name`、`save_path`) according to the requirements of the reference example.


2. Run the example file you configured above.

   Py2slx tool will check the compatibility of the model to confirm whether it can be converted and whether user's matlab version meets the requirements.
   
   - GOPS builtin models should work well without compatibility issue. If meeting something difficult, you could refer to [PyTorch JIT documentation](https://pytorch.org/docs/stable/jit.html) for requirements about `trace-able nn.Module`.
   - If matlab is not installed on your computer or the version is incorrect, the corresponding prompt will appear.
   - If everything is OK, a saved model will exist at `save_path` and the latest version of matlab on your computer will be opened.


3. Launch MATLAB 

   o ensure a successful execution, please make sure you have launched MATLAB within a Python environment that has PyTorch installed. If you encounter any issues, verify that `GOPS` is also installed in the same `PyTorch` environment.


    - If you prefer using your system-wide Python installation, you may launch MATLAB either from the shortcut or command line.



    - For the conda-based environment, the most efficient method would be to initiate MATLAB via the command line interface.

        ```shell
        conda activate <YOUR_ENV_WITH_PYTORCH>
        matlab
        ```
    
    - When utilizing alternative types of environments, the activation method may differ. However, it is crucial to ensure that environment variables are accurate when initiating MATLAB.

    To verify the environment is correct, you could type `pyenv` in MATLAB Command Window. The `Version`, `Executable`, `Library` and `Home` field of the result should match your target Python environment.

4. Copy `gops_validation_bridge.m` to your Simulink model directory. Create a `Level-2 MATLAB S-Function` block, set:
    - `S-Function Name` field to `gops_validation_bridge`
    - `Parameters` field to `'save_path'` (e.g. `'model.pt'`). The path is relative to your MATLAB working directory and an absolute path will also work.
    
   The observation will be input into the block inlet, and the block outlet will output policy action from the trained policy.


5. Utilize the `Level-2 MATLAB S-Function` block as the closed-loop controller in your Simulink model, then initiate the simulation and validation process.