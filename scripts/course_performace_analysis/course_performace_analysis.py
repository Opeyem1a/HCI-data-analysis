import json
import os

import matplotlib.patches as pch
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def course_performance_analysis(GRADEBOOK_PATH, QUIZSCOREJSON_PATH):
    sns.color_palette('bright')
    file = pd.read_csv(GRADEBOOK_PATH)
    data448_ids = file['ID']
    quiz_ids = []
    final_score = file['Overall Final Score']

    overall_pre_test = file['Overall Pre-Tests (880658)']
    overall_post_test = file['Overall Post-Tests (880660)']
    overall_pre_post_grade = 40

    df_first_attempt = pd.DataFrame(
        columns=['DATA448_ID', 'QUIZ_ID', 'score', 'time', 'possible_points']
    )
    df_student_grade_first_attempt = pd.DataFrame(
        columns=['DATA448_ID', 'QUIZ_ID', 'total_score', 'total_possible_points', 'final_score', 'first_attempt_final_score']
    )
    df_average_student_attempts = pd.DataFrame(
        columns=['DATA448_ID', 'QUIZ_ID', 'attempt', 'final_score']
    )
    df_first_attempt_classification = pd.DataFrame(
        columns=['DATA448_ID', 'QUIZ_ID', 'submission_type']
    )
    # Get first attempt only quiz mark out of JSON files
    number_of_quizzes = 0
    for i in os.listdir(QUIZSCOREJSON_PATH):
        if i.endswith('.json'):
            number_of_quizzes += 1
            full_path = os.path.join(QUIZSCOREJSON_PATH, i)
            with open(full_path, 'r') as f:
                file = f.read()
                json_file = json.loads(file)
                if json_file:
                    if json_file[0]['quiz_points_possible'] > 0:
                        quiz_ids.append(json_file[0]['quiz_id'])
                for json_block in json_file:
                    if json_block['quiz_points_possible'] == 1.0:
                        student_average_attempt_data = {
                            'DATA448_ID': json_block['user_id'],
                            'QUIZ_ID': json_block['quiz_id'],
                            'submission_type': 'Survey'
                        }
                        df_first_attempt_classification = df_first_attempt_classification.append(student_average_attempt_data,
                                                                                         ignore_index=True)
                    elif json_block['quiz_points_possible'] > 0:
                        student_average_attempt_data = {
                            'DATA448_ID': json_block['user_id'],
                            'QUIZ_ID': json_block['quiz_id'],
                            'submission_type': 'Quiz'
                        }
                        df_first_attempt_classification = df_first_attempt_classification.append(
                            student_average_attempt_data,
                            ignore_index=True)

                    if json_block['quiz_points_possible'] > 0:
                        student_average_attempt_data = {
                            'DATA448_ID': json_block['user_id'],
                            'QUIZ_ID': json_block['quiz_id'],
                            'attempt': json_block['attempt'],
                            'final_score': json_block['kept_score'] / json_block['quiz_points_possible'] * 100
                        }
                        df_average_student_attempts = df_average_student_attempts.append(student_average_attempt_data,
                                                                                         ignore_index=True)
                        if json_block['attempt'] > 1:
                            for previous_json_block in json_block['previous_submissions']:
                                if previous_json_block['attempt'] == 1:
                                    json_block = previous_json_block
                        student_first_attempt_data = {
                            'DATA448_ID': json_block['user_id'],
                            'QUIZ_ID': json_block['quiz_id'],
                            'score': json_block['score'],
                            'time': json_block['time_spent'],
                            'possible_points': json_block['quiz_points_possible']
                        }
                        df_first_attempt = df_first_attempt.append(student_first_attempt_data, ignore_index=True)

    df_first_attempt_classification = df_first_attempt_classification.drop_duplicates(subset=["QUIZ_ID"])
    df_first_attempt = remove_survey_from_df(df_first_attempt, df_first_attempt_classification)
    df_average_student_attempts = remove_survey_from_df(df_average_student_attempts, df_first_attempt_classification)
    quiz_ids = remove_survey_from_list(quiz_ids, df_first_attempt_classification)

    for index, data448_id in enumerate(data448_ids):
        df_student_first_attempts = df_first_attempt.loc[df_first_attempt['DATA448_ID'] == data448_id]
        df_student_first_attempts = remove_survey_from_df(df_student_first_attempts,
                                                               df_first_attempt_classification)

        total_score = df_student_first_attempts['score'].sum()
        total_possible_points = df_student_first_attempts['possible_points'].sum()
        final_score_percentage = final_score[index]

        pre_test_grade = overall_pre_test[index]
        post_test_grade = overall_post_test[index]
        first_attempt_final_score_percentage = (total_score / total_possible_points) * overall_pre_post_grade

        first_attempt_final_score = final_score_percentage - (
                pre_test_grade + post_test_grade) + first_attempt_final_score_percentage

        df_student_grade_first_attempt = df_student_grade_first_attempt.append({
            'DATA448_ID': data448_id,
            'total_score': total_score,
            'total_possible_points': total_possible_points,
            'final_score': final_score,
            'first_attempt_final_score': first_attempt_final_score,
        }, ignore_index=True)

    # First attempt only score mean and std
    mean = df_student_grade_first_attempt['first_attempt_final_score'].mean()
    standard_dev = df_student_grade_first_attempt['first_attempt_final_score'].std()
    quantile_25percent = df_student_grade_first_attempt['first_attempt_final_score'].quantile(.25)
    median = df_student_grade_first_attempt['first_attempt_final_score'].median()
    quantile_75percent = df_student_grade_first_attempt['first_attempt_final_score'].quantile(.75)

    # Actual Score mean and std
    current_mean = final_score.mean()
    current_standard_dev = final_score.std()

    w_2016_avg, w_2016_std = 79.93, 7.9
    w_2017_avg, w_2017_std = 78.70, 16.2
    w_2018_avg, w_2018_std = 85.97, 8.8
    w_2019_avg, w_2019_std = 83.81, 10.0
    w_2020_retrieve_avg, w_2020_retrieve_std = 90.80, 10.5
    w_2020_calculated_avg, w_2020_calculated_std = current_mean, current_standard_dev
    w_2020_first_attempt_avg, w_2020_first_attempt_std = mean, standard_dev

    winter_averages = [w_2016_avg, w_2017_avg, w_2018_avg, w_2019_avg, w_2020_retrieve_avg, w_2020_calculated_avg,
                       w_2020_first_attempt_avg]
    winter_deviations = [w_2016_std, w_2017_std, w_2018_std, w_2019_std, w_2020_retrieve_std, w_2020_calculated_std,
                         w_2020_first_attempt_std]
    winter_labels = ['W2016', 'W2017', 'W2018', 'W2019', 'W2020', 'C W2020', 'F 2020']

    # print out the statistics significant value of the first attempt final score.
    print('25% quantile: ' + str(quantile_25percent), ' Median: ' + str(median),
          ' 75% quantile: ' + str(quantile_75percent), ' Mean: ' + str(mean),
          ' Standard Deviation: ' + str(standard_dev))

    # 1) Histogram comparison plot for Actual score and First attempt only score
    fig, (ax1) = plt.subplots(1)
    data_graph_colors = ['b', 'r']
    for index, data in enumerate([final_score, df_student_grade_first_attempt['first_attempt_final_score']]):
        sns.histplot(data, kde=True, bins=30, line_kws={'linewidth': 1}, color=data_graph_colors[index], ax=ax1).set(
            title='Overall Score vs First Attempt Score',
            xlabel='Grade',
            ylabel='Number of Students')
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_yticks(range(0, 25, 3))
    score_legend = pch.Patch(color=data_graph_colors[0], label='Overall Score')
    first_attempt_legend = pch.Patch(color=data_graph_colors[1], label='First Attempt Score')
    ax1.legend(handles=[score_legend, first_attempt_legend])
    fig.tight_layout()
    plt.savefig(f'overall_vs_first_attempt.png')
    plt.close()

    # 2) Histogram comparison plot for Actual score and First attempt only score
    fig, (ax1) = plt.subplots(1)
    sns.histplot(final_score, kde=True, bins=30, line_kws={'linewidth': 1}, ax=ax1).set(
        title='Overall Score vs First Attempt Score',
        xlabel='Grade',
        ylabel='Number of Students')
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_yticks(range(0, 25, 3))
    fig.tight_layout()
    plt.savefig(f'course_performance.png')
    plt.close()

    # 3) Mean and Standard Deviation graph
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.barh(winter_labels, winter_averages, xerr=winter_deviations, capsize=3)
    ax1.set_xticks(range(40, 110, 10))
    ax1.set_xticklabels([f'{i}%' for i in range(40, 110, 10)])
    ax1.set_xlim([40, 110])
    ax1.set_title('Yearly Winter Term Grade History')

    ax2.errorbar(winter_labels, winter_averages, yerr=winter_deviations, capsize=4)
    ax2.set_yticks(range(60, 105, 5))
    fig.tight_layout()
    plt.savefig(f'mean_and_standard_deviation.png')
    plt.close()

    # 4) Students grades to attempts taken for each quiz
    for quiz_id in quiz_ids:
        students_per_quiz = df_average_student_attempts.loc[df_average_student_attempts['QUIZ_ID'] == quiz_id]

        quiz_attempt_grade_data = {
            'final_score': list(students_per_quiz['final_score']),
            'attempts': list(students_per_quiz['attempt'])
        }
        df = pd.DataFrame(quiz_attempt_grade_data)

        fig = sns.jointplot(x='final_score', y='attempts', kind='reg', data=df)
        fig.set_axis_labels('Final Score', 'Attempts')
        fig.ax_marg_x.set_xlim(0, 110)
        fig.ax_marg_y.set_ylim(0, 4)
        fig.figure.suptitle(f'Final Score vs Attempts Taken For Quiz {quiz_id}')
        fig.figure.tight_layout()
        plt.savefig(f'final_score_vs_attempts_{quiz_id}.png')
        plt.close()

    plt.show()


def remove_survey_from_df(df, classification_df):
    for index, row in classification_df.iterrows():
        if row["submission_type"] == "Survey":
            quiz_id = row["QUIZ_ID"]
            df = df[df.QUIZ_ID != quiz_id]
    return df


def remove_survey_from_list(lst, classification_df):
    for index, row in classification_df.iterrows():
        if row["submission_type"] == "Survey":
            quiz_id = row["QUIZ_ID"]
            lst.remove(quiz_id)
    return lst


if __name__ == '__main__':
    quiz_path = os.path.join(os.getcwd(), 'quizzes')
    course_performance_analysis('grade_book.csv', quiz_path)
