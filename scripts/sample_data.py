import gym
import numpy as np
from tqdm import trange, tqdm
from matplotlib import pyplot as plt
import argparse
from tianshou.data import Batch, ReplayBuffer, to_numpy
from fsrl.data.traj_buf import TrajectoryBuffer
from metadrive.fsrl_metadrive import safe_metadrive_environment_dict
from metadrive.fsrl_metadrive.policy.idm_policy import IDMPolicy_CustomSpeed


def get_parser(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--env_id", type=str, default="SafeMetaDrive-easysparse-v0", help="train/test")
    parser.add_argument("--env_num", type=int, default=1, help="num of environments")
    parser.add_argument("--ep_num", type=int, default=20, help="number of episodes")
    parser.add_argument("--log", type=str, default="debug", help="reward-cost plot name")
    
    return parser
    
def sample_traj(traj_buffer, env_name, speed, acc, env_num=1, ep_num=100): 
    data = Batch(
            obs={},
            act={},
            rew={},
            cost={},
            out_of_road_cost={}, 
            crash_cost={},
            proximity_cost={}, 
            velocity_cost={},
            terminated={},
            truncated={},
            done={},
            obs_next={},
            info={}
    )
    
    rew_list, cost_list = [],[]
    rew, cost = 0, 0
    count_ep = 0
    default_config = safe_metadrive_environment_dict[env_name]
    
    default_config.update({"idm_target_speed": speed, 
                           "idm_acc_factor": acc, 
                           "environment_num": env_num, 
                            "agent_policy": IDMPolicy_CustomSpeed,
                            })
    
    env = gym.make(env_name, config=default_config)
    obs = env.reset()        
    data.update(obs=[obs])

    pbar = tqdm(total=ep_num)
    while True: 
        obs_next, r, terminated, truncated, info = env.step(env.action_space.sample())
        done = np.logical_or(terminated, truncated)        
        rew += r
        cost += info["cost"]
        
        data.update(
            act=info["raw_action"],
            obs_next=[obs_next],
            rew=[r],
            terminated=[terminated],
            truncated=[truncated],
            done=[done],
            cost=[info["cost"]],
            proximity_cost=[info["proximity_cost"]], 
            velocity_cost=[info["velocity_cost"]], 
            crash_cost = [info["crash_cost"]], 
            out_of_road_cost = [info["out_of_road_cost"]], 
            info=[info]
        )
        
        traj_data = Batch(
            observations=data.obs,
            next_observations=data.obs_next,
            actions=[data.act],
            rewards=data.rew,
            costs=data.cost,
            proximity_costs=data.proximity_cost,
            velocity_costs=data.velocity_cost,
            crash_costs=data.crash_cost,
            out_of_road_costs=data.out_of_road_cost,
            terminals=data.terminated,
            timeouts=data.truncated
        )
        
        traj_buffer.store(traj_data)
        data.obs = data.obs_next
                
        if done: 
            obs = env.reset()
            data.update(obs=[obs])
            rew_list.append(rew)
            cost_list.append(cost)
            rew, cost = 0., 0.
            count_ep += 1
            pbar.update(1)
            if count_ep >= ep_num: 
                break
    
    pbar.close()
    env.close()
    return traj_buffer
    # return cost_list, rew_list

if __name__ == "__main__": 
    args = get_parser().parse_args()

    traj_buffer = TrajectoryBuffer(max_trajectory=1000)
    
    rew_list_all = []
    cost_list_all = []
    for acc in np.arange(0, 6.0, 0.6):
        for speed in range(5, 25, 4): 
            print("==================speed: {:02d}=====================".format(speed))
            traj_buffer = sample_traj(traj_buffer, args.env_id, speed, acc, args.env_num, args.ep_num)
            print(len(traj_buffer))
            traj_buffer.save('metadrive_dataset', args.env_id+'.hdf5')
    plt.legend()
    plt.savefig(args.log)
    
    