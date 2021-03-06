#!/usr/bin/env python

"""
A scripted agent called "Just Enough Retained Knowledge".
"""

import random
import math
import sys
import gym
import numpy as np
# from sonic_util import AllowBacktracking, make_env

import gym_remote.client as grc
import gym_remote.exceptions as gre

EXPLOIT_BIAS = 0.12 # 0.25
TOTAL_TIMESTEPS = int(1e6)


def main():
    # Set up a new TrackedEnv that can keep track of total timestamps and store
    # previous best solutions.
    env = grc.RemoteEnv('tmp/sock')
    env = TrackedEnv(env)

    # new_ep will keep track of if a new episode should be started.
    new_ep = True
    # solutions is an array of successful gameplay sequences as well as the
    # total reward earned from them.
    solutions = []
    best_run = 0
    while True:
        if new_ep:
            if (solutions):
                current = [np.mean(x[0]) for x in solutions]
                print('%f%% done, reward: %f' %
                      (env.total_steps_ever/10000, np.mean(current)))

            if (solutions and
                    random.random() < EXPLOIT_BIAS + env.total_steps_ever / TOTAL_TIMESTEPS + best_run/10000):
                    # random.random() < best_run/10000): #11
                    # random.random() < math.pow(best_run/10000,2) + env.total_steps_ever / TOTAL_TIMESTEPS): #12
                solutions = sorted(solutions, key=lambda x: np.mean(x[0]))
                best_pair = solutions[-1]
                best_run = np.mean(best_pair[0])
                new_rew = exploit(env, best_pair[1])
                best_pair[0].append(new_rew)
                # print('replayed best with reward %f' % new_rew)
                continue
            else:
                env.reset()
                new_ep = False
        rew, new_ep = move(env, 100)
        if not new_ep and rew <= 0:
            # print('backtracking due to negative reward: %f' % rew)
            _, new_ep = move(env, 45, left=True)
        if new_ep:
            solutions.append(([max(env.reward_history)], env.best_sequence()))


def move(env, num_steps, left=False, jump_prob=1.0 / 10.0, jump_repeat=4):
    """
    Move right or left for a certain number of steps,
    jumping periodically.
    """
    total_rew = 0.0
    done = False
    steps_taken = 0
    jumping_steps_left = 0
    while not done and steps_taken < num_steps:
        #["B", "A", "MODE", "START", "UP", "DOWN", "LEFT", "RIGHT", "C", "Y", "X", "Z"]
        action = np.zeros((12,), dtype=np.bool)
        action[6] = left
        action[7] = not left
        if jumping_steps_left > 0:
            action[0] = True
            jumping_steps_left -= 1
        else:
            if random.random() < jump_prob:
                jumping_steps_left = jump_repeat - 1
                action[0] = True
        # no info variable in contest variable
        obs, rew, done, _ = env.step(action)
        total_rew += rew
        steps_taken += 1
        if done:
            break
    return total_rew, done


def exploit(env, sequence):
    """
    Replay an action sequence; pad with NOPs if needed.

    Returns the final cumulative reward.
    """
    env.reset()
    done = False
    idx = 0
    rew = 0
    try:
        while not done:
            if idx >= len(sequence):
                # _, _, done, _ = env.step(np.zeros((12,), dtype='bool'))
                if  rew <= 0:
                    rew, done = move(env, 45, left=True)
                    # print(rew, done)
                    # done = True
                    # return env.total_reward
                else:
                    rew, done = move(env, 100)
            else:
                _, rew, done, _ = env.step(sequence[idx])
            idx += 1
    except:
        print("hello")
        print(sys.exc_info()[0])
        exit()
    return env.total_reward


class TrackedEnv(gym.Wrapper):
    """
    An environment that tracks the current trajectory and
    the total number of timesteps ever taken.
    """

    def __init__(self, env):
        super(TrackedEnv, self).__init__(env)
        self.action_history = []
        self.reward_history = []
        self.total_reward = 0
        self.total_steps_ever = 0

    def best_sequence(self):
        """
        Get the prefix of the trajectory with the best
        cumulative reward.
        """
        max_cumulative = max(self.reward_history)
        for i, rew in enumerate(self.reward_history):
            if rew == max_cumulative:
                return self.action_history[:i+1]
        raise RuntimeError('unreachable')

    # pylint: disable=E0202
    def reset(self, **kwargs):
        self.action_history = []
        self.reward_history = []
        self.total_reward = 0
        return self.env.reset(**kwargs)

    def step(self, action):
        self.total_steps_ever += 1
        self.action_history.append(action.copy())
        obs, rew, done, info = self.env.step(action)
        self.total_reward += rew
        self.reward_history.append(self.total_reward)
        return obs, rew, done, info


if __name__ == '__main__':
    try:
        main()
    except gre.GymRemoteError as exc:
        print('exception', exc)
