# The Improved Jerk Agent

The Jerk agent was a provided baseline for the [OpenAI Retro Contest](https://contest.openai.com/), you can find the original code in [openai/retro-baselines](https://github.com/openai/retro-baselines/blob/master/agents/jerk_agent.py). Throughout the contest I was able to make some useful improvements to the baseline agent, ultimately falling short of winning the contest, but ended up in the top 30 of the 200+ contestants. This is an explanation of how the improved-jerk agent works.

## Background

The improved JERK agent is an AI agent for reinforcement learning that uses a combination of random exploration and episode exploitation to build a successful solution to the environment.

At the start of each episode, there is first a check

Diagram of flowchart describing

start a new episode
 - if exploit & solutions
   - replay best run
else start a new run
 move and backtrack

Lets take a look at each of those parts




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

Move(env, num_steps, left, jump_prob, jump_repeat)
Move is where all of the actual action occurs. It first sets up some new variables to use later:

total_rew = 0.0
done = False
steps_taken = 0
jumping_steps_left = 0
Then it enters a loop that iterates through for the total number of num_steps that move() was called with.

The first thing that happens inside that loop is the creation of an array, action that is initially 12 falses, like this:

[False False False False False False False False False False False False]
Next, it takes the the 6th and 7th entries and assign them depending on whether move() was called with false being true. These two actions must be the left and right buttons on the D-pad, which is interesting. If Sonic is always moving to the right or left, are there obstacles that are impassable because they require only vertical movement? After that there is some logic around jumping. There are two variables that control jumping behavior, the jump_prob and jump_repeat . jump_prob is the probability that for a given step, action[0] will be true which will execute a jump in the game. For the default agent, the move() function is called in groups of 100 steps, so roughly 10 of them will include jumping, if it were not for jump_repeat. jump_repeat limits the number of times that you can have a jump inside the move() function, with a default of four, so if you are doing 100 steps, you will likely only have four jumps within those steps.

With our actions in place (either move left, move right, jump to the right, jump to the left) we can apply our button presses to the environment.

_, rew, done, _ = env.step(action)
The env.step function (as documented here) takes the array of actions that would be the moves for our controller and returns four variables:

ob I believe this is an array of the raw RGB values from the screen, totally not used for the jerk agent, so it is set to the python idiom _
rew this is the incremental reward achieved from executing this command.
done is a boolean value just describing if the game is over, either through sonic dying or getting to the end.
info here is an array of all the the relevant game information that the gym environment is pulling from the emulators memory. It has a ton of useful info such as the x & y position of Sonic, the number of rings & lives, etc. The baseline jerk agent does not use any of that, so it is also wasted away in _. For the third level of the first zone of Sonic, it looks like this:
{'act': 2, 'screen_x': 857, 'zone': 0, 'level_end_bonus': 0, 'score': 0, 'lives': 3, 'screen_x_end': 10592, 'rings': 2, 'x': 1017, 'y': 812}
The only variables that we need for the jerk agent are rew and done , rew gets added to a total_rew for total_reward, which stores the reward gained in that call to move(). That total reward and the done boolean are the returned values of the of the move function. If the episode finished during that call to move() then the main while loop will begin a new episode and restart the environment.

Backtracking
If the move function does make any positive impact into the reward, then the agent “backtracks” which is what is sounds like, moving backwards. This is achieved by just calling move() again, but with the Left parameter set to true, so that Sonic will move to the left. This is an essential aspect of the agent, since only going to the right can get Sonic stuck on plenty of walls.


Life without backtracking
So basically, if you don’t make progress going to the right for 100 moves, try going to the left for about 70 steps.

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