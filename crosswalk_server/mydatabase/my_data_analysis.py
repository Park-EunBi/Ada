'''
Data Analytics File
Edited by EunBi Park
8 Nov 2022
'''

from matplotlib import pyplot as plt
import sys

'''
description :
- Function to draw graph using csv file
params :
- None
return :
- None
'''

def make_graph():
    sys.path.append('..')
    data_day = open("./csv_data/count_by_day.csv")
    data_hour = open("./csv_data/count_by_hour.csv")
    data_user = open("./csv_data/count_by_user.csv")

    days = []
    counts = []

    for line in data_day:
        (day, count) = line.split(',')
        days.append(day)
        counts.append(int(count))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plt.plot(days, counts, color='green', marker='o', linestyle='solid')
    plt.title("Violators by date")
    plt.xlabel("Date")
    plt.ylabel("Violators")
    plt.savefig('count_by_day.png')

    times = []
    counts = []

    for line in data_hour:
        (time, count) = line.split(',')
        times.append(time)
        counts.append(int(count))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plt.plot(times, counts, color='blue', marker='o', linestyle='solid')
    plt.title("Violators by hour")
    plt.xlabel("Time")
    plt.ylabel("Violators")
    plt.savefig('count_by_hour.png')

    users = []
    counts = []

    for line in data_user:
        (user, count) = line.split(',')
        users.append(user)
        counts.append(int(count))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.bar(users,counts)
    plt.title("Top Violators")
    plt.xlabel("User_id")
    plt.ylabel("Violators")
    plt.savefig('count_by_user.png')