from sys import argv
from profile import Profile
from time import sleep
from environment import Environment
from house import House
from community import Community
from numpy import random

mode = argv[1]
profile = Profile("profiles/profile-1.txt")


if mode == "new":
    community_name = argv[2]
    environment_name = argv[3]
    houses_num = int(argv[4])
    interval = int(argv[5])
    sleep_between_intervals = float(argv[6])

    environment = Environment(f"environments/{environment_name}.csv")
    community = Community(community_name, environment)

    for n in range(houses_num):
        people_num = int(abs(random.normal(3, 1)))
        if people_num == 0:
            people_num += 1

        panels_area = int(abs(random.normal(3, 10)))

        buy_price = round(abs(random.normal(1.15, 0.02)), 2)
        sell_price = round(abs(random.normal(buy_price, 0.01)), 2)
        while sell_price <= buy_price:
            sell_price = round(abs(random.normal(buy_price, 0.02)), 2)

        house = House(profile, panels_area, people_num)
        house.register()
        house.login()
        house.set_prices(buy_price, sell_price)
        house.establish_connection()
        community.add_house(house)

    # community.save()
    community.start_simulation(interval, sleep_between_intervals)
    # community.start_simulation_plot(interval, 24)

elif mode == "load":
    community_name = argv[2]
    interval = int(argv[3])
    community = Community.load(f"communities/{community_name}.pkl")
    community.start_simulation(interval)
