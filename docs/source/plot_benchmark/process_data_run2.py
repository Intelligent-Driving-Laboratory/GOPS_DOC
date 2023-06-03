
import json
import pandas as pd
import numpy as np
import os
from tensorboard.backend.event_processing import event_accumulator

# tensorboard.backend.application.logger.setLevel("ERROR")

# Define the path to the events.out files
events_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'source_data_run2')

# Define the names of the algorithms (which are the names of the folders)
algorithms = ['DSAC5','SAC','TD3','DDPG','TRPO','PPO']
on_policy_algorithms = ['PPO','TRPO']
envs = ['gym_ant', 'gym_halfcheetah', 'gym_hopper', 'gym_humanoid', 'gym_inverteddoublependulum','gym_invertedpendulum','gym_reacher', 'gym_swimmer', 'gym_walker2d']
# envs = ['gym_swimmer']
# Define the metrics you want to visusalize
metrics = ['Evaluation/1. TAR-RL iter']
sample_interval = 15_000 # 0.3M
step_fix_factor = 250  # match the step of the on-policy algorithms since they repeat network updates in the same step
max_record_points = 100 # max_record_points * sample_interval = max RL steps(1.5M)
# Create a list to hold the data
data_list = []

def read_tensorboard(path):
    """
    Input dir of tensorboard log.
    """
    ea = event_accumulator.EventAccumulator(path)
    ea.Reload()
    valid_key_list = ea.scalars.Keys()

    event_dict ={}
    for key in valid_key_list:
        if key in metrics:
            event_list = ea.scalars.Items(key)
            event_dict[key] = event_list
    return event_dict


def get_files_path(algorithm,env):
    # get all the path of the files whose name begin with 'events.out' in the algorithm folder
    target_file_list = []
    target_folder = os.path.join(events_path, env,algorithm)
    if os.path.exists(target_folder):
        for files in os.listdir(target_folder):
            if files.startswith('events.out'):
                target_file_list.append(os.path.join(target_folder,files))
    return target_file_list

# Loop through the algorithms
for algorithm in algorithms:
    # Loop through the event files for this algorithm
    for env in envs:
        file_list = get_files_path(algorithm,env)
        for id, file in enumerate(file_list):
            # Load the event file
            event_dict = read_tensorboard(file)
            # Loop through the metrics
            for metric in metrics:
                # Loop through the steps and values for this metric
                data_length = len(event_dict[metric])
                alg_tag= algorithm
                if algorithm == 'DSAC5':
                    alg_tag = 'DSAC'
                record_points_num = 0
                for id, e in enumerate(event_dict[metric]):
                    if record_points_num>= max_record_points:
                        break
                    if algorithm in on_policy_algorithms:
                        step = e.step*step_fix_factor
                    else:
                        step = e.step
                    # Add the data to the list
                    if step >= record_points_num*sample_interval:
                        
                        data_list.append({'algorithm': alg_tag,'env':env, 'run': id, 'step': record_points_num*sample_interval/1_000_000, metric: e.value})
                        record_points_num += 1

# Convert the data to a pandas DataFrame
data_df = pd.DataFrame(data_list)

# Group the data by algorithm, step, and metric, and calculate the mean and standard deviation
data_summary = data_df.groupby(['algorithm', 'step','env'])[metrics].agg([np.mean, np.std]).reset_index()

# Rename the columns to a simpler format
data_summary.columns = ['algorithm', 'step', 'env', 'value_mean', 'value_std']
data_summary['value_std'] = data_summary['value_std'].fillna(0)

# # Reshape the data so that each metric is a separate column
# data_pivot = data_summary.pivot(index='step', columns=['algorithm', 'env'], values=['value_mean', 'value_std'])

# # Flatten the column index to make it easier to work with
# data_pivot.columns = [f'{algorithm}_{env}_{stat}' for algorithm, env, stat in data_pivot.columns]

# Convert the data to JSON format
data_json = json.loads(data_summary.reset_index().to_json(orient='records'))
with open('data_run2.json', "w", encoding="utf-8") as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)
    