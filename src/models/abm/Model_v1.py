#============================================================================================
#    Agent Based SEIR Model vector-borne disease propagation
#============================================================================================
__all__ = ['Human', 'Mosquito', 'SEIR_vector_borne_disease']

import random
import numpy as np
import networkx as nx

from mesa import Model, Agent
from mesa.time import RandomActivation,  ActivationByBreed
from mesa.datacollection import DataCollector

#============================================================================================
#Make Model Deterministic
#random.seed(10)
#np.random.seed(10)
#============================================================================================
#Global Parameters (do not sweep)
#============================================================================================
family_size = 4
average_M_lifespan = 25
prob_promiscuity = .02

#Class for Mosquito Agent
#============================================================================================
class Mosquito(Agent):
    '''
    Attributes:
        condition: "Susceptible",  "exposed", "infectious", "Recovered_Immune"
        node_ID: permanent position in Network
        age: M dies after several days
    '''
    def __init__(self, node_ID, condition, age = 0):
        '''
        Create a new Mosquito.
        '''
        self.node_ID = node_ID
        self.condition = condition
        self.age = age

        #Helper variables needed for flexibility in agent activation
        self.condition_nextState = None
        self.days_left_incubation_period = None
        self.person_contacts = []
        self.need_advance = False

    def step(self, model):
        '''
        Processes:
            Ageing: each time step age increases by one (day)
            Dying: Once the lifespan of mosquito is reached, it dies
            Reproduction and partial vertical transmission: mosquito reproduces and some carry also the virus
            Flow Exposed to Infectious:
        '''
        self.need_advance = False

        # Ageing
        self.age += 1

        # Dying
        if  self.age >= int(np.random.normal(average_M_lifespan, 1)):
            model.schedule.remove(self)

        # Reproduction and partial vertical transmission
        if  random.uniform(0.0, 1.0) < model.m_prob_reproduce and model.initial_Mosquitos >= model.schedule.get_breed_count(Mosquito):
            new_mosquito = Mosquito(
                node_ID =self.node_ID,
                condition = (self.condition if random.random() > model.share_m_vertical_transmission else 'susceptible')
                                    )
            model.schedule.add(new_mosquito)

        #Flow from exposed to infectious
        if self.condition == "exposed":
            if  self.days_left_incubation_period > 0:
                self.days_left_incubation_period -= 1

            if self.days_left_incubation_period <= 0:
                self.days_left_incubation_period = None

                if model.simultanousAct == False:
                    self.condition = "infectious"
                else:
                    self.condition_nextState = "infectious"
                    self.need_advance = True

        # Mosquito bites human at shared Location (Node)
        for agent in model.schedule.agents:
            if agent.node_ID == self.node_ID and isinstance(agent, Human):  # in lst_neighbor_nodes:
                if agent.protection <= random.uniform(0., 1.0): ############
                    self.person_contacts.append(agent)

        nr_contacts = len(self.person_contacts)
        self.person_contacts = random.sample(self.person_contacts,
                                             model.blood_meals_per_day if nr_contacts > model.blood_meals_per_day else nr_contacts)

        self.contact_list = []
        for contact in self.person_contacts:

            # Transmission from Mosquito to human
            if contact.condition == 'susceptible' and self.condition == "infectious":
                if model.transmission_prob_vector_to_human >= random.uniform(0., 1.0):
                    if model.simultanousAct == False:
                        contact.condition = "exposed"
                        contact.days_left_incubation_period = int(np.random.normal(model.intrinsic_incubation_period, 1))
                        model.Zika_Cases += 1
                    else:
                        self.contact_list.append(contact)
                        self.need_advance = True

            # Transmission from Human to Mosquito
            if contact.condition == 'infectious' and self.condition == 'susceptible':
                if model.transmission_prob_human_to_vector >= random.uniform(0., 1.0):
                    if model.simultanousAct == False:
                        self.condition = "exposed"
                        self.days_left_incubation_period = int(np.random.normal(model.extrinsic_incubation_period, 1))
                    else:
                        self.contact_list.append(contact)
                        self.need_advance = True

    def advance(self, model):
        '''
        Set the state to the new computed state -- computed in step()
        Only called by SimultaneousActivation function and for agents which change their condition
        '''
        if self.need_advance == True:
            # Transmission from Mosquito to Human
            if self.condition == 'infectious':
                for contact in self.contact_list:
                    contact.condition = "exposed"
                    contact.condition_nextState = 'exposed'
                    contact.days_left_incubation_period = int(np.random.normal(model.intrinsic_incubation_period, 1))
                    model.Zika_Cases += 1

            # Transmission from Human to Mosquito
            if self.condition == 'susceptible':
                for contact in self.contact_list:
                    self.condition = "exposed"
                    self.condition_nextState = 'exposed'
                    self.days_left_incubation_period = int(np.random.normal(model.extrinsic_incubation_period, 1))

            if self.condition == "exposed":
                self.condition = self.condition_nextState
