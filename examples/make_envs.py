import gym
import fsrl_metadrive

env = gym.make("SafeMetaDrive-easysparse-v0")
print(env.action_space)
env.reset()
for i in range(100): 
    o, r, term, trunc, i = env.step(env.action_space.sample())
    print(r)
env.close()