import numpy as np
import scr.FigureSupport as figureLibrary
import scr.StatisticalClasses as Stat

class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored

        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

        #define the object to do summary stats on
        self._sumStat_rewards_to_analyze = Stat.SummaryStat('Game rewards', self.get_reward_list())

        #create a new list to store rewards in the format of 1=lost money, 0=did not lose
        self._gameLoss = []
        for a in range(n_games):
            if self._gameRewards[a] >= 0:
                self._gameLoss.append(0)
            else:
                self._gameLoss.append(1)

        #define the object to do summary stats on for the loss prob
        self._sumStat_prob_loss_to_analyze = Stat.SummaryStat('Game rewards', self._gameLoss)

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_CI_reward(self, alpha):
        return self._sumStat_rewards_to_analyze.get_t_CI(alpha)

    def get_PI_reward(self,alpha):
        return self._sumStat_rewards_to_analyze.get_PI(alpha)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards


    def get_max(self):
        """ returns maximum reward"""
        return max(self._gameRewards)

    def get_min(self):
        """ returns minimum reward"""
        return min(self._gameRewards)

    def get_probability_loss(self):
        """ returns the probability of a loss """
        count_loss = 0
        for value in self._gameRewards:
            if value < 0:
                count_loss += 1
        return count_loss / len(self._gameRewards)

    def get_CI_of_prob_loss(self, alpha):
        return self._sumStat_prob_loss_to_analyze.get_t_CI(alpha)



#simulate the trial
trial = SetOfGames(prob_head=0.5, n_games=1000)

print("Problem 1:")
# Calculate expected reward of 1000 games
print("The average expected reward is:", trial.get_ave_reward())

# HW6 Problem 1: Print the 95% t-based confidence intervals for the expected reward and the probability of loss.
print("The 95% CI for the reward is:", trial.get_CI_reward(0.05))

# HW5 Problem 1: Create histogram of winnings
figureLibrary.graph_histogram(
    observations=trial.get_reward_list(),
    title="Histogram of Rewards from 1000 Games",
    x_label="Game Rewards",
    y_label="Frequency")

# minimum reward is -$250 if {T, T, H} never occurs.
# maximum reward is $350 if {T, T, H} occurs 6 times (if you increase the number of games you might see this outcome).

# find minimum and maximum reward in trial
print("In our trial, the maximum reward is:", trial.get_max())
print("In our trial, the minimum reward is:", trial.get_min())

# HW5 Problem 2: Find the probability of a loss
print("The probability of a single game yielding a loss is:", trial.get_probability_loss())
#HW6 Problem 1: Print the 95% t-based confidence intervals for the expected reward and the probability of loss.
print("The 95% CI for the probability of a loss is:", trial.get_CI_of_prob_loss(0.05))

# HW6 problem 2
print("Problem 2: There is a 95% probability that a large group of similarly produced confidence intervals contain the true values (of mean reward and probability of loss respectively)")



# HW6 problem 3

#outputs
print("Problem 3:")
print("The casino owner's game is a steady state situation, while the gambler should analyze a transient situation.")
print("For the casino owner, expected reward for each game is:", trial.get_ave_reward())
print("For the casino owner, uncertainty is represented by the 95% CI:", trial.get_CI_reward(0.05))
print("This means that 95% of similarly constructed intervals contain the true expected reward")
print("For the gambler, expected reward for each game is:", trial.get_ave_reward())
print("For the gambler, uncertainty in each game is represented by the 95% PI:", trial.get_PI_reward(0.05))
print("This means that 95% of the next game's rewards are expected to fall within the interval above")
