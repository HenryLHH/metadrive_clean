from gym.envs.registration import register, registry
from metadrive.fsrl_metadrive.envs.envs import SafeMetaDriveEnv_FSRL


safe_metadrive_environment_dict = {
    "SafeMetaDrive-easysparse-v0": {
        "start_seed": 0,
        "traffic_density": 0.1, 
        "map": 3, 
        "map_config": {"type": "block_sequence", "config": "SCS"}, 
        "accident_prob": 0.0,
        "environment_num": 1, 
        "horizon": 1000,
        # "agent_policy": IDMPolicy_CustomSpeed,
        # "idm_target_speed": 30,
        # "idm_acc_factor": 1.0,
        # "idm_deacc_factor": 5.0,
    }, 
    "SafeMetaDrive-mediumsparse-v0": {
        "start_seed": 100, 
        "traffic_density": 0.1,
        "map": 3,
        "map_config": {"type": "block_sequence", "config": "XST"}, 
        "accident_prob": 0.0,
        "environment_num": 1,
        "horizon": 1000,
    }, 
    "SafeMetaDrive-hardsparse-v0": {
        "start_seed": 200, 
        "traffic_density": 0.1,
        "map": 3,
        "map_config": {"type": "block_sequence", "config": "TRO"}, 
        "accident_prob": 0.0,
        "environment_num": 1,
        "horizon": 1000,
    }, 
    "SafeMetaDrive-easymean-v0": {
        "start_seed": 0, 
        "traffic_density": 0.15,
        "map": 3,
        "map_config": {"type": "block_sequence", "config": "SCS"}, 
        "accident_prob": 0.0,
        "environment_num": 1,
        "horizon": 1000,
    }, 
    "SafeMetaDrive-mediummean-v0": {
        "start_seed": 100, 
        "traffic_density": 0.15,
        "map": 3,
        "map_config": {"type": "block_sequence", "config": "XST"}, 
        "accident_prob": 0.0,
        "environment_num": 1,
        "horizon": 1000,
    }, 
    "SafeMetaDrive-hardmean-v0": {
        "start_seed": 200, 
        "traffic_density": 0.15,
        "map": 3,
        "map_config": {"type": "block_sequence", "config": "TRO"}, 
        "accident_prob": 0.0,
        "environment_num": 1,
    }, 
    "SafeMetaDrive-easydense-v0": {
        "start_seed": 0, 
        "traffic_density": 0.2,
        "map": 3,
        "map_config": {"type": "block_sequence", "config": "SCS"}, 
        "accident_prob": 0.0,
        "environment_num": 1,
        "horizon": 1000,
    }, 
    "SafeMetaDrive-mediumdense-v0": {
        "start_seed": 100, 
        "traffic_density": 0.2,
        "map": 3,
        "map_config": {"type": "block_sequence", "config": "XST"}, 
        "accident_prob": 0.0,
        "environment_num": 1,
        "horizon": 1000,
    }, 
    "SafeMetaDrive-harddense-v0": {
        "start_seed": 200, 
        "traffic_density": 0.2,
        "map": 3,
        "map_config": {"type": "block_sequence", "config": "TRO"}, 
        "accident_prob": 0.0,
        "environment_num": 1,
        "horizon": 1000,
    }, 
}

for env_name, env_config in safe_metadrive_environment_dict.items():
    register(id=env_name, entry_point=SafeMetaDriveEnv_FSRL, kwargs=dict(config=env_config))
