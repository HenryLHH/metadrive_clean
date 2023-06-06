import os
import h5py
import argparse
import numpy as np

from tianshou.data.utils.converter import to_hdf5, from_hdf5
from matplotlib import pyplot as plt

def get_parser(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", type=str, default="metadrive_dataset", help="train/test")
    parser.add_argument("--env_id", type=str, default="SafeMetaDrive-easysparse-v0", help="train/test")
    
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    filename = os.path.join(args.filepath, args.env_id+".hdf5")
    os.makedirs("figs/", exist_ok=True)
    os.makedirs(args.filepath+'_post', exist_ok=True)
    
    with h5py.File(filename, "r") as f: 
        data = from_hdf5(f)
    idx = np.where(np.logical_or(data["terminals"], data["timeouts"]))[0]
    rew_list, cost_list = [], []
    for i in range(len(idx)): 
        if i == 0: 
            rewards = np.sum(data["rewards"][0:idx[0]+1])
            costs = np.sum(data["costs"][0:idx[0]+1])
        else: 
            rewards = np.sum(data["rewards"][idx[i-1]+1:idx[i]+1])
            costs = np.sum(data["costs"][idx[i-1]+1:idx[i]+1])
        rew_list.append(rewards)
        cost_list.append(costs)
    print('===============stats==================')
    print('min rewards: {:.1f}'.format(np.min(rew_list)))
    print('max rewards: {:.1f}'.format(np.max(rew_list)))
    print('avg rewards: {:.1f}'.format(np.mean(rew_list)))
    print('min costs: {:.1f}'.format(np.min(cost_list)))
    print('max costs: {:.1f}'.format(np.max(cost_list)))
    print('avg costs: {:.1f}'.format(np.mean(cost_list)))
    
    cost_max_round = int((np.floor(np.max(cost_list)) // 5+1) * 5)
    print(cost_max_round)
    filename_resave = os.path.join(args.filepath+'_post', args.env_id+"-"+str(cost_max_round)+"-"+str(len(idx))+".hdf5")
    with h5py.File(filename_resave, "w") as f: 
        to_hdf5(data, f, compression='gzip')
    
        
    plt.scatter(cost_list, rew_list, s=3)
    plt.xlabel('Episodic Cost')
    plt.xlabel('Episodic Reward')
    plt.savefig(os.path.join("figs", args.env_id))
    