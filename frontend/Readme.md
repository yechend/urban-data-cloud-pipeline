# Front End Visualization Guide

## Description
CCC_frontend_combined integrated all visualization functions for each scenarios. It use buttons to provide an interactive front end.

## Scenario matched python files
1. **SUDO**: generate bar charts and interactive map of regional population

   ```
   populationVisual.py
   ```

2. **Traffic congestion**: path1.py plots a map with routes. congestion_statistic can generate bar chart with input value date and area id. Area id information can be obtained from the map generated in path1.py.

```bash
path1.py
congestion_statistic.py
```

3. **Pedestrians**: ped_Visual has 4 functions. Two generates bar charts with pedestrians count by hour and sensor separately. Two plots maps for sensor location and pedestrians distribution.

```bash
ped_Visual.py
```

4. **Mastodon**: Produce some statistical analysis plots:

```bash
mastodon_helper.py

```

5. **Train Service**: Due to the broken of the cinder, the visualization of the train service based on the results we got before it broke. Two html files provide maps for station information and all railway line. Pictures in trainservice folder are the generated plots.

```bash
trainservice folder
all_station_info.html
line_railway.html
```