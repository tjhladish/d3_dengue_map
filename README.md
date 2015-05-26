# How Visualization Works

## Data

There is a daily time series of infections, by districts in a larger administrative
region.  The series consists of a reference series, and intervention series (currently one other,
future multiple others?)

## Map

 - each map has boundaries specified by GIS data
   * *districts* specifying the areas which will display infection events
   * *admin* specifying any other boundaries
 - the district regions have meta-data
   * population
   * also name, id
 - the maps have distinct background colors, initially with 0 opacity.  opacity is
 modified as the simulation proceeds, with 1 corresponding to peak prevalence

## Time Series

 - the time series plot shows daily incidence for the reference and intervention
 series.
 - the sliding bar indicates roughly where the map display corresponds to the incidence series.
