import numpy as np
import matplotlib.pyplot as plt


class EISGame(object):
    """
    Simulates the game described in the paper. Game is multi-agent.
    S1= [1,2] , S2 = [-2,1]  S = S1 U S2
    Actions = [0.1,0.2,0.3,0.4,0.5]
    Transition = s' = Project (-s + Guassian(a,sigma^2)), sigma_2 = 1
    Reward = r1(s,a) = |s| - a
    t: near 0 constant so to avoid 0+,0- errors
    """

    def __init__(self, t=0.1, numActions=5, stateWidth=1, gamma=0.9, simultaneous=False):
        super(EISGame, self).__init__()
        # Actual Environment starts here
        self.t = t
        self.p0States = [t, t + stateWidth]  # Player 1
       # Randomly start in player 1's space
        # self.curState = np.random.uniform(self.p0States[0], self.p0States[1])
        self.curState = np.random.uniform(0 - stateWidth, 0 + stateWidth)
        self.curPlayer = 0  # Player 0 always starts first, 0 Indexed
        if self.curState <= 0:
            self.curPlayer = 1
        else:
            self.curPlayer = 0

        self.p1States = [-t - stateWidth, -t]  # PLayer 2
        self.States = [self.p0States, self.p1States]
        self.actions = [0.1 * i for i in range(1, numActions + 1)]
        self.simultaneous = simultaneous
        self.gamma = gamma
        self.rounds = 0  # Rounds updated when each player plays atleast once
        self.roundCounter = 0  # number of players that have played this round
        self.p0Rewards = [0] * 9999  # Preallocate 0 arrays
        self.p1Rewards = [0] * 9999  # Preallocate 0 arrays
        self.rewards = [self.p0Rewards, self.p1Rewards]  # Reward array
        print("The starting state is " + str(self.curState))

    def transition(self, action, state=None, prints=False, curPlayer=None):
        if state is None:
            state = self.curState
        act = np.random.normal(loc=action, scale=1)  # Gaussian filter
        if prints:
            print('Resulting action was ' + str(act))
        nextState = -state + act  # calculate next state
        # Calculate the possible states depending on the player
        # Transition to the next player
        if curPlayer is None:
            curPlayer = (self.curPlayer + 1) % 2  # Running the game
        else:
            curPlayer = (curPlayer + 1) % 2  # Simulator
        curStates = self.States[curPlayer]
        if nextState < min(curStates):  # Project to min
            nextState = min(curStates)
        if nextState > max(curStates):  # Project to max
            nextState = max(curStates)
        if prints:
            print('Next State is ' + str(nextState))
        return nextState

    def calcReward(self, action, state=None):
        if state is None:
            state = self.curState
        # if state == self.t or state == -self.t:  # t is 0
            # return - action
        return np.sin(2*abs(state)) - action

    def status(self):
        print("Current game status: ")
        print("Rounds: " + str(self.rounds))
        print("Number of players that have played this round: " +
              str(self.roundCounter))
        print("Player Turn: " + str(self.curPlayer + 1))
        print("Rewards so far: ")
        print("Player 1: " + str(self.rewards[0][0:self.rounds + 1]))
        print("Player 2: " + str(self.rewards[1][0:self.rounds + 1]))
        print("Curent State: " + str(self.curState))
        p1 = np.arange(0, 1, 0.02)
        p2 = np.arange(-1, 0, 0.02)
        plt.figure(figsize=(9, 1))
        plt.grid(True, 'both')
        plt.axvline(0).set_color("green")
        plt.axhline(0).set_color("green")
        plt.plot(p1, p1 - p1, color='red', linewidth=5)
        plt.plot(p2, p2 - p2, color='blue', linewidth=5)
        plt.plot(self.curState, 0, 'g^', markersize=12)

    def updateRounds(self):
        if self.simultaneous:
            self.roundCounter += 1
            if (self.roundCounter == 2):
                # If both players have played then increase total rounds
                self.roundCounter = 0  # reset the roundcounter
                self.rounds += 1  # Increase total rounds
        else:
            self.rounds += 1

    def takeAction(self, action, prints=False):
        if action not in self.actions:  # Make sure action is valid
            print("Invalid Action")
            return -1
        # Calculate the reward from the action
        reward = pow(self.gamma, self.rounds) * \
            self.calcReward(action, state=self.curState)
        # Increase the number of players that have played this round
        if prints:
            print('Player ' + str(self.curPlayer + 1) +
                  ' Took action ' + str(action))
        print("The reward was " + str(reward))
        # Update current player's rewards
        if not self.simultaneous:  # Player 1 is the only player whose reward matters
            self.rewards[0][self.rounds] = reward
        else:  # simulatenous not implemented
            raise NotImplementedError

        # update the current state
        self.curState = self.transition(
            action, state=self.curState, prints=prints, curPlayer=None)
        self.curPlayer = (self.curPlayer + 1) % 2
        self.updateRounds()
        return 1
