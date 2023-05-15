import pytest
#from rlberry.utils.check_gym_env import check_gym_env
#from farmgym_games import Farm0
from rlberry.agents import AgentWithSimplePolicy

from farmgym_games.game_catalogue.game0_env import Farm0


ALL_ENVS = [Farm0]

# test gym compatibility


@pytest.mark.parametrize("Env", ALL_ENVS)
def test_env(Env):
    check_gym_env(Env())


# test with random agent


class RandomAgent(AgentWithSimplePolicy):
    name = "RandomAgent"

    def __init__(self, env, **kwargs):
        AgentWithSimplePolicy.__init__(self, env, **kwargs)

    def fit(self, budget=100, **kwargs):
        observation = self.env.reset()
        episode_reward = 0
        for ep in range(int(budget)):
            action = self.policy(observation)
            observation, reward, done, _, _ = self.env.step(action)
            episode_reward += reward
            if done:
                self.writer.add_scalar("episode_rewards", episode_reward, ep)
                episode_reward = 0
                self.env.reset()

    def policy(self, observation):
        return self.env.action_space.sample()  # choose an action at random


@pytest.mark.parametrize("Env", ALL_ENVS)
def test_env_agent(Env):
    env = Env()
    agent = RandomAgent(env)
    agent.fit(10)

if __name__ == "__main__":
    env = Farm0()
    #env.farm.understand_the_farm()
    agent = RandomAgent(env)
    agent.fit(10)