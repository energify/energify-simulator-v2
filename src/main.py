from sys import argv
from profile import Profile
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

    community = Community(
        community_name, f"environments/{environment_name}.txt")

    for n in range(houses_num):
        people_num = int(abs(random.normal(3, 1)))
        if people_num == 0:
            people_num += 1
        panels_area = int(abs(random.normal(3, 10)))
        community.add_house(House(profile, panels_area, people_num))

    community.save()
    community.start_simulation(interval)
    community.show_simulation(3600)

elif mode == "load":
    community_name = argv[2]
    interval = int(argv[3])
    community = Community.load(f"communities/{community_name}.pkl")
    community.start_simulation(interval)
