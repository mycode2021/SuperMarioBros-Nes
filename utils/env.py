from collections import deque
from gym import spaces
from retro import make
import cv2, gym, numpy as np, utils


class ActionsDiscretizer(gym.ActionWrapper):
    def __init__(self, env, actions):
        super(ActionsDiscretizer, self).__init__(env)
        buttons = env.buttons
        self._actions = []
        for action in actions:
            arr = np.array([False]*len(buttons))
            for button in action:
                arr[buttons.index(button)] = True
            self._actions.append(arr)
        self.action_space = spaces.Discrete(len(self._actions))

    def action(self, action):
        return self._actions[action].copy()

class ProcessFrame(gym.ObservationWrapper):
    def __init__(self, env, width=84, height=84):
        super(ProcessFrame, self).__init__(env)
        self.observation_space = spaces.Box(low=0, high=255, shape=(1, width, height))
        self.shape = width, height

    def observation(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = cv2.resize(frame, self.shape, interpolation=cv2.INTER_AREA)
        frame = frame[None, :, :]
        return frame

class AllowBacktracking(gym.Wrapper):
    def __init__(self, env, width=84, height=84, skip=4):
        super(AllowBacktracking, self).__init__(env)
        self.observation_space = spaces.Box(low=0, high=255, shape=(skip, width, height))
        self.states = deque(np.zeros((skip, width, height), dtype=np.float32), maxlen=4)
        self.skip, self.xscroll, self.coins = skip, 0, 0

    def step(self, action):
        total_reward, state_buffer = 0, deque(maxlen=2)
        for _ in range(self.skip):
            state, reward, done, info = self.env.step(action)
            total_reward += reward
            curr_xscroll = info["xscrollHi"] * 256 + info["xscrollLo"]
            total_reward += abs(curr_xscroll-self.xscroll) * 15.0
            self.xscroll = curr_xscroll
            total_reward += (info["coins"]-self.coins) * 20.0
            self.coins = info["coins"]
            state_buffer.append(state)
            if done: break
        else:
            self.states.append(np.max(np.concatenate(state_buffer, 0), 0))
        del state_buffer
        return np.array(self.states)[None, :, :, :].astype(np.float32), \
               np.clip(total_reward, -300, 300), done, info

    def reset(self, **kwargs):
        self.xscroll, self.coins = 0, 0
        state = self.env.reset(**kwargs)
        self.states.extend(np.concatenate([state for _ in range(self.skip)], 0))
        return np.array(self.states)[None, :, :, :].astype(np.float32)

class RewardScaler(gym.RewardWrapper):
    def __init__(self, env, scale=0.005):
        super(RewardScaler, self).__init__(env)
        self.scale = scale

    def reward(self, reward):
        return reward * self.scale

class MarioWinner(gym.Wrapper):
    def __init__(self, env):
        super(MarioWinner, self).__init__(env)
        self.actions = deque(maxlen=300)
        self.levelLo, self.levelHi, self.lives, self.finish = 0, 0, 0, None

    def step(self, action):
        state, reward, done, info = self.env.step(action)
        self.actions.append(action)
        if self.finish == None:
            self.lives, self.levelLo, self.levelHi = info["lives"], info["levelLo"], info["levelHi"]
            self.finish = lambda levelLo, levelHi: levelLo != self.levelLo or levelHi != self.levelHi
        self.lives = max(self.lives, info["lives"])
        info["finish"] = self.finish(info["levelLo"], info["levelHi"])
        done |= self.actions.count(action) == self.actions.maxlen \
            or info["finish"] or info["lives"] < self.lives
        if done:
            if info["finish"]:
                reward += 1000
            else:
                reward += -10
        return state, reward, done, info

    def reset(self, **kwargs):
        self.actions.clear()
        self.levelLo, self.levelHi, self.lives, self.finish = 0, 0, 0, None
        return self.env.reset(**kwargs)


def create_runtime_env(game, state, action_type, record=False):
    actions = utils.Actions.get(action_type)
    assert actions, "Invalid action type."
    env = make(game, state, record=record)
    env = ActionsDiscretizer(env, actions)
    env = ProcessFrame(env)
    env = AllowBacktracking(env)
    env = RewardScaler(env)
    env = MarioWinner(env)
    return env, env.observation_space.shape[0], len(actions)