#                 print ('condition updated advance: ', self.condition)

            self.need_advance = False


class Human(Agent):
    '''
    Attributes:
        condition: "susceptible",  "exposed", "infectious", "recovered_Immune"
        node_ID: current position in Network
        recovery_period
    '''
    def __init__(self, model, node_ID, condition, income_group):
        '''
        Create a new person.
        '''
        self.node_ID = node_ID
        self.condition = condition

#         print condition
        self.income_group = income_group

        if self.income_group == 'rich':
            self.protection = .98
        else:
            self.protection = .05

        self.recovery_period = None

        if self.condition == 'infectious':
            self.condition_nextState = 'infectious' # DO ALSO FOR M infected by human
            self.recovery_period = int(np.random.normal(model.recovery_period_human, 1))

        if self.condition == 'exposed':
            self.condition_nextState = 'exposed' # DO ALSO FOR M infected by human
            self.days_left_incubation_period = int(np.random.normal(model.intrinsic_incubation_period, 1))

        self.condition_nextState =None
        self.case = False
        self.need_advance = False
        self.sexual_partners = []

        # Create a sexual partner for the person, condition: other person at same location
        for agent in model.schedule.agents:
            if agent.node_ID == self.node_ID and isinstance(agent, Human):
                self.sexual_partners.append(agent)
                break

    def step(self, model):
        '''
        Processes:
            1. Human local travel: Move to random neighboring position
            2. Flow from exposed to infectious Human
            3. Flow from infectious to recovered
            4. Sexual Transmission from human to human
        '''
        # 1. Human local travel
        lst_neighbor_nodes = model.network.neighbors(self.node_ID)
        if lst_neighbor_nodes: # Ensure list is not empty
            self.node_ID = random.choice(lst_neighbor_nodes)

        self.need_advance = False

        # 2. Flow from exposed to infectious Human
        if self.condition == "exposed":
            if  self.days_left_incubation_period > 0:
                self.days_left_incubation_period -= 1

            if self.days_left_incubation_period <= 0:
                self.days_left_incubation_period = None
                self.recovery_period = int(np.random.normal(model.recovery_period_human, 1))

                if random.random() < model.share_symptomatic_humans:
                    self.symptoms = True
                if model.simultanousAct == False:
                    self.condition = "infectious"
                else:
                    self.condition_nextState = "infectious"
                    self.need_advance = True

        # 3. Flow from infectious to recovered
        if self.condition == "infectious":
            if  self.recovery_period > 0:
                self.recovery_period -= 1
            if self.recovery_period <= 0:
                self.recovery_period = None
                if model.simultanousAct == False:
                    self.condition = "recovered_immune"
                else:
                    self.condition_nextState = "recovered_immune"
                    self.need_advance = True

        # 3. Sexual Transmission from human to human
        if prob_promiscuity >= random.uniform(0., 1.0): # Casual intercourse with different partner?
            for agent in model.schedule.agents:
                if agent.node_ID == self.node_ID and isinstance(agent, Human):
                    self.sexual_partners.append(agent)
                    break

        self.contact_list = []
        for contact in self.sexual_partners: # Transmission to sexual partners
            if contact.condition == 'susceptible' and self.condition == "infectious":
                if (model.transmission_prob_vector_to_human >= random.uniform(0., 1.0) and
                         model.sexual_intercourse_day >= random.uniform(0., 1.0)):
                    if model.simultanousAct == False:
                        contact.condition = "exposed"
                        contact.days_left_incubation_period = int(np.random.normal(model.intrinsic_incubation_period, 1))
                        model.Zika_Cases += 1
                    else:
                        self.contact_list.append(contact)
                        self.need_advance = True

        if len(self.sexual_partners) > 1:
            del self.sexual_partners[-1]

    def advance(self, model):
        '''
        Set the state to the new computed state -- computed in step()
        Only called by SimultaneousActivation function and for agents which change their condition
        '''
        if self.need_advance == True:
            # Transmission from human to human
            if self.condition == 'infectious':
                for contact in self.contact_list:
                    contact.condition = "exposed"
                    contact.condition_nextState = 'exposed'
                    contact.days_left_incubation_period = int(np.random.normal(model.intrinsic_incubation_period, 1))
                    model.Zika_Cases += 1
            self.condition = self.condition_nextState
            self.need_advance = False

