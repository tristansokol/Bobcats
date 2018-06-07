# Bobcats
Code used for the [OpenAI Retro Contest](https://contest.openai.com/)
Read more about Team Bobcats' journey in the *eleven* part blog series:

* Day 1: Getting the Basics Set Up

* Day 3: Running the Jerk Agent

* Days 4 & 5: Getting TensorFlow &  Docker to work on my MacBook

* Day 6: Playback Tooling for .bk2 files

* Days 9 &10: Failing with the Rainbow DQN baseline code.

* Days 11–14: Reading the PPO2 code

* Days 16–18: Running the PPO2 baseline code, and failing at TensorFlow & Docker optimization.

* Days 22–25: A Deep Dive into the Jerk Agent

* Days 26–29: Visualizing batches of sonic runs

* Days 38–53: Discovering Q-Learning

* TODO - last post. 

The explanation of the final code ( and the submission for the contest) can be found in [improved-jerk.md](improved-jerk.md)

A list of the different tools that I made in the process can be found here: https://gist.github.com/tristansokol/062b1d509e2e8e6e250a30ae09928a58

All of the code is pretty much exactly the same as the final state of my working repository with the redactions of failed Q-learning model weights, an image of the sonic level (for copyright concerns) and the sonic roms. The top level folders each represent a different agent attempt with our final agent being `jerk_agent_for_understanding/jerk_agent.py`.

Much of the code is adapted from [openai/retro-baselines](https://github.com/openai/retro-baselines) which is [Copyrighted by OpenAI](https://github.com/openai/retro-baselines/blob/master/LICENSE)