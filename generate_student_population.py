import random
import json
import csv
from util_names import FIRST_NAMES, LAST_NAMES

"""
Generates a CSV file that represents the student population at a school.
"""

# To make everything deterministic
random.seed(12345)

# The grades offered at school.
#GRADES = ['K','1st','2nd','3rd','4th','5th']
GRADES = [0, 1, 2, 3, 4, 5]

# Families have 1 .. 4 chidlren, according to the following distribution
HOW_MANY_KIDS_PER_FAMILY = [1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,4]

POPULATION_SIZE = 600


## MAIN LOOP

count = 0
family_id = 1
kid_id = 1
STUDENTS = []

pick_one = random.choice

while count < POPULATION_SIZE:
  # generate a random family
  last_name = pick_one(LAST_NAMES)
  for i in range(0, pick_one(HOW_MANY_KIDS_PER_FAMILY)):
    STUDENTS.append({ 'id': kid_id,
                  'family_id': family_id,
                  'last_name': last_name,
                  'first_name': pick_one(FIRST_NAMES),  # we pick a random first name
                  'grade': pick_one(GRADES) })          # we pick a random grade
    kid_id += 1
    count += 1
  family_id += 1

# We write a CSV file
with open('student-population.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Student ID', 'First Name', 'Last Name', 'Family ID', 'Grade'])
    for s in STUDENTS:
        writer.writerow([s['id'], s['first_name'], s['last_name'], s['family_id'], s['grade']])
print('csv written to student-population.csv.')

# We write a JSON file
with open('student-population.json', 'w') as json_file:
  json.dump(STUDENTS, json_file, indent=True)
print('json written to student-population.json.')