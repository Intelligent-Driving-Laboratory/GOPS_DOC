import os
import shutil

src_dir = 'result_0419'
dst_dir = 'source_data_run2'

for env in os.listdir(src_dir):
    env_path = os.path.join(src_dir, env)
    if os.path.isdir(env_path):
        for algorithm in os.listdir(env_path):
            algorithm_path = os.path.join(env_path, algorithm)
            if os.path.isdir(algorithm_path):
                new_algorithm = algorithm[:-14] # remove yymmdd from algorithm folder name
                if new_algorithm != 'DSAC5':
                    continue
                new_algorithm_path = os.path.join(dst_dir, env, new_algorithm)
                os.makedirs(new_algorithm_path, exist_ok=True)
                for file in os.listdir(algorithm_path):
                    if file.startswith('events.'):
                        src_file = os.path.join(algorithm_path, file)
                        dst_file = os.path.join(new_algorithm_path, file)
                        shutil.copy2(src_file, dst_file)