class SEIR_vector_borne_disease(Model):
    '''
    Simple Human SIR (susceptible infected recovered) model.
    '''
    def __init__(self,
                 nr_infected=5,
                 nr_exposed=10,
                 nr_recovered_immune=0,
                 simultanousAct=True,
                 network_type = 'watts_strogatz_graph',
                 human_population=200,
                 ratio_vectors_per_person = .5,
                 intrinsic_incubation_period = 5.5,
                 extrinsic_incubation_period = 7,
                 m_prob_reproduce = .02,
                 transmission_prob_human_to_vector = .9,
                 transmission_prob_vector_to_human =.9,
                 blood_meals_per_day = 4,
                 share_m_vertical_transmission = .11,
                 recovery_period_human = 5,
                 sexual_intercourse_day = .2,
                 share_symptomatic_humans = .2,
                 share_infected_mosquitos = 0,
                 share_extreme_poverty = .2,
                 network_connectivity = 2.5
                ):
        '''
        Initialize model parameters
        '''
        self.Zika_Cases = 0

        self.human_population = human_population
        self.initial_Mosquitos = int(human_population * ratio_vectors_per_person)

        self.simultanousAct = simultanousAct
        self.network_type = network_type

        self.extrinsic_incubation_period = extrinsic_incubation_period
        self.intrinsic_incubation_period = intrinsic_incubation_period

        self.transmission_prob_human_to_vector = transmission_prob_human_to_vector
        self.transmission_prob_vector_to_human = transmission_prob_vector_to_human

        self.m_prob_reproduce = m_prob_reproduce
        self.blood_meals_per_day =  blood_meals_per_day
        self.share_m_vertical_transmission = share_m_vertical_transmission

        self.recovery_period_human = recovery_period_human
        self.sexual_intercourse_day = sexual_intercourse_day
        self.share_symptomatic_humans = share_symptomatic_humans
        self.share_infected_mosquitos = share_infected_mosquitos

        number_of_links = int(network_connectivity * human_population)
        ###################
        # Agent Activation#
        ###################
        if self.simultanousAct == False:
            self.schedule = ActivationByBreed(self, False)
        else:
            self.schedule = ActivationByBreed(self, True)

        ###########
        # Network #
        ###########
        # Random Network: binomial_graph
        if network_type == 'erdos_renyi_graph':
            link_probability = (float(number_of_links) / float(human_population**2) ) * 1.6
            self.network = nx.erdos_renyi_graph(human_population, link_probability)

        #Scale-free network (Powerlaw)
        elif network_type == 'barabasi_albert_graph':
            self.network = nx.barabasi_albert_graph(human_population, number_of_links / human_population)

        # Network: small-world graph
        elif network_type == 'watts_strogatz_graph':
            link_probability = (float(number_of_links) / float(human_population**2) ) * 1.6
            self.network = nx.watts_strogatz_graph(human_population, family_size, link_probability)

        # cellular automaton
        elif network_type == 'grid_2d_graph':
            self.network = nx.grid_2d_graph(int(round(np.sqrt(human_population))),int(round(np.sqrt(human_population))), periodic = True)
            self.network = nx.convert_node_labels_to_integers(self.network)
            self.human_population = int(round(np.sqrt(human_population)))**2
        else:
            raise Exception("Not recognized Network, please select a different network type")

        self.datacollector = DataCollector(model_reporters={
                                "m_susceptible": lambda m: self.count_type(m, "susceptible", Mosquito),
                                "m_exposed": lambda m: self.count_type(m, "exposed", Mosquito),
                                "m_infectious": lambda m: self.count_type(m, "infectious", Mosquito),

                                "h_susceptible_rich": lambda m: self.count_type(m, "susceptible", Human)-self.count_poor_human(m, "susceptible"),
                                "h_exposed_rich": lambda m: self.count_type(m, "exposed", Human)-self.count_poor_human(m, "exposed"),
                                "h_symptomatic_infectious_rich": lambda m: self.count_type(m, "infectious", Human, True)-self.count_poor_human(m, "infectious", True),
                                "h_asymptomatic_infectious_rich": lambda m: self.count_type(m, "infectious", Human)-self.count_poor_human(m, "infectious"),
                                "h_recovered_immune_rich": lambda m: self.count_type(m, "recovered_immune", Human)-self.count_poor_human(m, "recovered_immune"),

                                "h_susceptible_poor": lambda m: self.count_poor_human(m, "susceptible"),
                                "h_exposed_poor": lambda m: self.count_poor_human(m, "exposed"),
                                "h_symptomatic_infectious_poor": lambda m: self.count_poor_human(m, "infectious", True),
                                "h_asymptomatic_infectious_poor": lambda m: self.count_poor_human(m, "infectious"),
                                "h_recovered_immune_poor": lambda m: self.count_poor_human(m, "recovered_immune"),

                                "cumulative_cases": lambda m: m.Zika_Cases,
                                                           })
        # Create Mosquitos:
        for i in range(self.initial_Mosquitos):
            node_ID = random.choice(self.network.nodes())
            if self.share_infected_mosquitos >= random.uniform(0., 1.0):
                M_condition = 'infected'
            else:
                M_condition = 'susceptible'
            new_mosquito = Mosquito(
                                     node_ID=node_ID,
                                     condition=M_condition, # Assumes all mosquitoes are susceptible initially
                                     age = int(np.random.uniform(0, average_M_lifespan)),
                                     # age = int(np.random.triangular(0, average_M_lifespan/2.0, average_M_lifespan)),
                                    )
            self.schedule.add(new_mosquito)


