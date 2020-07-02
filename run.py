#!/usr/bin/env python

import os
import sys
import numpy as np
import pandas as pd

from libplot import plot_by_date, plot_by_case

def get_populations():
    p0 = pd.read_csv("census.csv", encoding="ISO-8859-1")
    p = p0[['STATE', 'COUNTY', 'STNAME', 'CTYNAME', 'POPESTIMATE2019']]
    p = p.rename(columns={"POPESTIMATE2019": "n"})
    return p

def get_data():
    us_all = pd.read_csv("nytimes/us.csv")
    by_state = pd.read_csv("nytimes/us-states.csv")
    by_county = pd.read_csv("nytimes/us-counties.csv")
    #
    us_all['date'] = pd.to_datetime(us_all['date'])
    by_state['date'] = pd.to_datetime(by_state['date'])
    by_county['date'] = pd.to_datetime(by_county['date'])
    return us_all, by_state, by_county

def get_county_data(state_name, county_name, by_county, p):
    data = {}
    #
    county_data = by_county[(by_county.state == state_name) & (by_county.county == county_name)]
    #
    fips = county_data.fips.to_numpy()[0].astype(int)
    fips_state = int(fips/1000)
    fips_county = int(fips%1000)
    populations = p[(p['STATE'] == fips_state) & (p['COUNTY'] == fips_county)]['n'].to_numpy()
    if len(populations) == 0: return None
    data['norm'] = populations[0]/1e6
    #
    data['date'] = county_data['date']
    data['cases'] = county_data['cases'].to_numpy()
    data['deaths'] = county_data['deaths'].to_numpy()
    data['cases.incr'] = np.concatenate([[0], data['cases'][1:] - data['cases'][:-1]])
    data['deaths.incr'] = np.concatenate([[0], data['deaths'][1:] - data['deaths'][:-1]])
    return data

def get_state_data(state_name, by_state, p):
    data = {}
    #
    state_data = by_state[by_state.state == state_name]
    #
    fips = state_data.fips.to_numpy()[0]
    populations = p[(p['STATE'] == fips) & (p['COUNTY'] == 0)]['n'].to_numpy()
    if len(populations) == 0: return None
    data['norm'] = populations[0]/1e6
    #
    data['date'] = state_data['date']
    data['cases'] = state_data['cases'].to_numpy()
    data['deaths'] = state_data['deaths'].to_numpy()
    data['cases.incr'] = np.concatenate([[0], data['cases'][1:] - data['cases'][:-1]])
    data['deaths.incr'] = np.concatenate([[0], data['deaths'][1:] - data['deaths'][:-1]])
    return data

def get_us_data(us_all, p, state_s):
    populations = 0
    for state in state_s:
        n = p[(p.STNAME == state) & (p.CTYNAME == state)]['n'].to_numpy()
        if len(n) > 0:
            populations += n[0]
    #
    data = {}
    data['norm'] = populations/1e6
    data['date'] = us_all['date']
    data['cases'] = us_all['cases'].to_numpy()
    data['deaths'] = us_all['deaths'].to_numpy()
    data['cases.incr'] = np.concatenate([[0], data['cases'][1:] - data['cases'][:-1]])
    data['deaths.incr'] = np.concatenate([[0], data['deaths'][1:] - data['deaths'][:-1]])
    return data

def main():
    populations = get_populations()
    us_all, by_state, by_county = get_data()
    state_s = np.unique(by_state['state'].to_numpy())
    #
    us_data = get_us_data(us_all, populations, state_s)
    multiple_states = [get_state_data(state, by_state, populations) for state in state_s]
    #
    pltargs_date = plot_by_date("_all_", us_data, multiple=multiple_states)
    pltargs_case = plot_by_case("_all_", us_data, multiple=multiple_states)
    pltargs_date_norm = plot_by_date("_all_", us_data, multiple=multiple_states, norm=True)
    pltargs_case_norm = plot_by_case("_all_", us_data, multiple=multiple_states, norm=True)
    #
    plot_by_date("_US_", us_data, **pltargs_date)
    plot_by_case("_US_", us_data, **pltargs_case)
    plot_by_date("_US_", us_data, norm=True, **pltargs_date_norm)
    plot_by_case("_US_", us_data, norm=True, **pltargs_case_norm)
    #
    for data,state in zip(multiple_states, state_s):
        if data is None: continue
        print (state)
        plot_by_date(state, data, **pltargs_date)
        plot_by_case(state, data, **pltargs_case)
        plot_by_date(state, data, norm=True, **pltargs_date_norm)
        plot_by_case(state, data, norm=True, **pltargs_case_norm)

    ingham_MI = get_county_data("Michigan", "Ingham", by_county, populations)
    plot_by_date("Michigan.Ingham", ingham_MI)
    plot_by_case("Michigan.Ingham", ingham_MI)
    plot_by_date("Michigan.Ingham", ingham_MI, norm=True)
    plot_by_case("Michigan.Ingham", ingham_MI, norm=True)
    
if __name__ == '__main__':
    main()
