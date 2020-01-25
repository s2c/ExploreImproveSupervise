from gym.envs.registration import register

register(
    id='EIS-v0',
    entry_point='EIS.envs:EISEnv',
)
