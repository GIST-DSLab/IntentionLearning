import json
import os
import glob
import argparse


def extract_tools_from_json(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tools_sequence = [
        step["action"]["tool"]
        for step in data["action_sequence"]["action_sequence"]
        if step["action"]["tool"] != "none"
    ]
    
    return tools_sequence


def process_directory(base_dir):
    unique_trajectories = {}
    results = []

    subdirs = [d for d in glob.glob(os.path.join(base_dir, "trace_*")) if os.path.isdir(d)]

    if subdirs:
        for trace_dir in sorted(subdirs):
            json_files = sorted(glob.glob(os.path.join(trace_dir, "*.json")))
            if not json_files:
                continue

            full_trajectory = []
            for json_file in json_files:
                tools_sequence = extract_tools_from_json(json_file)
                if not tools_sequence:
                    continue

                if not full_trajectory:
                    full_trajectory.extend(tools_sequence)
                else:
                    full_trajectory.append(tools_sequence[-1])

            trace_name = os.path.basename(trace_dir)
            if full_trajectory and full_trajectory[0] == "start" and full_trajectory[-1] == "end":
                traj_tuple = tuple(full_trajectory)
                if traj_tuple not in unique_trajectories:
                    unique_trajectories[traj_tuple] = []
                    results.append(full_trajectory)

                unique_trajectories[traj_tuple].append(trace_name)
    
    else:
        for json_file in sorted(glob.glob(os.path.join(base_dir, "*.json"))):
            full_trajectory = extract_tools_from_json(json_file)
            file_name = os.path.basename(json_file)

            if not full_trajectory:
                continue

            if full_trajectory[0] != "start" or full_trajectory[-1] != "end":
                continue

            traj_tuple = tuple(full_trajectory)
            if traj_tuple not in unique_trajectories:
                unique_trajectories[traj_tuple] = []
                results.append(full_trajectory)

            unique_trajectories[traj_tuple].append(file_name)

    return results, unique_trajectories


def map_to_intention_trajectory(task_name, unique_trajectories):
    trajectory_to_intention = dict()

    trajectory_to_intention['dflip'] = {
        ('start', 'rotate', 'rotate', 'reflectx', 'rotate', 'rotate', 'rotate', 'end'): 
            [(0, 1), (1, 2), (2, 5), (2, 5), (5, 3), (5, 3), (3, 6), (6, 7)],

        ('start', 'rotate', 'reflecty', 'end'): 
            [(0, 1), (1, 2), (2, 6), (6, 7)],

        ('start', 'reflectx', 'reflecty', 'rotate', 'reflectx', 'end'): 
            [(0, 1), (1, 3), (3, 4), (3, 4), (4, 6), (6, 7)],

        ('start', 'reflecty', 'reflectx', 'rotate', 'reflectx', 'end'): 
            [(0, 1), (1, 5), (5, 4), (5, 4), (4, 6), (6, 7)],

        ('start', 'reflectx', 'reflectx', 'rotate', 'reflecty', 'end'): 
            [(0, 1), (1, 3), (3, 1), (1, 2), (2, 6), (6, 7)],

        ('start', 'rotate', 'rotate', 'reflecty', 'rotate', 'end'): 
            [(0, 1), (1, 2), (2, 3), (2, 3), (3, 6), (6, 7)],

        ('start', 'rotate', 'reflectx', 'rotate', 'rotate', 'end'): 
            [(0, 1), (1, 2), (2, 3), (2, 3), (3, 6), (6, 7)],

        ('start', 'reflectx', 'rotate', 'end'): 
            [(0, 1), (1, 3), (3, 6), (6, 7)],

        ('start', 'rotate', 'rotate', 'rotate', 'reflectx', 'end'): 
            [(0, 1), (1, 2), (2, 4), (2, 4), (4, 6), (6, 7)],

        ('start', 'reflecty', 'rotate', 'rotate', 'rotate', 'end'): 
            [(0, 1), (1, 5), (5, 3), (5, 3), (3, 6), (6, 7)],

        ('start', 'end'): 
            [(0, 1), (6, 7)],
    }

    trajectory_to_intention['stretch'] = {
        ('start', 'translate', 'translate', 'translate', 'select_fill', 'select_fill', 'select_fill', 'end'): 
            [(0, 3), (3, 4), (3, 4), (4, 6), (4, 6), (6, 8), (6, 8), (8, 9)],

        ('start', 'translate', 'translate', 'select_fill', 'select_fill', 'end'):
            [(0, 5), (5, 6), (5, 6), (6, 8), (6, 8), (8, 9)],

        ('start', 'translate', 'select_fill', 'translate', 'select_fill', 'end'): 
            [(0, 5), (5, 7), (5, 7), (7, 8), (7, 8), (8, 9)],

        ('start', 'translate', 'select_fill', 'translate', 'select_fill', 'translate', 'select_fill', 'end'): 
            [(0, 3), (3, 5), (3, 5), (5, 7), (5, 7), (7, 8), (7, 8), (8, 9)],

        ('start', 'translate', 'select_fill', 'translate', 'select_fill', 'translate', 'select_fill', 'translate', 'select_fill', 'end'): 
            [(0, 1), (1, 3), (1, 3), (3, 5), (3, 5), (5, 7), (5, 7), (7, 8), (7, 8), (8, 9)],

        ('start', 'translate', 'translate', 'select_fill', 'select_fill', 'translate', 'select_fill', 'end'): 
            [(0, 3), (3, 4), (3, 4), (4, 7), (4, 7), (7, 8), (7, 8), (8, 9)],

        ('start', 'translate', 'translate', 'select_fill', 'select_fill', 'translate', 'translate', 'select_fill', 'select_fill', 'end'): 
            [(0, 1), (1, 2), (1, 2), (2, 5), (2, 5), (5, 6), (5, 6), (6, 8), (6, 8), (8, 9)],

        ('start', 'translate', 'translate', 'translate', 'select_fill', 'select_fill', 'select_fill', 'translate', 'select_fill', 'end'): 
            [(0, 1), (1, 2), (1, 2), (2, 4), (2, 4), (4, 7), (4, 7), (7, 8), (7, 8), (8, 9)],

        ('start', 'translate', 'translate', 'translate', 'translate', 'select_fill', 'select_fill', 'select_fill', 'select_fill', 'end'): 
            [(0, 1), (1, 2), (1, 2), (2, 6), (2, 6), (2, 6), (2, 6), (6, 8), (6, 8), (8, 9)],

        ('start', 'end'):  # for test dataset (only start and end action pair is provided)
            [(0, 1), (8, 9)],
    }

    return {tuple(traj): trajectory_to_intention[task_name].get(tuple(traj), None) for traj in unique_trajectories}


def modify_json_with_intentions(base_dir, trajectory_mapping, intention_mapping):
    json_files = []
    subdirs = [d for d in glob.glob(os.path.join(base_dir, "trace_*")) if os.path.isdir(d)]

    if subdirs:
        for trace_dir in subdirs:
            json_files.extend(sorted(glob.glob(os.path.join(trace_dir, "*.json"))))
    else:
        json_files = sorted(glob.glob(os.path.join(base_dir, "*.json")))

    for json_file in json_files:
        file_name = os.path.basename(json_file)

        trajectory = next((t for t, files in trajectory_mapping.items() if file_name in files), None)
        if trajectory is None:
            file_name = '_'.join(file_name.split('_')[:2])
            trajectory = next((t for t, files in trajectory_mapping.items() if file_name in files), None)
        if trajectory is None:
            print(f"Warning: No trajectory found for {file_name}")
            continue

        intention_trajectory = intention_mapping.get(trajectory, None)
        if intention_trajectory is None:
            print(f"Warning: No intention mapping found for {file_name}")
            continue

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for action_data in data["action_sequence"]["action_sequence"]:
            tool = action_data["action"]["tool"]
            time_step = action_data["time_step"]

            if tool == "none":
                action_data["intention"] = (0, 0)
            else:
                step_index = min(time_step, len(intention_trajectory) - 1)
                action_data["intention"] = intention_trajectory[step_index]

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, separators=(",", ": "))

        print(f"Updated {json_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str, default="./dataset/")
    parser.add_argument("task_name", type=str, default="dflip")
    parser.add_argument("train_or_test", type=str, default="train")

    args = parser.parse_args()

    dataset_dir = args.base_dir + "/" + args.task_name + "/" + args.train_or_test + "/"

    reconstructed_trajectories, trajectory_mapping = process_directory(dataset_dir)
    intention_mapping = map_to_intention_trajectory(args.task_name, reconstructed_trajectories)

    # Checking Unique Trajectories
    '''
    print(f"{len(reconstructed_trajectories)} Unique Trajectories Exist\n")
    for traj in reconstructed_trajectories:
        print("(%d)" % len(trajectory_mapping[tuple(traj)]), end=': (')
        for act in traj:
            print("'%s'" % act, end=', ')
        print('):')

        for i in range(min(3, len(trajectory_mapping[tuple(traj)]))):
            print("\t", trajectory_mapping[tuple(traj)][i], end="")
        print()
    '''

    modify_json_with_intentions(dataset_dir, trajectory_mapping, intention_mapping)

    print("All JSON files updated with intention values.")
