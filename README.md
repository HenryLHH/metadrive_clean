# fsrl_metadrive


We provide nine different safe driving environments in metadrive, named as: `SafeMetaDrive-{Road}{Vehicle}-v0`,
where {Road} includes three different levels for self-driving cars: easy, medium, hard, {Vehicle} includes four different levels of surrounding traffic: sparse, mean, dense. 

## 1. Set up the environments: 
```
# set up metadrive
git clone --recursive https://github.com/HenryLHH/metadrive_clean.git
cd metadrive_clean
pip3 install -e .

# set up fsrl_metadrive
git clone https://github.com/HenryLHH/fsrl_metadrive.git
cd fsrl_metadrive/
pip3 install -e .
```

## 2. MetaDrive Safe Environment import

```
import gym
import fsrl_metadrive

env = gym.make("SafeMetaDrive-easysparse-v0")
```


## 3. MetaDrive data collection for fsrl



### 3.1. Run collecting the dataset:
```
bash run_collect.sh [your_env_name]
```

e.g. 
```
bash run_collect.sh SafeMetaDrive-harddense-v0
```

### 3.2 Visualize the collected dataset:
```
bash run_visualize.sh [your_env_name]
```

e.g. 
```
bash run_collect.sh SafeMetaDrive-harddense-v0
```

The cost-reward plot will be saved in `figs/` folder. 