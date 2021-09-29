import re
import pandas as pd
import os
from schemas import DataFilesSchema

ANSWER_OPTIONS = {
    "Strongly Disagree": -2,
    "Disagree": -1,
    "Neither Agree Nor Disagree": 0,
    "Agree": 1,
    "Strongly Agree": 2
}


def clean_background_survey():
    """
    Prepares and cleans the dataframe so it is possible to use it for clustering.
    Fixes the single column with all the questions in it.
    """
    df = pd.read_csv(DataFilesSchema.BACKGROUND_SURVEY_DATA)
    df = df.drop(df.columns[1:13], axis=1).drop(df.columns[14:19], axis=1).dropna()
    questions = list(df.columns)[1]
    new_columns = _get_columns(questions)

    row_index = 1
    for row in df.itertuples():
        answers = row[2].split(",")
        column_index = 0
        for column in new_columns:
            if column_index < len(answers):
                df.at[row_index, column] = _map_to_number(answers[column_index])
            column_index += 1
        row_index += 1
    df.drop(df.columns[1], axis=1)
    return df


def _get_columns(questions):
    """
    This separates the questions into a list so they can be used to update the columns in the dataframe.
    :param questions: a string of the questions to process.
    """
    new_columns = []
    for question in questions.splitlines():
        substring = re.search(r"\[(.*?)]", question)
        if substring:
            new_columns.append(substring.group(1).replace("_", " "))
    return new_columns


def _map_to_number(answer):
    """
    Map a number to the student's answer.
    :param answer: the answer to map.
    """
    return ANSWER_OPTIONS[answer]


if __name__ == "__main__":
    data = clean_background_survey()
    output_dir = os.path.join(DataFilesSchema.OUTPUT_DIRECTORY, "processed_background_survey" + '.csv')
    data.to_csv(output_dir, index=False)
