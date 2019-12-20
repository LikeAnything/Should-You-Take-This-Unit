from statistics import mean
from statistics import stdev
import csv

# stat columns columns in the csv that we care about
csv_stat_cols = [
    'Unit',
    'Campus',
    'Semester',
    'Learning outcomes were clear',
    'Assessments were clear',
    'Assessments allowed me to demonstrate the learning outcomes',
    'Feedback helped me achieve the learning outcomes',
    'Resources helped me achieve the learning outcomes',
    'Is satisfied with the unit',
]

def stats_from_data_set(data_list):
    data_mean = mean(data_list)
    data_std = stdev(data_list)
    return data_mean, data_std


def calculate_score(raw, data_stats):
    score = ((raw - data_stats[0]) / data_stats[1]) + 3
    if score < 0:
        score = 0
    if score > 5:
        score = 5
    return score


def read_csv():
    csv_file = open("data.csv", "r")
    reader = csv.DictReader(csv_file)

    data_list = []
    for row in reader:
        data_list.append(row)

    sorted_list = sorted(data_list, key=lambda x: x["Unit"])
    csv_file.close()

    # new_list = []
    # i = 1
    # while i < len(sorted_list) - 1:
    #     if sorted_list[i]["Unit"] == sorted_list[i+1]["Unit"]:
    #         combined_item = [sorted_list[i][0], sorted_list[i][1]]
    #         for j in range(2, len(sorted_list[i])):
    #             combined_item.append((float(sorted_list[i][j]) + float(sorted_list[i+1][j])) / 2)
    #         new_list.append(combined_item)
    #         i += 2
    #     else:
    #         new_list.append(sorted_list[i])
    #         i += 1

    unit_codes = []
    campus = []
    year = []
    semester = []

    assessment = []
    feedback = []
    satisfaction = []
    resources = []
    activities = []

    for row in sorted_list:
        unit_codes.append(row["Unit"])
        campus.append(row["Campus"])
        year.append(row["Year"])
        semester.append(row["Semester"])

        assessment.append((float(row['Assessments were clear']) +
                          float(row['Assessments allowed me to demonstrate the learning outcomes'])) /2 )
        feedback.append(float(row['Feedback helped me achieve the learning outcomes']))
        satisfaction.append(float(row['Resources helped me achieve the learning outcomes']))
        resources.append(float(row['Activities helped me achieve the learning outcomes']))
        activities.append(float(row['Is satisfied with the unit']))

    # for i in range(1, len(new_list)):
    #     unit_codes.append(new_list[i][0])
    #     assessment.append((float(new_list[i][3]) + float(new_list[i][4])) / 2)
    #     feedback.append(float(new_list[i][5]))
    #     resources.append(float(new_list[i][6]))
    #     activities.append(float(new_list[i][7]))
    #     satisfaction.append(float(new_list[i][9]))

    assessment_stats = stats_from_data_set(assessment)
    feedback_stats = stats_from_data_set(feedback)
    satisfaction_stats = stats_from_data_set(satisfaction)
    resources_stats = stats_from_data_set(resources)
    activities_stats = stats_from_data_set(activities)

    standardised = []

    for i in range(len(unit_codes)):
        unit = unit_codes[i]
        c = campus[i]
        y = year[i]
        s = semester[i]
        assessment_score = calculate_score(float(assessment[i]), assessment_stats)
        feedback_score = calculate_score(float(feedback[i]), feedback_stats)
        satisfaction_score = calculate_score(float(satisfaction[i]), satisfaction_stats)
        resources_score = calculate_score(float(resources[i]), resources_stats)
        activities_score = calculate_score(float(activities[i]), activities_stats)

        standardised.append([unit, c, y, s, assessment_score, feedback_score, satisfaction_score, resources_score,
                             activities_score])

    return standardised


def generate_javascript():
    output_file = open("jsData.js", "w")
    html_list = open("html_list.html", "w")
    standardised = read_csv()
    function_declaration = "function data() { \n return ["
    output_file.write(function_declaration)

    for unit in standardised:
        html_list.write("<option value='" + unit[0] + "'>" + "\n")
        new_block = "{ \n"
        new_block += "unitCode: '" + unit[0] + "'," + "\n"
        new_block += "campus: '" + unit[1] + "'," + "\n"
        new_block += "year: '" + unit[2] + "'," + "\n"
        new_block += "semester: '" + unit[3] + "'," + "\n"
        new_block += "assessment: " + str(unit[4]) + "," + "\n"
        new_block += "feedback: " + str(unit[5]) + "," + "\n"
        new_block += "satisfaction: " + str(unit[6]) + "," + "\n"
        new_block += "resources: " + str(unit[7]) + "," + "\n"
        new_block += "activities: " + str(unit[8]) + "," + "\n"
        new_block += "},"
        output_file.write(new_block)
    output_file.write("]")
    output_file.write("}")
    html_list.close()
    output_file.close()


generate_javascript()
