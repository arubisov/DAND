#!/usr/bin/env python3

import csv

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        return list(reader)

def fix_acct(arr):
    for row in arr:
        row['account_key'] = row['acct']
        del row['acct']
    return arr

def unique_students(arr):
    keys = set( [row['account_key'] for row in arr] )
    return keys

enrollments = read_csv('enrollments.csv')
daily_engagement = fix_acct(read_csv('daily_engagement.csv'))
project_submissions = read_csv('project_submissions.csv')

### For each of these three tables, find the number of rows in the table and
### the number of unique students in the table. To find the number of unique
### students, you might want to create a set of the account keys in each table.


enrollment_num_rows = len(enrollments)             # Replace this with your code
enrollment_num_unique_students = len(unique_students(enrollments))  # Replace this with your code

engagement_num_rows = len(daily_engagement)             # Replace this with your code
engagement_num_unique_students = len(unique_students(daily_engagement))  # Replace this with your code

submission_num_rows = len(project_submissions)             # Replace this with your code
submission_num_unique_students = len(unique_students(project_submissions))  # Replace this with your code

numweird = 0
for row in enrollments:
    if row['account_key'] not in unique_students(daily_engagement):
        if row['days_to_cancel'] != '0':
            numweird = numweird + 1

print(numweird)