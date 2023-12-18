from random import random
from scipy.stats import norm
from math import exp

# def total_demand_i(household, usage, householdvehicle, day, vehiclechance, energyvehicle):
#     energy_demand_household = usage / 365 * norm.ppf(random(), loc = 1, scale = 0.05)
#     while random < vehiclechance:
#         energy_demand_household += energyvehicle)
#         vehiclechance -= 1
#     return energy_demand_household

# def total_generated_i(energytable, day, total_energy, solarpanels):
#     energy_generated = energytable[day] / total_energy * solarpanels
#     return energy_generated

# def minimizing_function(demand_hour, buy_price, excess_hour, sell_price):
#     for hour in range(1, 25):
#         total_profit = demand_hour * buy_price - excess_hour * sell_price
#     return total_profit

# Solar in 001.xlsx levert data voor zonne energie op


def plan_new(appliance, starttime, duration):
    return 0


def change(planning, appliance, hour):
    return 0


def swap(planning, appliance1, appliance2):
    copyplanning = planning
    return copyplanning


def energy_bought(planning):
    bought = 0
    return bought


def send_update():
    return 0


def calc_price():
    return


def sort():
    return


def send_to_frontend():
    return


def initialize(
    household,
    planning,
    day,
    appliances,
    total_demand_i,
    total_excess_energy_hour,
):
    # Plan alles van eigen huizen in
    for house in household:
        for hour in range(1, 25):
            i = 0
            while total_excess_energy_hour[house, hour] >= 0:
                appliances = sort(appliance.loc[house, "power"])
                plan(appliances[i], hour, hour + appliance.loc[i, "duration"])
                i += 1
    # Plan de rest in

    for appliance in appliances:
        if appliance in planning:
            continue
        for hour in range(1, 25):
            if (
                appliance not in planning
                and total_excess_energy_hour[hour]
                < appliance.loc[house, "power"]
            ):
                plan(appliance, hour)


def local_optimum(planning, appliances):
    bestcost = 0
    previouscost = 1
    while bestcost < previouscost():
        bestcost = energy_bought(planning)
        previouscost = bestcost
        price = calc_price(planning)
        for appliance in appliances:
            for hour in range(0, 24):
                copyplanning = change(planning, appliance, hour)
                if energy_bought(copyplanning) < bestcost:
                    temporary_best_planning = copyplanning
                    send_to_frontend(appliance, hour, price)
                    bestcost = energy_bought(planning)
        planning = temporary_best_planning
    return planning


def simulated_annealing(
    planning,
    appliances,
    start_iteration_count,
    end_iteration_count,
    frequency_frontend,
    kmax,
):
    bestplanning = planning
    bestcost = energy_bought(bestplanning)
    for i in range(start_iteration_count, end_iteration_count):
        if i % frequency_frontend == 0:
            send_update(bestplanning)
        temperature = 1 - (i + 1) / kmax
        copyplanning = swap(
            planning,
            random.int(0, len(appliances) - 1),
            random.int(0, len(appliances) - 1),
        )
        energy_bought_current = energy_bought(copyplanning)
        energy_bought_previous = energy_bought(planning)
        if (
            energy_bought_current < energy_bought_previous
            or exp(
                -(energy_bought_current - energy_bought_previous) / temperature
            )
            < random.random()
        ):
            planning = copyplanning
            if energy_bought(planning) < bestcost:
                bestplanning = planning
                bestcost = energy_bought_current
