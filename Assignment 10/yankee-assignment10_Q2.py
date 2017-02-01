import random
import math
import operator
import pandas as pd
import numpy as np
import pylab as plt


def gini_coefficient(tables, guests):
    size_of_table = len(tables)
    table_shared = {}

    for table in tables:
        table_shared[table] = tables[table] / guests

    count = 0
    for table in table_shared:
        count += table_shared[table]

    count = count / size_of_table
    count = 2 * count

    temp = 0
    for i in table_shared:
        for j in table_shared:
            temp += abs(table_shared[i] - table_shared[j])

    temp = temp / (math.pow(size_of_table, 2))
    gini = temp / count

    return gini


def draw_plot(list1, list2, list3, list4, list5):
    x = len(list1) * [0]
    for i in range(0, len(x)):
        x[i] = i + 1

    plt.xticks(np.arange(0, 1001, 100))
    plt.ylim(0, 1)
    plt.title("Gini Coeficient plot")
    plt.xlabel("Subjects")
    plt.ylabel("Gini Coefficient")

    plt.plot(x, list1, label='simulation1', color="b")
    plt.plot(x, list2, label='simulation2', color="r")
    plt.plot(x, list3, label='simulation3', color="g")
    plt.plot(x, list4, label='simulation4', color="y")
    plt.plot(x, list5, label='simulation5', color="k")
    plt.legend(loc=0, fontsize='small')
    plt.show()


def sitting_at_tables(number_of_customers):
    tables_dict = {}
    all_gini = 1000 * [0]
    tables_dict[1] = 1
    number_of_tables = 1
    total_number_of_guests = 1
    re = gini_coefficient(tables_dict, total_number_of_guests)
    all_gini[total_number_of_guests - 1] = re

    for i in range(2, number_of_customers + 1):

        total_number_of_guests += 1
        found = 0
        rand = random.random()
        for table in tables_dict:

            prob = tables_dict[table] / total_number_of_guests
            if rand < prob:
                tables_dict[table] += 1
                found = 1
                re = gini_coefficient(tables_dict, total_number_of_guests)
                all_gini[total_number_of_guests - 1] = re
                break

        if found == 0:
            number_of_tables += 1
            tables_dict[number_of_tables] = 1
            re = gini_coefficient(tables_dict, total_number_of_guests)
            all_gini[total_number_of_guests - 1] = re

    return all_gini


number_of_customers = 1000


gini_1 = sitting_at_tables(number_of_customers)
gini_2 = sitting_at_tables(number_of_customers)
gini_3 = sitting_at_tables(number_of_customers)
gini_4 = sitting_at_tables(number_of_customers)
gini_5 = sitting_at_tables(number_of_customers)

draw_plot(gini_1, gini_2, gini_3, gini_4, gini_5)
