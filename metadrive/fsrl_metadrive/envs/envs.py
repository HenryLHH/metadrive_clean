import numpy as np
from metadrive.envs import SafeMetaDriveEnv
from metadrive.constants import TerminationState
from metadrive.manager.traffic_manager import TrafficMode

class SafeMetaDriveEnv_FSRL(SafeMetaDriveEnv): 

    def default_config(self):
        config = super(SafeMetaDriveEnv_FSRL, self).default_config()
        config.update(
            {
                "idm_target_speed": 30,
                "idm_acc_factor": 1.0, 
                "idm_deacc_factor": 5.0, 
                "crash_vehicle_penalty": 0.0,
                "random_traffic": True,
                "traffic_mode": TrafficMode.Hybrid
            },
            allow_add_new_key=True
        )
        return config


    def done_function(self, vehicle_id: str):
        done, done_info = super(SafeMetaDriveEnv_FSRL, self).done_function(vehicle_id)
        
        if done_info[TerminationState.MAX_STEP]:
            done = True
        
        return done, done_info

    def step(self, actions):
        o, r, d, i = super(SafeMetaDriveEnv_FSRL, self).step(actions)
        i["velocity_cost"] = max(0, 1e-2*(i["velocity"]-10.))
        i["cost"] += i["velocity_cost"]
        i["proximity_cost"] = 1e-2*max(0, 0.1-np.min(o[-240:]))**2
        i["cost"] += i["proximity_cost"]
        
        i["out_of_road_cost"] = self.config["out_of_road_cost"] if i["out_of_road"] else 0
        i["crash_cost"] = self.config["crash_vehicle_cost"] if i["crash"] else 0
        
        if i["max_step"]: 
            truncated = True
        else: 
            truncated = False
        if i["arrive_dest"] or i["crash"] or i["out_of_road"]: 
            terminated = True
        else: 
            terminated = False
        return o, r, terminated, truncated, i