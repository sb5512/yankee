import math
import operator
import pandas as pd
import numpy as np
import pylab as plt

df = pd.read_table(r'onlyhash.data')

# renaming data frame with meaningful column name
df.columns = ['user', 'date', 'hash_tag']


# returns all the unique values from a given column
def get_unique_values(data_frame, column):
    return data_frame[column].unique()


# removes all the rows whose given column contains term value
def remove_noise(data_frame, column, term):
    unwanted_data_frame = data_frame[data_frame[column].str.contains(term)]
    for unwanted_value in unwanted_data_frame[column].unique():
        data_frame = data_frame[data_frame[column] != unwanted_value]

    return data_frame


dataFrame = remove_noise(df, 'date', r'\\')
unique_dates = get_unique_values(dataFrame, 'date')

system_entropy_dict = {}
user_entropy_dict = {}


def get_data_frame_with_matching_values(data_frame, column, value):
    return data_frame[data_frame[column] == value]


def convert_hash_tags_to_list_of_hash_tags(hash_tags):
    list_of_hash_tags = []
    if isinstance(hash_tags, str):
        split_hash_tags = hash_tags.split()
        for split_hash_tag in split_hash_tags:
            list_of_hash_tags.append(split_hash_tag)
        return list_of_hash_tags
    for row_hash_tag in hash_tags:
        if row_hash_tag.count('#') > 1:
            split_row_hash_tags = row_hash_tag.split()
            for split_row_hash_tag in split_row_hash_tags:
                list_of_hash_tags.append(split_row_hash_tag)
        else:
            list_of_hash_tags.append(row_hash_tag)
    return list_of_hash_tags


def calculate_entropy_for_a_day(hash_tags):
    entropy = 0
    hash_tag_set = set(hash_tags)
    for unique_hash_tag in hash_tag_set:
        f_u_i = hash_tags.count(unique_hash_tag) / (len(hash_tags))
        entropy_of_one_hash_tag = (f_u_i * math.log2(f_u_i))
        entropy += entropy_of_one_hash_tag
    return entropy


def calculate_average_entropy_of_a_day(total_entropy, total_count):
    return total_entropy / total_count


count = 0

# for each unique date calculate system entropy and user entropy
for unique_date in unique_dates:
    # df_for_uniqueDate = dataFrame[dataFrame.date == unique_date]
    df_for_uniqueDate = get_data_frame_with_matching_values(dataFrame, \
                                                          'date', unique_date)
    all_possible_hash_tags = df_for_uniqueDate['hash_tag']
    total_users_entropy = 0
    # each iteration of this loop deals with a user's hashtags
    for user_hash_tags in all_possible_hash_tags:
        user_hash_tag_list = convert_hash_tags_to_list_of_hash_tags(user_hash_tags)
        user_entropy_for_a_day = calculate_entropy_for_a_day(user_hash_tag_list)
        total_users_entropy = (total_users_entropy + (-1 * user_entropy_for_a_day))

    average_users_entropy = calculate_average_entropy_of_a_day\
                                (total_users_entropy, len(user_hash_tag_list))

    # add average user entropy for each day as dictionary value
    user_entropy_dict[count] = average_users_entropy

    all_individual_hash_tag_in_a_day = convert_hash_tags_to_list_of_hash_tags\
                                                       (all_possible_hash_tags)
    total_system_entropy_for_a_day = -1 * calculate_entropy_for_a_day\
                                            (all_individual_hash_tag_in_a_day)

    average_system_entropy_for_a_day = calculate_average_entropy_of_a_day\
                                     (total_system_entropy_for_a_day, \
                                      len(all_individual_hash_tag_in_a_day))

    # add average user entropy for each day as dictionary value
    system_entropy_dict[count] = average_system_entropy_for_a_day
    count += 1

sorted_system_entropy = sorted(system_entropy_dict.items(), \
                                               key=operator.itemgetter(1))

sorted_user_entropy_dict_based_on_system_entropy = {}
count = 0
new_data_frame = pd.DataFrame()
# new_data_frame.columns = ['sno', 'system_entropy', 'user_entropy']
for key, value in sorted_system_entropy:
    sorted_user_entropy_dict_based_on_system_entropy[count] = \
                                                    user_entropy_dict.get(key)
    count += 1
    temp = pd.DataFrame([[count, value, user_entropy_dict.get(key)]])
    new_data_frame = new_data_frame.append(temp)

plt.xlabel("Day(0-384): 0 being the lowest system entropy and 384 the highest.")
plt.ylabel("Entropy")
system_entropy_plot = plt.scatter(new_data_frame[0], new_data_frame[1], \
                      color='r', marker='o', label='System entropy', alpha=0.5)
user_entropy_plot = plt.scatter(new_data_frame[0], new_data_frame[2], \
                        color='k', marker='x', label='User entropy', alpha=0.5)
plt.legend(handles=[system_entropy_plot, user_entropy_plot])
plt.show()

