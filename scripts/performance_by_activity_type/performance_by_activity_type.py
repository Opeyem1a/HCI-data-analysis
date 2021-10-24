import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from schemas import GradeBookSchema


def performance_by_activity_type(file_path):
    """

    :param file_path: the path to the gradebook csv.
    """
    gradebook = pd.read_csv(file_path)
    overall_score_cols = [GradeBookSchema.OVERALL_COURSE_SCORE, GradeBookSchema.OVERALL_PROJECT_SCORE,
                          GradeBookSchema.OVERALL_PRE_POST_TESTS_SCORE, GradeBookSchema.OVERALL_MAIN_ACTIVITIES_SCORE,
                          GradeBookSchema.OVERALL_TUTORIAL_ACTIVITIES_SCORE, GradeBookSchema.OVERALL_READING_LOGS_SCORE]
    overall_score_data = gradebook.loc[:, gradebook.columns.isin(overall_score_cols)].replace({0: np.nan})

    for col in overall_score_cols:
        # set up plot
        mean = overall_score_data[col].mean()
        stdev = overall_score_data[col].std()
        figure, ax = plt.subplots()

        # plot using seaborn distplot
        sns.distplot(overall_score_data[col], color='blue', ax=ax)

        # set the limits of the x-axis
        ax.set_xlim(0, 120)

        # Plot mean and 2 std deviations on either side
        plt.axvline(mean, label='mean', linestyle=':', color='red')
        plt.axvline(mean - stdev, label='standard deviation', linestyle='--', color='purple')
        plt.axvline(mean + stdev, linestyle='--', color='purple')
        plt.axvline(mean - 2 * stdev, linestyle='--', color='purple')
        plt.axvline(mean + 2 * stdev, linestyle='--', color='purple')
        plt.suptitle('Density Distribution of {}'.format(col))
        plt.legend()
        plt.show()
