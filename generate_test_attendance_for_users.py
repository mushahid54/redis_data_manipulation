from itertools import count
import json
import random
import redis
import datetime
r = redis.StrictRedis()


def set_attendance_data():
    """
        Generating random user_id with random attendance type and set data to redis.
    :return:
    """
    user_list = []
    for user_id in range(1, 1000000+1):
        attendance = random.choice(["present", "absent", "leave"])
        user_list.append({
            "user_id": user_id,
            "attendance": attendance,
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        })

        # if attendance == "present":
        #     r.setbit(user_list, user_id, 1)
        # if attendance == "absent":
        #     r.setbit(user_list, user_id, 0)

    serialized_data = json.dumps(user_list)
    set_data_to_redis = r.set("data", serialized_data)



############### Set data to Redis #############

set_data_to_redis = set_attendance_data()
alist = json.loads(r.get("data"))

##############################################


#get_all_data = r.get("data")



def get_count_of_present_attendance(alist):
    """
        Checking user present or absent at particular day and calculating the count for that day.
    :param alist:
    :return:
    """
    present_list = []
    absent_list = []
    for item in alist:
        if item['attendance'] == "present":
            present_list.append(item)
        if item['attendance'] in ["absent", "leave"]:
            absent_list.append(item)
    final_dict = {"number_of_present_user_attendance": len(present_list), "number_of_absent_user_attendance": len(absent_list), "date": str(alist[0]['date'])}

    return final_dict


def binary_search(alist, item):
    user_details_found = dict()
    number_of_attendance = get_count_of_present_attendance(alist)
    first = 0
    last = len(alist)-1
    while first <= last:
        midpoint = (first + last)//2
        if alist[midpoint]['user_id'] == item:
            user_details_found = {
                "user_id": alist[midpoint]['user_id'],
                "attendance": str(alist[midpoint]['attendance'])
            }
            break
        else:
            if item < alist[midpoint]['user_id']:
                last = midpoint-1
            else:
                first = midpoint+1
    return user_details_found, number_of_attendance

find_attendance_by_user_id = binary_search(alist, 74)
print find_attendance_by_user_id
