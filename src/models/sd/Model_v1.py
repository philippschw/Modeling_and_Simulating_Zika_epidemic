from __future__ import division                                 
import numpy as np                                              
from pysd import functions                                      
from pysd import builder                                        
                                                                
class Components(builder.ComponentClass):                       
                                                                
    def inital_susceptible_poor(self):
        """Type: Flow or Auxiliary
        """
        return 100000 

    def inital_susceptible_rich(self):
        """Type: Flow or Auxiliary
        """
        return 100000 

    def rich_population(self):
        """Type: Flow or Auxiliary
        """
        return self.h_asymptomatic_infectious_poor()+self.h_exposed_poor()+self.h_recovered_immune_poor()+self.h_susceptible_poor()+self.h_symptomatic_infectious_poor() 

    def dmax_awareness_dt(self):                       
        return -self.building_up_awareness()                           

    def max_awareness_init(self):                      
        return self.init_max_awareness()                           

    def max_awareness(self):                            
        """ Stock: max_awareness =                      
                 -self.building_up_awareness()                          
                                             
        Initial Value: self.init_max_awareness()                    
        Do not overwrite this function       
        """                                  
        return self.state["max_awareness"]              
                                             
    def mosquito_bites_poor_pop(self):
        """Type: Flow or Auxiliary
        """
        return self.normal_blood_meals_a_day()*(self.ratio_of_vectors_per_person())*self.total_adult_mosquito_population()*(1-self.personal_protection_poor()) 

    def mosquito_bites_rich_pop(self):
        """Type: Flow or Auxiliary
        """
        return self.normal_blood_meals_a_day()*(self.ratio_of_vectors_per_person())*self.total_adult_mosquito_population()*(1-self.personal_protection_rich()) 

    def davailability_breeding_rich_dt(self):                       
        return self.creation_of_new_breeding_sites_rich()-self.elimination_of_potential_breeding_grounds_rich_neighb()                           

    def availability_breeding_rich_init(self):                      
        return self.init_breeding_sites_rich()                           

    def availability_breeding_rich(self):                            
        """ Stock: availability_breeding_rich =                      
                 self.creation_of_new_breeding_sites_rich()-self.elimination_of_potential_breeding_grounds_rich_neighb()                          
                                             
        Initial Value: self.init_breeding_sites_rich()                    
        Do not overwrite this function       
        """                                  
        return self.state["availability_breeding_rich"]              
                                             
    def building_awareness_based_on_reports(self):
        """Type: Flow or Auxiliary
        """
        return min((self.report_case()-self.public_awareness())/self.human_population(), self.report_case()) 

    def human_population(self):
        """Type: Flow or Auxiliary
        """
        return 10000 

    def initial_recovered_poor(self):
        """Type: Flow or Auxiliary
        """
        return 1000 

    def init_cumulative_cases(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def dcumulative_cases_dt(self):                       
        return self.zika_cases()                           

    def cumulative_cases_init(self):                      
        return self.init_cumulative_cases()                           

    def cumulative_cases(self):                            
        """ Stock: cumulative_cases =                      
                 self.zika_cases()                          
                                             
        Initial Value: self.init_cumulative_cases()                    
        Do not overwrite this function       
        """                                  
        return self.state["cumulative_cases"]              
                                             
    def init_max_awareness(self):
        """Type: Flow or Auxiliary
        """
        return 100 

    def init_public_awareness(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def init_reported_cases(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def initial_recovered_rich(self):
        """Type: Flow or Auxiliary
        """
        return 1000 

    def initial_susceptible_m(self):
        """Type: Flow or Auxiliary
        """
        return 10000 

    def ratio_of_vectors_per_person(self):
        """Type: Flow or Auxiliary
        """
        return 0.4 

    def init_diagnosed_cases(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def intial_infectious_m(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def report_case(self):
        """Type: Flow or Auxiliary
        """
        return self.diagnosed_zika_cases()/self.delaytime_of_reporting() 

    def personal_protection_rich(self):
        """Type: Flow or Auxiliary
        """
        return self.normal_personal_protection_rich()+self.public_awareness() 

    def normal_personal_protection_rich(self):
        """Type: Flow or Auxiliary
        """
        return 0.9 

    def personal_protection_poor(self):
        """Type: Flow or Auxiliary
        """
        return self.normal_personal_protection_poor()+self.public_awareness() 

    def transmission_probability_vector_to_human(self):
        """Type: Flow or Auxiliary
        """
        return self.transmission_probability() 

    def transmission_probability_human_to_vector(self):
        """Type: Flow or Auxiliary
        """
        return self.transmission_probability() 

    def transmission_probability(self):
        """Type: Flow or Auxiliary
        """
        return 0.4 

    def disease_sank_into_oblivion(self):
        """Type: Flow or Auxiliary
        """
        return self.public_awareness()/self.delay_time_until_it_falls_into_oblivion() 

    def building_up_awareness(self):
        """Type: Flow or Auxiliary
        """
        return min(self.building_awareness_based_on_reports(), self.max_awareness()) 

    def creation_of_new_breeding_sites_poor(self):
        """Type: Flow or Auxiliary
        """
        return (self.init_breeding_sites_poor()-self.availability_breeding_poor())*self.rate_of_breeding_site_recreation_poor() 

    def mosquito_renewal_rate(self):
        """Type: Flow or Auxiliary
        """
        return self.normal_mosquito_renewal_rate()+self.man_made_mosquito_renewal_rate() 

    def init_breeding_sites_rich(self):
        """Type: Flow or Auxiliary
        """
        return 100 

    def davailability_breeding_poor_dt(self):                       
        return self.creation_of_new_breeding_sites_poor()-self.elimination_of_potential_breeding_grounds_poor_neighb()                           

    def availability_breeding_poor_init(self):                      
        return self.init_breeding_sites_poor()                           

    def availability_breeding_poor(self):                            
        """ Stock: availability_breeding_poor =                      
                 self.creation_of_new_breeding_sites_poor()-self.elimination_of_potential_breeding_grounds_poor_neighb()                          
                                             
        Initial Value: self.init_breeding_sites_poor()                    
        Do not overwrite this function       
        """                                  
        return self.state["availability_breeding_poor"]              
                                             
    def creation_of_new_breeding_sites_rich(self):
        """Type: Flow or Auxiliary
        """
        return (self.init_breeding_sites_rich()-self.availability_breeding_rich())*self.rate_of_breeding_site_recreation_rich() 

    def rate_of_breeding_site_recreation_poor(self):
        """Type: Flow or Auxiliary
        """
        return 0.01 

    def rate_of_breeding_site_recreation_rich(self):
        """Type: Flow or Auxiliary
        """
        return 0.015 

    def init_breeding_sites_poor(self):
        """Type: Flow or Auxiliary
        """
        return 70 

    def initial_exposed_m(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def man_made_mosquito_renewal_rate_no_effort(self):
        """Type: Flow or Auxiliary
        """
        return 0.009 

    def elimination_of_potential_breeding_grounds_rich_neighb(self):
        """Type: Flow or Auxiliary
        """
        return min((self.public_awareness()*100)/self.destruction_time_of_water_ponds(), self.availability_breeding_rich()) 

    def delay_time_until_it_falls_into_oblivion(self):
        """Type: Flow or Auxiliary
        """
        return 60 

    def dm_exposed_dt(self):                       
        return self.mosquito_infection_poor()+self.mosquito_infection_rich()-self.incubation_mosquito()-self.mosquito_e_death()                           

    def m_exposed_init(self):                      
        return self.initial_exposed_m()                           

    def m_exposed(self):                            
        """ Stock: m_exposed =                      
                 self.mosquito_infection_poor()+self.mosquito_infection_rich()-self.incubation_mosquito()-self.mosquito_e_death()                          
                                             
        Initial Value: self.initial_exposed_m()                    
        Do not overwrite this function       
        """                                  
        return self.state["m_exposed"]              
                                             
    def mosquito_probability_decease(self):
        """Type: Flow or Auxiliary
        """
        return self.normal_mosquito_renewal_rate()+self.man_made_mosquito_renewal_rate_no_effort() 

    def dm_susceptible_dt(self):                       
        return self.mosquito_renewal()-self.mosquito_infection_rich()-self.mosquito_infection_poor()-self.mosquito_s_death()                           

    def m_susceptible_init(self):                      
        return self.initial_susceptible_m()                           

    def m_susceptible(self):                            
        """ Stock: m_susceptible =                      
                 self.mosquito_renewal()-self.mosquito_infection_rich()-self.mosquito_infection_poor()-self.mosquito_s_death()                          
                                             
        Initial Value: self.initial_susceptible_m()                    
        Do not overwrite this function       
        """                                  
        return self.state["m_susceptible"]              
                                             
    def man_made_mosquito_renewal_rate(self):
        """Type: Flow or Auxiliary
        """
        return self.man_made_mosquito_renewal_rate_no_effort()* ((self.availability_breeding_poor()/140)+(self.availability_breeding_rich()/200)) 

    def dpublic_awareness_dt(self):                       
        return self.building_up_awareness()-self.disease_sank_into_oblivion()                           

    def public_awareness_init(self):                      
        return self.init_public_awareness()                           

    def public_awareness(self):                            
        """ Stock: public_awareness =                      
                 self.building_up_awareness()-self.disease_sank_into_oblivion()                          
                                             
        Initial Value: self.init_public_awareness()                    
        Do not overwrite this function       
        """                                  
        return self.state["public_awareness"]              
                                             
    def destruction_time_of_water_ponds(self):
        """Type: Flow or Auxiliary
        """
        return 15 

    def elimination_of_potential_breeding_grounds_poor_neighb(self):
        """Type: Flow or Auxiliary
        """
        return min((self.public_awareness()*100)/self.destruction_time_of_water_ponds(), self.availability_breeding_poor()-self.stock_min_level_consequence_of_slum_conditions()) 

    def rich_pop_human_infection(self):
        """Type: Flow or Auxiliary
        """
        return self.mosquito_bites_rich_pop()*self.ratio_infectious_mosquitos()*self.rich_pop_ratio_of_susceptible_people()*self.transmission_probability_vector_to_human() 

    def share_reported_cases(self):
        """Type: Flow or Auxiliary
        """
        return 0.6 

    def mosquito_infection_poor(self):
        """Type: Flow or Auxiliary
        """
        return self.mosquito_bites_poor_pop()*self.ratio_of_susceptible_mosquitos()*self.share_viremic_poor_population()*self.transmission_probability_human_to_vector() 

    def mosquito_infection_rich(self):
        """Type: Flow or Auxiliary
        """
        return self.mosquito_bites_rich_pop()*self.ratio_of_susceptible_mosquitos()*self.share_viremic_rich_population()*self.transmission_probability_human_to_vector() 

    def share_viremic_rich_population(self):
        """Type: Flow or Auxiliary
        """
        return self.rich_pop_infectious()/self.rich_population() 

    def share_viremic_poor_population(self):
        """Type: Flow or Auxiliary
        """
        return self.poor_pop_infectious()/self.poor_population() 

    def mosquito_renewal(self):
        """Type: Flow or Auxiliary
        """
        return (self.m_infectious()*(1-self.vertical_transmission_infection_rate())+(self.total_adult_mosquito_population()-self.m_infectious()))*self.mosquito_renewal_rate() 

    def normal_personal_protection_poor(self):
        """Type: Flow or Auxiliary
        """
        return 0.05 

    def stock_min_level_consequence_of_slum_conditions(self):
        """Type: Flow or Auxiliary
        """
        return 30 

    def arrival_airtravel_passengers_asumptomatic(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def arrival_airtravel_passengers_exposed(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def arrival_airtravel_passengers_recovered(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def arrival_airtravel_passengers_susceptible(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def arrival_airtravel_passengers_symptomatic(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def poor_population(self):
        """Type: Flow or Auxiliary
        """
        return self.h_asymptomatic_infectious_rich()+self.h_exposed_rich()+self.h_recovered_immune_rich()+self.h_susceptible_rich()+self.h_symptomatic_infectious_rich() 

    def departures(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def departure_airtravel_passengers_asymptomatic(self):
        """Type: Flow or Auxiliary
        """
        return self.departures()*(self.h_asymptomatic_infectious_rich()/self.rich_population()) 

    def departure_airtravel_passengers_exposed(self):
        """Type: Flow or Auxiliary
        """
        return self.departures()*(self.h_exposed_rich()/self.rich_population()) 

    def departure_airtravel_passengers_recovered(self):
        """Type: Flow or Auxiliary
        """
        return self.departures()*(self.h_recovered_immune_rich()/self.rich_population()) 

    def departure_airtravel_passengers_susceptible(self):
        """Type: Flow or Auxiliary
        """
        return self.departures()*(self.h_susceptible_rich()/self.rich_population()) 

    def departure_airtravel_passengers_symptomatic(self):
        """Type: Flow or Auxiliary
        """
        return self.departures()*(self.h_symptomatic_infectious_rich()/self.rich_population()) 

    def dh_asymptomatic_infectious_rich_dt(self):                       
        return self.arrival_airtravel_passengers_asumptomatic()+self.rich_pop_asym_incubation()-self.departure_airtravel_passengers_asymptomatic()-self.rich_pop_asym_human_recovery()                           

    def h_asymptomatic_infectious_rich_init(self):                      
        return self.initial_infectious_rich_asym()                           

    def h_asymptomatic_infectious_rich(self):                            
        """ Stock: h_asymptomatic_infectious_rich =                      
                 self.arrival_airtravel_passengers_asumptomatic()+self.rich_pop_asym_incubation()-self.departure_airtravel_passengers_asymptomatic()-self.rich_pop_asym_human_recovery()                          
                                             
        Initial Value: self.initial_infectious_rich_asym()                    
        Do not overwrite this function       
        """                                  
        return self.state["h_asymptomatic_infectious_rich"]              
                                             
    def dh_susceptible_rich_dt(self):                       
        return self.arrival_airtravel_passengers_susceptible()-self.departure_airtravel_passengers_susceptible()-\
		self.rich_pop_human_infection()-self.rich_pop_sexual_transmission()                           

    def h_susceptible_rich_init(self):                      
        return self.inital_susceptible_rich()                           

    def h_susceptible_rich(self):                            
        """ Stock: h_susceptible_rich =                      
                 self.arrival_airtravel_passengers_susceptible()-self.departure_airtravel_passengers_susceptible()-\
		self.rich_pop_human_infection()-self.rich_pop_sexual_transmission()                          
                                             
        Initial Value: self.inital_susceptible_rich()                    
        Do not overwrite this function       
        """                                  
        return self.state["h_susceptible_rich"]              
                                             
    def dh_symptomatic_infectious_rich_dt(self):                       
        return self.arrival_airtravel_passengers_symptomatic()+self.rich_pop_human_incubation()-self.departure_airtravel_passengers_symptomatic()-self.rich_pop_human_recovery()                           

    def h_symptomatic_infectious_rich_init(self):                      
        return self.initial_infectious_rich_sym()                           

    def h_symptomatic_infectious_rich(self):                            
        """ Stock: h_symptomatic_infectious_rich =                      
                 self.arrival_airtravel_passengers_symptomatic()+self.rich_pop_human_incubation()-self.departure_airtravel_passengers_symptomatic()-self.rich_pop_human_recovery()                          
                                             
        Initial Value: self.initial_infectious_rich_sym()                    
        Do not overwrite this function       
        """                                  
        return self.state["h_symptomatic_infectious_rich"]              
                                             
    def total_human_population(self):
        """Type: Flow or Auxiliary
        """
        return self.poor_population()+self.rich_population() 

    def dh_exposed_rich_dt(self):                       
        return self.arrival_airtravel_passengers_exposed()+self.rich_pop_human_infection()+self.rich_pop_sexual_transmission()-self.departure_airtravel_passengers_exposed()-self.rich_pop_asym_incubation()-self.rich_pop_human_incubation()                           

    def h_exposed_rich_init(self):                      
        return self.initial_exposed_rich()                           

    def h_exposed_rich(self):                            
        """ Stock: h_exposed_rich =                      
                 self.arrival_airtravel_passengers_exposed()+self.rich_pop_human_infection()+self.rich_pop_sexual_transmission()-self.departure_airtravel_passengers_exposed()-self.rich_pop_asym_incubation()-self.rich_pop_human_incubation()                          
                                             
        Initial Value: self.initial_exposed_rich()                    
        Do not overwrite this function       
        """                                  
        return self.state["h_exposed_rich"]              
                                             
    def dh_recovered_immune_rich_dt(self):                       
        return self.arrival_airtravel_passengers_recovered()+self.rich_pop_asym_human_recovery()+self.rich_pop_human_recovery()-self.departure_airtravel_passengers_recovered()                           

    def h_recovered_immune_rich_init(self):                      
        return self.initial_recovered_rich()                           

    def h_recovered_immune_rich(self):                            
        """ Stock: h_recovered_immune_rich =                      
                 self.arrival_airtravel_passengers_recovered()+self.rich_pop_asym_human_recovery()+self.rich_pop_human_recovery()-self.departure_airtravel_passengers_recovered()                          
                                             
        Initial Value: self.initial_recovered_rich()                    
        Do not overwrite this function       
        """                                  
        return self.state["h_recovered_immune_rich"]              
                                             
    def delaytime_of_reporting(self):
        """Type: Flow or Auxiliary
        """
        return 14 

    def diagnose_zika_case(self):
        """Type: Flow or Auxiliary
        """
        return (self.rich_pop_human_incubation()+self.pop_poor_human_incubation())*self.share_reported_cases() 

    def ddiagnosed_zika_cases_dt(self):                       
        return self.diagnose_zika_case()-self.report_case()                           

    def diagnosed_zika_cases_init(self):                      
        return self.init_diagnosed_cases()                           

    def diagnosed_zika_cases(self):                            
        """ Stock: diagnosed_zika_cases =                      
                 self.diagnose_zika_case()-self.report_case()                          
                                             
        Initial Value: self.init_diagnosed_cases()                    
        Do not overwrite this function       
        """                                  
        return self.state["diagnosed_zika_cases"]              
                                             
    def dreported_cases_dt(self):                       
        return self.report_case()                           

    def reported_cases_init(self):                      
        return self.init_reported_cases()                           

    def reported_cases(self):                            
        """ Stock: reported_cases =                      
                 self.report_case()                          
                                             
        Initial Value: self.init_reported_cases()                    
        Do not overwrite this function       
        """                                  
        return self.state["reported_cases"]              
                                             
    def rich_pop_asym_human_recovery(self):
        """Type: Flow or Auxiliary
        """
        return self.h_asymptomatic_infectious_rich()/self.recovery_period_human() 

    def rich_pop_asym_incubation(self):
        """Type: Flow or Auxiliary
        """
        return (self.h_exposed_rich()*(1-self.share_symptomatic_humans()))/self.intrinsic_incubation_period() 

    def rich_pop_human_incubation(self):
        """Type: Flow or Auxiliary
        """
        return (self.share_symptomatic_humans()* self.h_exposed_rich())/self.intrinsic_incubation_period() 

    def rich_pop_human_recovery(self):
        """Type: Flow or Auxiliary
        """
        return self.h_symptomatic_infectious_rich()/self.recovery_period_human() 

    def rich_pop_sexual_transmission(self):
        """Type: Flow or Auxiliary
        """
        return self.rich_pop_sexual_intercourse_per_person_and_day()*self.share_viremic_poor_population()*self.h_susceptible_rich()*self.transmission_probability_sexual_transmission() 

    def zika_cases(self):
        """Type: Flow or Auxiliary
        """
        return self.pop_poor_asym_human_incubation()+self.pop_poor_human_incubation()+self.rich_pop_asym_incubation()+self.rich_pop_human_incubation() 

    def ratio_infectious_mosquitos(self):
        """Type: Flow or Auxiliary
        """
        return self.m_infectious()/self.total_adult_mosquito_population() 

    def normal_blood_meals_a_day(self):
        """Type: Flow or Auxiliary
        """
        return 1.5 

    def dh_symptomatic_infectious_poor_dt(self):                       
        return self.pop_poor_human_incubation()-self.pop_poor_human_recovery()                           

    def h_symptomatic_infectious_poor_init(self):                      
        return self.initial_infectious_poor_sym()                           

    def h_symptomatic_infectious_poor(self):                            
        """ Stock: h_symptomatic_infectious_poor =                      
                 self.pop_poor_human_incubation()-self.pop_poor_human_recovery()                          
                                             
        Initial Value: self.initial_infectious_poor_sym()                    
        Do not overwrite this function       
        """                                  
        return self.state["h_symptomatic_infectious_poor"]              
                                             
    def pop_poor_human_incubation(self):
        """Type: Flow or Auxiliary
        """
        return (self.share_symptomatic_humans()* self.h_exposed_poor())/self.intrinsic_incubation_period() 

    def rich_pop_infectious(self):
        """Type: Flow or Auxiliary
        """
        return self.h_symptomatic_infectious_rich()+self.h_asymptomatic_infectious_rich() 

    def pop_poor_asym_human_incubation(self):
        """Type: Flow or Auxiliary
        """
        return (self.h_exposed_poor()*(1-self.share_symptomatic_humans()))/self.intrinsic_incubation_period() 

    def pop_poor_asym_human_recovery(self):
        """Type: Flow or Auxiliary
        """
        return self.h_asymptomatic_infectious_poor()/self.recovery_period_human() 

    def dh_asymptomatic_infectious_poor_dt(self):                       
        return self.pop_poor_asym_human_incubation()-self.pop_poor_asym_human_recovery()                           

    def h_asymptomatic_infectious_poor_init(self):                      
        return self.initial_infectious_poor_asym()                           

    def h_asymptomatic_infectious_poor(self):                            
        """ Stock: h_asymptomatic_infectious_poor =                      
                 self.pop_poor_asym_human_incubation()-self.pop_poor_asym_human_recovery()                          
                                             
        Initial Value: self.initial_infectious_poor_asym()                    
        Do not overwrite this function       
        """                                  
        return self.state["h_asymptomatic_infectious_poor"]              
                                             
    def dh_exposed_poor_dt(self):                       
        return self.pop_poor_human_infection()+self.pop_poor_sexual_transmission()-self.pop_poor_asym_human_incubation()-self.pop_poor_human_incubation()                           

    def h_exposed_poor_init(self):                      
        return self.initial_exposed_poor()                           

    def h_exposed_poor(self):                            
        """ Stock: h_exposed_poor =                      
                 self.pop_poor_human_infection()+self.pop_poor_sexual_transmission()-self.pop_poor_asym_human_incubation()-self.pop_poor_human_incubation()                          
                                             
        Initial Value: self.initial_exposed_poor()                    
        Do not overwrite this function       
        """                                  
        return self.state["h_exposed_poor"]              
                                             
    def dh_recovered_immune_poor_dt(self):                       
        return self.pop_poor_asym_human_recovery()+self.pop_poor_human_recovery()                           

    def h_recovered_immune_poor_init(self):                      
        return self.initial_recovered_poor()                           

    def h_recovered_immune_poor(self):                            
        """ Stock: h_recovered_immune_poor =                      
                 self.pop_poor_asym_human_recovery()+self.pop_poor_human_recovery()                          
                                             
        Initial Value: self.initial_recovered_poor()                    
        Do not overwrite this function       
        """                                  
        return self.state["h_recovered_immune_poor"]              
                                             
    def dh_susceptible_poor_dt(self):                       
        return -self.pop_poor_human_infection()-self.pop_poor_sexual_transmission()                           

    def h_susceptible_poor_init(self):                      
        return self.inital_susceptible_poor()                           

    def h_susceptible_poor(self):                            
        """ Stock: h_susceptible_poor =                      
                 -self.pop_poor_human_infection()-self.pop_poor_sexual_transmission()                          
                                             
        Initial Value: self.inital_susceptible_poor()                    
        Do not overwrite this function       
        """                                  
        return self.state["h_susceptible_poor"]              
                                             
    def pop_poor_human_infection(self):
        """Type: Flow or Auxiliary
        """
        return self.mosquito_bites_poor_pop()*self.ratio_infectious_mosquitos()*self.poor_pop_ratio_of_susceptible_people()*self.transmission_probability_vector_to_human() 

    def pop_poor_human_recovery(self):
        """Type: Flow or Auxiliary
        """
        return self.h_symptomatic_infectious_poor()/self.recovery_period_human() 

    def poor_pop_infectious(self):
        """Type: Flow or Auxiliary
        """
        return self.h_symptomatic_infectious_poor()+self.h_asymptomatic_infectious_poor() 

    def initial_infectious_poor_asym(self):
        """Type: Flow or Auxiliary
        """
        return 5 

    def initial_exposed_poor(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def initial_infectious_poor_sym(self):
        """Type: Flow or Auxiliary
        """
        return 10 

    def intrinsic_incubation_period(self):
        """Type: Flow or Auxiliary
        """
        return 5.5 

    def poor_pop_ratio_of_susceptible_people(self):
        """Type: Flow or Auxiliary
        """
        return self.h_susceptible_poor()/self.total_human_population() 

    def recovery_period_human(self):
        """Type: Flow or Auxiliary
        """
        return 5 

    def poor_pop_sexual_intercourse_per_person_and_day(self):
        """Type: Flow or Auxiliary
        """
        return 0.2 

    def pop_poor_sexual_transmission(self):
        """Type: Flow or Auxiliary
        """
        return self.poor_pop_sexual_intercourse_per_person_and_day()*self.share_viremic_poor_population()*self.h_susceptible_poor()*self.transmission_probability_sexual_transmission() 

    def share_symptomatic_humans(self):
        """Type: Flow or Auxiliary
        """
        return 0.2 

    def transmission_probability_sexual_transmission(self):
        """Type: Flow or Auxiliary
        """
        return 0.1 

    def rich_pop_ratio_of_susceptible_people(self):
        """Type: Flow or Auxiliary
        """
        return self.h_susceptible_rich()/self.total_human_population() 

    def rich_pop_sexual_intercourse_per_person_and_day(self):
        """Type: Flow or Auxiliary
        """
        return 0.2 

    def initial_infectious_rich_asym(self):
        """Type: Flow or Auxiliary
        """
        return 5 

    def initial_infectious_rich_sym(self):
        """Type: Flow or Auxiliary
        """
        return 10 

    def initial_exposed_rich(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def ratio_of_susceptible_mosquitos(self):
        """Type: Flow or Auxiliary
        """
        return self.m_susceptible()/self.total_adult_mosquito_population() 

    def mosquito_s_death(self):
        """Type: Flow or Auxiliary
        """
        return self.mosquito_probability_decease()*self.m_susceptible() 

    def dm_infectious_dt(self):                       
        return self.incubation_mosquito()+self.vertical_transmission_of_zika_viruses()-self.mosquito_i_death()                           

    def m_infectious_init(self):                      
        return self.intial_infectious_m()                           

    def m_infectious(self):                            
        """ Stock: m_infectious =                      
                 self.incubation_mosquito()+self.vertical_transmission_of_zika_viruses()-self.mosquito_i_death()                          
                                             
        Initial Value: self.intial_infectious_m()                    
        Do not overwrite this function       
        """                                  
        return self.state["m_infectious"]              
                                             
    def vertical_transmission_infection_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def normal_mosquito_renewal_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.15 

    def mosquito_i_death(self):
        """Type: Flow or Auxiliary
        """
        return self.m_infectious()*self.mosquito_probability_decease() 

    def mosquito_e_death(self):
        """Type: Flow or Auxiliary
        """
        return self.m_exposed()*self.mosquito_probability_decease() 

    def vertical_transmission_of_zika_viruses(self):
        """Type: Flow or Auxiliary
        """
        return self.m_infectious()*self.vertical_transmission_infection_rate()*self.normal_mosquito_renewal_rate() 

    def total_adult_mosquito_population(self):
        """Type: Flow or Auxiliary
        """
        return self.m_exposed()+self.m_infectious()+self.m_susceptible() 

    def extrinsic_incubation_period(self):
        """Type: Flow or Auxiliary
        """
        return 7 

    def incubation_mosquito(self):
        """Type: Flow or Auxiliary
        """
        return self.m_exposed()/self.extrinsic_incubation_period() 

    def final_time(self):
        """Type: Flow or Auxiliary
        """
        return 2 

    def initial_time(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def saveper(self):
        """Type: Flow or Auxiliary
        """
        return self.time_step() 

    def time_step(self):
        """Type: Flow or Auxiliary
        """
        return 1 

