# The Improved Jerk Agent

The Jerk agent was a provided baseline for the [OpenAI Retro Contest](https://contest.openai.com/), you can find the original code in [openai/retro-baselines](https://github.com/openai/retro-baselines/blob/master/agents/jerk_agent.py). Throughout the contest I was able to make some useful improvements to the baseline agent, ultimately falling short of winning the contest, but ended up in the top 30 of the 200+ contestants. This is an explanation of how the improved-jerk agent works.

## Background

The improved JERK agent is an AI agent for reinforcement learning that uses a combination of random exploration and episode exploitation to solve and optimise solutions to episode. Initially the agent explores the environment somewhat randomly until an episode ends, then with a previous solution stored, continues to explore as well as repeat the best existing solution.

Here are definitions of some of the terms that I'll be using in case you are not familar: 

* **Episode** a set of timesteps, actions, and rewards that defines a discreet engagement of the agent with the environment. For this code, an episode is a level of Sonic the Hedgehog gameplay, it starts when the level begins, and ends whenever Sonic dies, reaches the end, or runs out of time.

* **Action** This is a an input the agent applies to the evironment. With our Sega Genesis version of Sonic, these correspond to a button press of the 12 buttoned Genesis controller. In our code they are represented by an array of 12 booleans `[False False False False False False False False False False False False]` corresponding to `[B, A, MODE, START, UP, DOWN, LEFT, RIGHT, C, Y, X, Z]`

TODO Diagram of flowchart describing

start a new episode
 - if exploit & solutions
   - replay best run
else start a new run
 move and backtrack

Lets take a look at each of those parts

### Moving
```python
move(env, num_steps, left, jump_prob, jump_repeat)
```

When the agent begins, it starts by taking a fresh episode and exploring it with the `move()` function. This function first sets up some variables to store the in-process responses from the environment before it starts interacting with the environment passed in with `env`:

```python
total_rew = 0.0 # the reward from all actions in this call of move
done = False # whether or not the episode has finished
steps_taken = 0 # a counter for the number of actions taken
jumping_steps_left = 0
```
Then it enters a loop that iterates through for the total number of num_steps that move() was called with.

The first thing that happens inside that loop is the creation of an an empty boolean array that will hold the value of the action to take. To play sonic, you generally win by moving to the right to find the end of the level. We take advantage of this by designing the move function to always move the right, (or left in the case of back tracking that we will get to later). In the code this is achieved by assigning the 6th and 7th entries of our action array based on whether `move()` was called with the parameter `Left` being true. That means for this agent, every move is either going left or right, no standing still or just vertical jumping.

 After that there is some logic to control jumping. There are two variables that control jumping behavior, the `jump_prob` and `jump_repeat`. `jump_prob` is the probability that for a given step, action[0] (the B button) will be set to true which will execute a jump in the game. For the default agent, the move() function is called in groups of 100 steps, so roughly 10 of them will include jumping, if it were not for `jump_repeat`. `jump_repeat` limits the number of times that you can have a jump inside the move() function, with a default of four, so if you are doing 100 steps, you will only have four jumps within those steps.

With our actions in place ( move right or left, possibly jump as well) we can apply our button presses to the environment.

`_, rew, done, _ = env.step(action)`
The env.step function (as documented [here](https://github.com/openai/retro/blob/master/retro/retro_env.py#L145)) takes the array of actions that would be the moves for our controller and returns four variables, two of which we will use:

`rew` this is the incremental reward achieved from executing this command. The reward in our environment is determined how far from left to right the agent has controlled Sonic to go. 
`done` is a boolean value just describing if the game is over, either through sonic dying, timing out or getting to the end.

The reward (`rew`) gets added to a total_rew which stores the total amount of reward for that invocation of the `move()` function. After all of the actions/steps have been made or if the episode finished, the total reward and the done boolean are then returned by the move function.

If the total reward from `move()`-ing is less than or equal to zero, such as this scenario:

TODO, add the gif of no backtracking 

then we enter a code branch for _backtracking_.

### Backtracking

Backtracking is just how it sounds, moving backwards. If the agent isn't getting any reward from moving to the right, then Sonic is probably stuck, and moving back to the left might help. This is achieved by just calling `move()` again, but with the Left parameter set to true, so that Sonic will move to the left. This is an essential aspect of the agent, since only going to the right can get Sonic stuck on plenty of walls.

So basically, if you don’t make progress going to the right for 100 moves, try going to the left for 70.

### Learning

If the episode finished during that call to move(), or the backtracking then the main while loop will begin a new episode and restart the environment. Then there is a choice to make, whether to randomly explore the environment again in a new episode, or to instead exploit (which we'll cover later). This choice is decieded by this line of code:

```python
 if (solutions and random.random() < EXPLOIT_BIAS + env.total_steps_ever / TOTAL_TIMESTEPS + best_run/10000):
```

which checks for truthyness of `solutions` which is a list of the key presses used to finish an episode and get a reward, and also compares a random number to the sum of `EXPLOIT_BIAS`, the % of time that has passed, and how close the best score is to the maximum score of 10,000. `EXPLOIT_BIAS` is a hyperparameter that is set at the beginning of the code and for the purposes of the contest, seems to have had a sweet spot right around `0.12`

![A scatter plot of exploit biases and contest scores.](img/graph.png "A scatter plot of exploit biases and contest scores.")


TODOTODOTODO


...

Possible expansions:
* exploit for a bit and then go back to random
* use a neural net for deciding backtracking

Initialization
Starting with the main function, the first thing that gets set up is the remote environment. I conceptualize this as being the same as the local environment that I could render, but instead being specified by the retro-contest command. The environment is also wrapped into a larger class of a TrackedEnv, this take the initial environment and gives in the following additional properties that will be used for learning:

self.action_history = []
self.reward_history = []
self.total_reward = 0
self.total_steps_ever = 0
and three functions to interact with this new TrackedEnv that I will get into later. There are also a couple of variables set that will be used later on when the action gets going: new_ep which defines whether or not we should start a new episode, and solutions which will store a list of successful gameplay sequences and their total reward.

Next we enter an infinite loop, and because new_ep is true, the environment is immediately reset and the new_ep variable set to False. The very next line is rew, new_ep = move(env, 100) where we actually start playing some Sonic.



Backtracking


The Learning part of Machine Learning
Now that we have gone through how to get Sonic through the environment, let’s take a look at how our agent learns. At the end of the episode, the maximum total cumulative reward (the largest in a running total of all the rewards achieved) in the run along with an array of all of the moves that were made (that is, a long list of 1x12 arrays that are mostly filled with false values), are stored in the solutions array. The array of all the moves is created by the TrackedEnv’s best_sequence method, which returns all the moves made up until the maximum total reward wash achieved. For reference, a run that didn’t go well for me looked like this:

[(
  [1903800.0], 
  [array([False, False, False, False, False, False, False,  True, False,False, False, False]),
   array([False, False, False, False, False, False, False,  True, False,False, False, False]),
...
Exploitation
With one run complete, we now have a viable sequence of moves and the reward that we achieved by doing those moves. Now it is time to exploit. Back in the main while loop, if you start a new episode with a solution, there is a check for whether or not you should exploit your best solution, or if you should try for a better solution with the random movements. This check looks like this:

random.random() < EXPLOIT_BIAS + env.total_steps_ever / TOTAL_TIMESTEPS
A random number needs to be less than hyper parameter EXPLOIT_BIAS plus the percentage of total timesteps that has occurred. As time goes on, this agent will be more likely to exploit the best solution encountered for a given step. If the exploit branch is called, then the previous solutions are sorted and the one with the best average score is stored in a variable best_pair. Then a new reward is achieved by playing that same sequence of moves again, instead of going through the normal move()/backtrack process. If Sonic happens to get further than the sequence did, then empty moves will be used to finish out the episode (he will stand still until the game timer runs out, or he is killed). That new reward is added to that action sequence (that is how the average reward for a given action sequence is determined). It might seem strange that replaying the same sequence of moves could get you different results, but the game has a sticky frameskip mechanic that makes actions sometimes repeat themselves.

I really enjoyed diving deep into this code, and will probably use this as the basis for new agents, since I think I came up with quite a few improvements that I am excited to implement. I have also really enjoyed talking to the other contestants, so if you are thinking of saying hello, please do!

Thanks for reading! You might be interested in the rest of this series:

Day 1: Getting the Basics Set Up
Day 3: Running the Jerk Agent
Days 4 & 5: Getting TensorFlow & Docker to work on my MacBook
Day 6: Playback Tooling for .bk2 files
Days 9 &10: Failing with the Rainbow DQN baseline code.
Days 11–14: Reading the PPO2 code
Days 16–18: Running the PPO2 baseline code, and failing at TensorFlow & Docker optimization.
Days 22–25: A Deep Dive into the Jerk Agent
Days 26–29: Visualizing batches of sonic runs
Days 38–53: Discovering Q-Learning
ProgrammingOpenAIOpenai Retro ContestArtificial IntelligenceMachine Learning
Like what you read? Give Tristan Sokol a round of applause.
From a quick cheer to a standing ovation, clap to show how much you enjoyed this story.

Go to the profile of Tristan Sokol
Tristan Sokol
Developer Evangelist for Square. When I’m not helping build a commerce platform, I’m growing succulents in my back yard. https://tristansokol.com/

Also tagged OpenAI
Open AI releases charter promising AGI safety for human race
Go to the profile of Aditya Chennuru
Aditya Chennuru
Also tagged Machine Learning
An intro to Machine Learning for designers
Go to the profile of Sam Drozdov
Sam Drozdov
Also tagged OpenAI
Conquering OpenAI Retro Contest 1: Preparing Everything for the Contest
Go to the profile of Flood Sung
Flood Sung
Responses
1 response to your storyManage responses
Next story
Discovering Q learning