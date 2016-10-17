## Modeling and simulating the Zika outbreak under deep uncertainty

#### Author Philipp Schwarz, 

#### Researcher in Policy Analysis Section, Delft University of Technology, The Netherlands

This repository contains all Python scripts that were used to produce the simulation results, however data and outcomes will only be made available once journal paper has been published.

***In a Nutshell*** 

Large-scale simulation model to study worldwide potential Zika outbreaks. 
Methodological contributions: (1) Pulls in big (geo-referenced) data from different sources combining high-resolution raster data, census data and model-based predictions on global air travel [(Mao et al. 2015)](https://dx.doi.org/10.7554/eLife.15272) and Aedes Mosquito species distribution [(Messina et al. 2016)](https://dx.doi.org/10.7554/eLife.15272). (2) Account for deep uncertainty by sampling over high dimensional uncertainty space [(Kwakkel and Pruyt 2013)](Exploratory Modeling and Analysis, an Approach for Model-Based Foresight under Deep Uncertainty.) (3) Cope with seasonal dynamics by making use of monthly resolved exogenous data, (4) Ensure computational efficiency by switching from stochastic to differential equation-based model.


***Simulation input data***

To achieve a fast computational model on global scope but at the same time address subnational heterogneity. The world was divided into regions smaller than countries. Adjacent provinces within nations that are similiar with respect to vector presence were joined to one single regional unit. Furthermore, whenever possible high-resolution raster data rather than census data (typically reported on country level) was used to inform the parameterization of the model elements.

The figure below illustrates the conversion from raw raster map to the level of aggregation of the compuational model on the example of population.

Raw raster dataset         |  Vector data after pre-processing
:-------------------------:|:-------------------------:
<img src="figs/population_raster_data.png" width="420"/>  |  <img src="figs/population_aggregated_low_Res_hig_res.png" width="420"/> 

For vector presence and air travel monthly resolved data were used. The following animations show the vector presence of Aedes Aegypti and Aedes Albopictus respectively. Raw raster dataset were produced by Moritz Kraemer and Oliver Brady (2016).

Aedes Aegypti         |  Aedes Albopictus
:-------------------------:|:-------------------------:
<img src="figs/Animation_Aegypti_v2.gif" width="600"/>  |  <img src="figs/Animation_Albopictus_v2.gif" width="600"/> 


***Computation***

Preprocessing and postprocessing sripts (Jupyter Notebooks) were run in the indicated order using my personal laptop. 
* System: Virtual Environment Ubuntu 14.04, 64 bit, Python 2.7
* Hardware: Intel Core i7-4500 CPU 1.80GHz - 2.40GHz, 2 Core(s), 4 Logical Processor(s), RAM 8GB)

Computational experiments were produced making use of high performance cluster provided by [Dominodatalab] (https://www.dominodatalab.com/). 


***Preliminary Results***
* Consistently over the complete ensemble of models, the recovery period (time human is infectious and can infect mosquito when being bitten) is the most important single variable that determines the speed of transmission and the Zika cases in the first wave of the global outbreak
* Travel plays a crucial role in the diffusion of the disease 
* The proposed integrated design method has proven to be useful to study Zika and could be applied with relatively little effort also to other vector-borne diseases such as malaria and dengue

***Please consider citing this Publication***

Schwarz P. Modeling and simulating the Zika outbreak under deep uncertainty | TU Delft Repositories [Internet]. Delft University of Technology; 2016 [cited 2016 Sep 19]. Available from: http://repository.tudelft.nl/islandora/object/uuid%3A4957df8e-3de1-4b5e-8231-731287a4ede4?collection=education
[Link](http://repository.tudelft.nl/islandora/object/uuid:4957df8e-3de1-4b5e-8231-731287a4ede4?collection=education)

***Future steps***

Upcoming journal paper

***License***

Data and scripts within this repository are released under the [CRAPL v0.1 License](http://matt.might.net/articles/crapl/).

[Contact me](philipp.schw@gmail.com)
