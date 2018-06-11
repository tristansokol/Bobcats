# Bobcats
Code used for the [OpenAI Retro Contest](https://contest.openai.com/)
Read more about Team Bobcats' journey in the *eleven* part blog series:

* [Day 1: Getting the Basics Set Up](https://medium.com/@tristansokol/day-one-of-the-openai-retro-contest-1651ddcd6aa5)

* [Day 3: Running the Jerk Agent](https://medium.com/@tristansokol/openai-retro-contest-day-3-7a75289a1c9c)

* [Days 4 & 5: Getting TensorFlow &  Docker to work on my MacBook](https://medium.com/@tristansokol/day-4-5-of-the-openai-retro-contest-a3e36e04d467)

* [Day 6: Playback Tooling for .bk2 files](https://medium.com/@tristansokol/day-6-of-the-openai-retro-contest-playback-tooling-3844ba655919)

* [Days 9 & 10: Failing with the Rainbow DQN baseline code.](https://medium.com/@tristansokol/days-9-10-of-the-openai-retro-contest-e8352ea6aafb)

* [Days 11–14: Reading the PPO2 code](https://medium.com/@tristansokol/day-11-ac14a299e69d)

* [Days 16–18: Running the PPO2 baseline code, and failing at TensorFlow & Docker optimization.](https://medium.com/@tristansokol/running-the-ppo-baseline-and-giving-up-on-local-evaluation-1c7d171e5bc8)

* [Days 22–25: A Deep Dive into the Jerk Agent](https://medium.com/@tristansokol/a-deep-dive-into-the-jerk-agent-3c553dbab442)

* [Days 26–29: Visualizing batches of sonic runs](https://medium.com/@tristansokol/making-fun-visuals-history-maps-and-other-tool-improvements-eb5ffe187fd3)

* [Days 38–53: Discovering Q-Learning](https://medium.com/@tristansokol/discovering-q-learning-f7780a77b927)

* [My final submission: the improved JERK agent](https://medium.com/@tristansokol/my-final-submission-the-improved-jerk-724bb54555ee)

The explanation of the final code ( and the submission for the contest) can be found in [improved-jerk.md](improved-jerk.md)

A list of the different tools that I made in the process can be found here: https://gist.github.com/tristansokol/062b1d509e2e8e6e250a30ae09928a58

All of the code is pretty much exactly the same as the final state of my working repository with the redactions of failed Q-learning model weights, an image of the sonic level and the sonic roms (for copyright concerns). The top level folders each represent a different agent attempt with our final agent being `jerk_agent_for_understanding/jerk_agent.py`.

Much of the code is adapted from [openai/retro-baselines](https://github.com/openai/retro-baselines) which is [Copyrighted by OpenAI](https://github.com/openai/retro-baselines/blob/master/LICENSE)