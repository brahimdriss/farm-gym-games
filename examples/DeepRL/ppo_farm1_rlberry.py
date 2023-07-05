"""
rlberry PPO on Farm1
====================
"""


import farmgym_games
import numpy as np
from rlberry.envs import gym_make

from rlberry.agents.torch import PPOAgent
from rlberry.manager import AgentManager, evaluate_agents, plot_writer_data
from rlberry.agents.torch.utils.training import model_factory_from_env
import numpy as np

from rlberry.agents.torch.utils.training import model_factory_from_env
import numpy as np
# import logging
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)


policy_configs = {
    "type": "MultiLayerPerceptron",  # A network architecture
    "layer_sizes": (256, 256),  # Network dimensions
    "reshape": False,
    "is_policy": True,
}

value_configs = {
    "type": "MultiLayerPerceptron",
    "layer_sizes": (256, 256),
    "reshape": False,
    "out_size": 1,
}


env_ctor, env_kwargs = gym_make, {"id": "OldV21Farm0-v0"}

if __name__ == "__main__":
    manager = AgentManager(
        PPOAgent,
        (env_ctor, env_kwargs),
        agent_name="PPOAgent",
        init_kwargs=dict(
            policy_net_fn=model_factory_from_env,
            policy_net_kwargs=policy_configs,
            value_net_fn=model_factory_from_env,
            value_net_kwargs=value_configs,
            learning_rate=9e-5,
            n_steps=5 * 365,
            batch_size=365,
            eps_clip=0.2,
        ),
        fit_budget=5e4,
        eval_kwargs=dict(eval_horizon=365),
        n_fit=2,
        parallelization="process",
        mp_context="spawn",
        enable_tensorboard=True,
    )
    manager.fit()
    eval_means = []
    for id_agent in range(2):
        eval_values.append(
                np.mean(manager.eval_agents(100, agent_id=id_agent))
            )
    np.savetxt("ppo_farm1.out", np.array(eval_means), delimiter=",")

