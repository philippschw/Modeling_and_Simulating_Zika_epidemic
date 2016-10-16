# Function generates list that maps the simulation timestep with the month

from itertools import cycle
import numpy as np

def set_up(Simulation_time, Month_before_startup):
	days_in_month_list =  [31, 28, 31, 30,31,30, 31, 31, 30, 31, 30, 31]
	months_lst = list(np.linspace(1, 12, 12))
	month = cycle(months_lst)

	for i in xrange(Month_before_startup):
		m = int(month.next())

	days = 0
	lst_sim_time_month = []
	for i in np.linspace(1, Simulation_time, Simulation_time):
		if days <= 1:
		    m = int(month.next())
		    days = (days_in_month_list[m-1])
		days -= 1
		lst_sim_time_month.append(m)
		
	return lst_sim_time_month
#=================================