#         print ('infected', nr_infected)
#         print ('nr_exposed', nr_exposed)
#         print ('nr_recovered_immune', nr_recovered_immune)

        # Create Humans
        for i in range(self.human_population):
            node_ID = random.choice(self.network.nodes())
            if nr_infected > 0:
                condition = "infectious"
                nr_infected -= 1
            elif nr_recovered_immune > 0:
                condition = "recovered_immune"
                nr_recovered_immune -= 1
            elif nr_exposed > 0:
                condition = "exposed"
                nr_exposed -= 1
            else:
                condition = "susceptible"

            if share_extreme_poverty >= random.uniform(0., 1.0):
                income_group = 'poor'
            else:
                income_group = 'rich'
            new_person = Human(self,
                               node_ID,
                               condition,
                               income_group
                                    )
            self.schedule.add(new_person)

        # Auto run until stop
        self.running = False

    def Feed_data(self, exinfected):
        #print (exinfected)
        for x in range(int(exinfected)):
            node_ID = random.choice(self.network.nodes())
            new_person = Human(self,
                               node_ID,
                               condition='infectious',
                               income_group='rich'
                                    )
            self.schedule.add(new_person)

    # Simulation Model Time advance function
    def step(self):
        '''
        Advance the model by one step.
        '''
#         print len(self.schedule.agents)

        self.datacollector.collect(self)
        self.schedule.step()

#     # Simulation model run function
#     def run(self, n):
#         '''
#         Run the model for a certain number of steps.
#         '''
#         for _ in range(n):
#             self.step()

# With staticmethods behave like plain functions except that you can call them from an instance or the class:
# Staticmethods are used to group functions which have some logical connection with a class to the class.
    @staticmethod
    def count_type(model, condition, breed, symptomatic=False):
        '''
        Helper method to count persons in different condition in the model.
        '''
        count = 0
        if symptomatic==True:
            for agent in model.schedule.agents_by_breed[Human]:
                if hasattr(agent, 'symptoms'):
                    if agent.symptoms == True and agent.condition == condition:
                        count += 1
        else:
            for agent in model.schedule.agents:
                if agent.condition == condition and isinstance(agent, breed):
                    if agent.condition == 'infectious' and symptomatic==True:
                        continue
                    count += 1

        return count

    @staticmethod
    def count_poor_human(model, condition, symptomatic=False):
        '''
        Helper method to count persons in different condition in the model.
        '''
        count = 0
        if symptomatic==True:
            for agent in model.schedule.agents_by_breed[Human]:
                if agent.income_group == 'poor' and hasattr(agent, 'symptoms'):
                    if agent.symptoms == True and agent.condition == condition:
                        count += 1
        else:
            for agent in model.schedule.agents_by_breed[Human]:
                if agent.condition == condition and agent.income_group == 'poor':
                    if agent.condition == 'infectious' and symptomatic==True:
                        continue
        return count
