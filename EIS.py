import numpy as np


class EISGame(object):
    """
    Simulates the game described in the paper. Game is multi-agent.
    S1= [1,2] , S2 = [-2,1]  S = S1 U S2
    Actions = [0.1,0.2,0.3,0.4,0.5]
    Transition = s' = Project (-s + Guassian(a,sigma^2)), sigma_2 = 1
    Reward = r1(s,a) = |s| - a
    """

    def __init__(self, numActions=5, stateWidth=1, gamma=0.9):
        super(EISGame, self).__init__()
        # Actual Environment starts here
        # Randomly start in player 1's space
        self.curState = np.random.uniform(1, 2)
        self.curPlayer = 0  # Player 0 always starts first, 0 Indexed
        self.p0States = [1, 1 + stateWidth]
        self.p1States = [-1 - stateWidth, -1]
        self.States = [self.p0States, self.p1States]
        self.actions = [0.1 * i for i in range(1, numActions + 1)]
        self.gamma = gamma
        self.rounds = 0
        self.roundCounter = 0  # number of players that have played this round
        self.p0Rewards = [0] * 9999  # Preallocate 0 arrays
        self.p1Rewards = [0] * 9999  # Preallocate 0 arrays
        self.rewards = [self.p0Rewards, self.p1Rewards]  # Reward array

    def transition(self, action, prints=False):
        act = np.random.normal(loc=action, scale=1)  # Gaussian filter
        if prints:
            print('Resulting action was ' + str(act))
        nextState = -self.curState + act  # calculate next state
        # Calculate the possible states depending on the player
        # Transition to the next player
        self.curPlayer = (self.curPlayer + 1) % 2
        curStates = self.States[self.curPlayer]
        if nextState < min(curStates):  # Project to min
            nextState = min(curStates)
        if nextState > max(curStates):  # Project to max
            nextState = max(curStates)
        if prints:
            print('Next State is ' + str(nextState))
        return nextState

    def calcReward(self, action):
        return pow(self.gamma, self.rounds) * (abs(self.curState) + action)

    def takeAction(self, action, prints=False):
        if action not in self.actions:  # Make sure action is valid
            print("Invalid Action")
            return -1
        # Calculate the reward from the action
        reward = self.calcReward(action)
        self.roundCounter += 1
        # Increase the number of players that have played this round
        if (self.roundCounter == 2):
            # If both players have played then increase total rounds
            self.roundCounter = 0  # reset the roundcounter
            self.rounds += 1  # Increase total rounds
        if prints:
            print('Player ' + str(self.curPlayer + 1) +
                  ' Took action ' + str(action))
        print("The reward was " + reward)
        # Update current player's rewards
        self.rewards[self.curPlayer][self.rounds] = reward
        # update the current state. # also transitions to the next player
        self.curState = self.transition(action, prints)
        return 1
