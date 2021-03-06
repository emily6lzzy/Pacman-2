# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.values_copy = util.Counter()
        for i in range(self.iterations): #Run through all the iterations
            values_copy = self.values.copy() #Do not disturb the original values.
            for state in self.mdp.getStates():
                aggregrate_list = util.Counter()
                for action in self.mdp.getPossibleActions(state):
                    aggregrate = 0
                    for transition in self.mdp.getTransitionStatesAndProbs(state, action):
                        aggregrate += transition[1] * (self.mdp.getReward(state, action, transition[0]) + self.discount * values_copy[transition[0]])
                    aggregrate_list[action] = aggregrate
                self.values[state] = aggregrate_list[aggregrate_list.argMax()]#Store the max of all actions in the values.

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        aggregrate = 0
        for transition in self.mdp.getTransitionStatesAndProbs(state, action):
            aggregrate += transition[1] * (self.mdp.getReward(state, action, transition[0]) + self.discount * self.values[transition[0]])
        return aggregrate #Return the computed average of all the actions.
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """

        if self.mdp.isTerminal(state):
            return None
        else:
            max_value, best_action = - float("inf"), "" #Initialize the default max value and best action
            for action in self.mdp.getPossibleActions(state):
                aggregrate = 0
                for transition in self.mdp.getTransitionStatesAndProbs(state, action):
                    aggregrate += transition[1]*(self.mdp.getReward(state, action, transition[0]) + self.discount*self.values[transition[0]])
                if aggregrate > max_value:#Update the max value and best action
                    max_value = aggregrate
                    best_action = action
            return best_action #Return the best action

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
