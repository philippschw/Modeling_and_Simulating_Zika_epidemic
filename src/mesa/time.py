'''
Mesa Time Module
=================================

Objects for handling the time component of a model. In particular, this module
contains Schedulers, which handle agent activation. A Scheduler is an object
which controls when agents are called upon to act, and when.

The activation order can have a serious impact on model behavior, so it's
important to specify it explicity. Example simple activation regimes include
activating all agents in the same order every step, shuffling the activation
order every time, activating each agent *on average* once per step, and more.

Key concepts:
    Step: Many models advance in 'steps'. A step may involve the activation of
    all agents, or a random (or selected) subset of them. Each agent in turn
    may have their own step() method.

    Time: Some models may simulate a continuous 'clock' instead of discrete
    steps. However, by default, the Time is equal to the number of steps the
    model has taken.


TODO: Have the schedulers use the model's randomizer, to keep random number
seeds consistent and allow for replication.

'''

import random
from collections import defaultdict


class BaseScheduler(object):
    '''
    Simplest scheduler; activates agents one at a time, in the order they were
    added.

    Assumes that each agent added has a *step* method, which accepts a model
    object as its single argument.

    (This is explicitly meant to replicate the scheduler in MASON).
    '''

    model = None
    steps = 0
    time = 0
    agents = []

    def __init__(self, model):
        '''
        Create a new, empty BaseScheduler.
        '''

        self.model = model
        self.steps = 0
        self.time = 0
        self.agents = []

    def add(self, agent):
        '''
        Add an Agent object to the schedule.

        Args:
            agent: An Agent to be added to the schedule. NOTE: The agent must
            have a step(model) method.
        '''
        self.agents.append(agent)

    def remove(self, agent):
        '''
        Remove all instances of a given agent from the schedule.

        Args:
            agent: An agent object.
        '''
        while agent in self.agents:
            self.agents.remove(agent)

    def step(self):
        '''
        Execute the step of all the agents, one at a time.
        '''
        for agent in self.agents:
            agent.step(self.model)
            agent.show_properties(self.model)
        self.steps += 1
        self.time += 1

    def get_agent_count(self):
        '''
        Returns the current number of agents in the queue.
        '''

        return len(self.agents)

#############!!!!!!!!!!!!!!!!!!######################Added Function###########
    def show_schedule_list(self):
        '''
        Returns the list of agents on schedule
        '''
        print "test"
        return self.agents

    def return_specific_agent(self, name):
        print name
        agent = [x for x in self.agents if x.agent_name == name]
        print agent
        return self.agents[agent]

class RandomActivation(BaseScheduler): #Rewritten so that Both synchronous and asynchronous agent activation is possible
    '''
    A scheduler which activates each agent once per step, in random order,
    with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask agents...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step(model) method.
    '''
###################################CHANGED############################	

    def __init__(self, model, Simultanously):
        BaseScheduler.__init__(self, model)
        self.Simultanously = Simultanously

    def step(self): 
        '''
        Executes the step of all agents, one at a time, in random order.
        '''
        random.shuffle(self.agents)
        for agent in self.agents:
            agent.step(self.model)
        if self.Simultanously == True:
            for agent in self.agents:
                agent.advance(self.model)
        self.steps += 1
        self.time += 1
###################################CHANGED############################
    #def show_schedule_list(self):
    #    return self.agents

class SimultaneousActivation(BaseScheduler):
    '''
    A scheduler to simulate the simultaneous activation of all the agents.

    This scheduler requires that each agent have two methods: step and advance.
    step(model) activates the agent and stages any necessary changes, but does
    not apply them yet. advance(model) then applies the changes.
    '''
    def step(self):
        '''
        Step all agents, then advance them.
        '''
        for agent in self.agents:
            agent.step(self.model)
        for agent in self.agents:
            agent.advance(self.model)
        self.steps += 1
        self.time += 1

#####Added based on Predator Prey Example Model
       
class ActivationByBreed(RandomActivation): 
    '''
    A scheduler which activates each type of agent once per step, in random 
    order, with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask breed...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step(model) method.
    '''
    agents_by_breed = defaultdict(list)
    
    # def __init__(self, model, Simultanously, agents_by_breed):
        # RandomActivation.__init__(self, model, Simultanously)
        # self.Simultanously = Simultanously
        # self.agents_by_breed = defaultdict(list)
         
    def __init__(self, model, Simultanously):
        super(ActivationByBreed, self).__init__(model, Simultanously)
        self.agents_by_breed = defaultdict(list)

    def add(self, agent):
        '''
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        '''

        self.agents.append(agent)
        agent_class = type(agent)
        self.agents_by_breed[agent_class].append(agent)

    def remove(self, agent):
        '''
        Remove all instances of a given agent from the schedule.
        '''

        while agent in self.agents:
            self.agents.remove(agent)

        agent_class = type(agent)
        while agent in self.agents_by_breed[agent_class]:
            self.agents_by_breed[agent_class].remove(agent)

    def step(self, by_breed=False): #True
        '''
        Executes the step of each agent breed, one at a time, in random order.

        Args:
            by_breed: If True, run all agents of a single breed before running
                      the next one.
        '''
        if by_breed:
            for agent_class in  self.agents_by_breed:
                self.step_breed(agent_class)
            self.steps += 1
            self.time += 1
        else:
            super(ActivationByBreed, self).step()

    def step_breed(self, breed):
        '''
        Shuffle order and run all agents of a given breed.

        Args:
            breed: Class object of the breed to run.
        '''
        agents = self.agents_by_breed[breed]
        random.shuffle(agents)
        for agent in agents:
            agent.step(self.model)

    def get_breed_count(self, breed_class):
        '''
        Returns the current number of agents of certain breed in the queue.
        '''
        return len(self.agents_by_breed[breed_class])


class StagedActivation(BaseScheduler):
    '''
    A scheduler which allows agent activation to be divided into several stages
    instead of a single `step` method. All agents execute one stage before
    moving on to the next.

    Agents must have all the stage methods implemented. Stage methods take a
    model object as their only argument.

    This schedule tracks steps and time separately. Time advances in fractional
    increments of 1 / (# of stages), meaning that 1 step = 1 unit of time.
    '''

    stage_list = []
    shuffle = False
    shuffle_between_stages = False
    stage_time = 1

    def __init__(self, model, stage_list=["step"], shuffle=False,
            shuffle_between_stages=False):
        '''
        Create an empty Staged Activation schedule.

        Args:
            model: Model object associated with the schedule.
            stage_list: List of strings of names of stages to run, in the
                         order to run them in.
            shuffle: If True, shuffle the order of agents each step.
            shuffle_between_stages: If True, shuffle the agents after each
                                    stage; otherwise, only shuffle at the start
                                    of each step.
        '''
        super().__init__(model)
        self.stage_list = stage_list
        self.shuffle = shuffle
        self.shuffle_between_stages = shuffle_between_stages
        self.stage_time = 1 / len(self.stage_list)

    def step(self):
        '''
        Executes all the stages of all agents.
        '''

        if self.shuffle:
            random.shuffle(self.agents)
        for stage in self.stage_list:
            for agent in self.agents:
                getattr(agent, stage)(self.model)  # Run stage
            if self.shuffle_between_stages:
                random.shuffle(self.agents)
            self.time += self.stage_time

        self.steps += 1
