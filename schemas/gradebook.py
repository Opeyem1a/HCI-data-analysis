class GradeBookSchema:
    STUDENT_NAME = 'Student'
    STUDENT_ID = 'ID'
    SECTION = 'Section'
    LECTURE = 'Lecture'
    LAB = 'Lab'
    OVERALL_PROJECT_SCORE = 'Project Final Score'
    OVERALL_MAIN_ACTIVITIES_SCORE = 'Main Activities Final Score'
    OVERALL_TUTORIAL_ACTIVITIES_SCORE = 'Tutorial Activities Final Score'
    OVERALL_PRE_POST_TESTS_SCORE = 'Pre/Post Tests Final Score'
    OVERALL_READING_LOGS_SCORE = 'Reading Logs Final Score'
    OVERALL_COURSE_SCORE = 'Final Score'
    FINAL_SCORE = 'Overall Final Score'
    PRE_TEST_SCORE = 'Overall Pre-Tests (880658)'
    POST_TEST_SCORE = 'Overall Post-Tests (880660)'
    COMBINED_PRE_POST_WORTH = 40
    TOTAL_QUIZ_POSSIBLE_SCORE = 84  # not including post/pre test 0 and post/pre test 9 since not in the gradebook
