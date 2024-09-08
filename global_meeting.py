def get_free_slots(busy_slots, day_start=0, day_end=24):
    """
    Given a list of busy time slots, return the free time slots in a given day.
    busy_slots: List of tuples [(start_time, end_time), ...]
    day_start: Start time of the day (default 0)
    day_end: End time of the day (default 24)
    """
    if not busy_slots:
        return [(day_start, day_end)]

    busy_slots.sort()  # Sort busy slots by start time
    free_slots = []

    # Check for a free slot before the first busy slot
    if busy_slots[0][0] > day_start:
        free_slots.append((day_start, busy_slots[0][0]))

    # Check for free slots between busy slots
    for i in range(len(busy_slots) - 1):
        if busy_slots[i][1] < busy_slots[i + 1][0]:
            free_slots.append((busy_slots[i][1], busy_slots[i + 1][0]))

    # Check for a free slot after the last busy slot
    if busy_slots[-1][1] < day_end:
        free_slots.append((busy_slots[-1][1], day_end))

    return free_slots

def find_common_free_time_week(student_schedules):
    """
    Find common free time slots across all students for each day of the week.
    student_schedules: Dictionary where keys are student majors and values are dictionaries with day-wise busy slots.
    """
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    common_free_slots_week = {}

    for day in days_of_week:
        all_free_slots = []

        # Calculate free slots for each student's schedule for the current day
        for major, schedule in student_schedules.items():
            busy_slots = schedule.get(day, [])
            free_slots = get_free_slots(busy_slots)
            all_free_slots.append(free_slots)

        # Find the intersection of all free slots for the current day
        if all_free_slots:
            common_free_slots = all_free_slots[0]
            for slots in all_free_slots[1:]:
                common_free_slots = intersect_slots(common_free_slots, slots)
            common_free_slots_week[day] = common_free_slots
        else:
            common_free_slots_week[day] = [(0, 24)]

    return common_free_slots_week

def intersect_slots(slots1, slots2):
    """
    Find intersection of two lists of time slots.
    slots1, slots2: Lists of tuples representing time slots.
    """
    intersection = []
    i, j = 0, 0

    while i < len(slots1) and j < len(slots2):
        start = max(slots1[i][0], slots2[j][0])
        end = min(slots1[i][1], slots2[j][1])

        if start < end:  # There is an overlap
            intersection.append((start, end))

        # Move to the next slot
        if slots1[i][1] < slots2[j][1]:
            i += 1
        else:
            j += 1

    return intersection

# Example Usage
student_schedules = {
    "Major_1": {
        "Monday": [],
        "Tuesday": [(8, 11), (12, 15)],
        "Wednesday": [(12, 15), (16, 19)],
        "Thursday": [(13, 15)],
        "Friday": [(8, 11)],
    },
    "Major_2": {
        "Monday": [(9, 12), (13, 15)],
        "Tuesday": [(16, 18)],
        "Wednesday": [(12, 15), (16, 18)],
        "Thursday": [],
        "Friday": [(9, 12)],
    },
    "Major_3": {
        "Monday": [(8, 12)],
        "Tuesday": [(8, 10), (12, 15)],
        "Wednesday": [(16, 19)],
        "Thursday": [(13, 17)],
        "Friday": [(8, 11), (13, 16)],
    },
    "Major_4": {
        "Monday": [],
        "Tuesday": [(8, 18)],
        "Wednesday": [(16, 19)],
        "Thursday": [(12, 15)],
        "Friday": [(8, 11)],
    }
    # ,
    # "Major_5": {
    #     "Monday": [(9, 10), (12, 13), (15, 18)],
    #     "Tuesday": [(8, 9), (11, 13)],
    #     "Wednesday": [(9, 11), (13, 15)],
    #     "Thursday": [(8, 10), (13, 14)],
    #     "Friday": [(10, 12), (14, 16)],
    # }
}

common_free_slots_week = find_common_free_time_week(student_schedules)
for day, slots in common_free_slots_week.items():
    print(f"{day}: {slots}")

# The Result so far (SE, CSC, DCE, CE) (in that order) 
# Monday: [(12, 13), (15, 24)]
# Tuesday: [(18, 24)]
# Wednesday: [(8, 12), (15, 16), (19, 24)]
# Thursday: [(8, 12), (17, 24)]
# Friday: [(12, 13), (16, 24)]
# Saturday: [(0, 24)]
# Sunday: [(0, 24)]