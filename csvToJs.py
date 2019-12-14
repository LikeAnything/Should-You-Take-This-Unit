from statistics import mean
from statistics import stdev


def stats_from_data_set(data_list):
    data_mean = mean(data_list)
    data_std = stdev(data_list)
    return data_mean, data_std


def calculate_score(raw, data_stats):
    return ((raw - data_stats[0]) / data_stats[1]) + 3


def read_csv():
    csv_file = open("data.csv", "r")
    data_list = []
    for line in csv_file:
        data_list.append(line.strip().split(","))

    sorted_list = sorted(data_list, key=lambda x: x[0])

    new_list = []

    i = 1

    while i < len(sorted_list) - 1:
        if sorted_list[i][0] == sorted_list[i+1][0]:
            combined_item = [sorted_list[i][0], sorted_list[i][1]]
            for j in range(2, len(sorted_list[i])):
                combined_item.append((float(sorted_list[i][j]) + float(sorted_list[i+1][j])) / 2)
            new_list.append(combined_item)
            i += 2
        else:
            new_list.append(sorted_list[i])
            i += 1

    csv_file.close()
    unit_codes = []
    assessment = []
    feedback = []
    satisfaction = []
    resources = []
    activities = []

    for i in range(1, len(new_list)):
        unit_codes.append(new_list[i][0])
        assessment.append((float(new_list[i][3]) + float(new_list[i][4])) / 2)
        feedback.append(float(new_list[i][5]))
        resources.append(float(new_list[i][6]))
        activities.append(float(new_list[i][7]))
        satisfaction.append(float(new_list[i][9]))

    assessment_stats = stats_from_data_set(assessment)
    feedback_stats = stats_from_data_set(feedback)
    satisfaction_stats = stats_from_data_set(satisfaction)
    resources_stats = stats_from_data_set(resources)
    activities_stats = stats_from_data_set(activities)

    standardised = []

    for i in range(len(unit_codes)):
        unit = unit_codes[i]
        assessment_score = calculate_score(float(assessment[i]), assessment_stats)
        feedback_score = calculate_score(float(feedback[i]), feedback_stats)
        satisfaction_score = calculate_score(float(satisfaction[i]), satisfaction_stats)
        resources_score = calculate_score(float(resources[i]), resources_stats)
        activities_score = calculate_score(float(activities[i]), activities_stats)

        standardised.append([unit, assessment_score, feedback_score, satisfaction_score, resources_score,
                             activities_score])

    return standardised


def generate_javascript():
    output_file = open("jsData.js", "w")
    standardised = read_csv()
    function_declaration = "function data() { \n return ["
    output_file.write(function_declaration)

    for unit in standardised:
        new_block = "{ \n"
        new_block += "unitCode: '" + unit[0] + "'," + "\n"
        new_block += "assessment: " + str(unit[1]) + "," + "\n"
        new_block += "feedback: " + str(unit[2]) + "," + "\n"
        new_block += "satisfaction: " + str(unit[3]) + "," + "\n"
        new_block += "resources: " + str(unit[4]) + "," + "\n"
        new_block += "activities: " + str(unit[5]) + "," + "\n"
        new_block += "},"
        output_file.write(new_block)
    output_file.write("]")
    output_file.write("}")
    output_file.close()


generate_javascript()

    
    