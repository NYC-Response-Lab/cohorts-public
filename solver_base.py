from ortools.linear_solver import pywraplp
import csv
import json
import logging
import sys
from collections import defaultdict


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# We load the students info.

CLASS_PER_GRADE = { 0: 4, 1: 4, 2: 4, 3: 4, 4: 3, 5: 4}
NUMBER_OF_GROUPS = 3

with open('student-population.json', 'r') as json_file:
    student_data = json.load(json_file)
    log.info('Students loaded: %d.' % len(student_data))

students = { str(s['id']):s for s in student_data }
families = defaultdict(list)
for s in student_data:
    families[str(s['family_id'])].append(str(s['id']))

grades = list(set([s['grade'] for s in student_data]))
groups = [g for g in 'ABCDEFGH'][0:NUMBER_OF_GROUPS]
cohorts = [ ("%d%02d%c" % (grade, class_number, group)) \
        for grade in grades \
        for class_number in range(1,1+ CLASS_PER_GRADE[grade]) \
        for group in groups]
homerooms = sorted(list(set([c[0:3] for c in cohorts])))


# Returns True if cohort corresponds to grade `grade`.
def same_grade(cohort, grade):
    return str(grade) == cohort[0]

# Returns True if cohorts corresponds to group `group`.
def same_group(cohort, group):
    return group == cohort[-1]

# Returns True if cohort corresponds to homeroom `homeroom`. 
def same_homeroom(cohort, homeroom):
    return homeroom == cohort[0:3]

#####################
# Problem statement #
#####################

solver = pywraplp.Solver('StudentProjectGridCBC', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

matches = {}
for c in cohorts:
    for s in students:
        matches[c, s] = solver.IntVar(0, 1, 'matches[%s,%s]' % (c, s))


z = solver.Sum( matches[c, s]
                 for c in cohorts
                 for s in students )


###############
# Constraints #
###############

# 1 student <-> 1 CHR
for s in students:
    solver.Add(solver.Sum([matches[c, s] for c in cohorts]) == 1)

# Students MUST get a cohort that matches their grade level.
for s in students:
    grade = students[s]['grade']
    solver.Add(solver.Sum([matches[c, s] for c in cohorts if same_grade(c, grade)]) == 1)
 

# We put some limits on the size of each cohort
for c in cohorts:
  solver.Add(solver.Sum([matches[c, s] for s in students]) <= 12)
  solver.Add(solver.Sum([matches[c, s] for s in students]) >= 8)   # I could not go higher than that.

# We put some limits on the size of each group
for g in groups:
  solver.Add(solver.Sum([matches[c, s] for s in students for c in cohorts if same_group(c, g)]) <= 205)
  solver.Add(solver.Sum([matches[c, s] for s in students for c in cohorts if same_group(c, g)]) >= 185)


# Special Constraints

# Student 476 and Student 477 MUST NOT be in the same homeroom because of bullying.
for h in homerooms:
    solver.Add(solver.Sum(matches[c, s] for s in ['476', '477'] for c in cohorts if same_homeroom(c, h)) <= 1)

# Student 499 MUST be in homeroom 2nd-1 (201) because of special needs.
solver.Add(solver.Sum(matches[c, '499'] for c in cohorts if same_homeroom(c, "201")) == 1)

############
# We solve #
############
objective = solver.Minimize(z)
status = solver.Solve()
if status != pywraplp.Solver.OPTIMAL:
    logging.error('No solution found')
    sys.exit(-1)

logging.info('Solution found.')
log.info("Score: %f." % solver.Objective().Value())
log.info("Time: %d ms." % solver.WallTime())


assignments = []
for s in students:
    for c in cohorts: 
        if matches[c, s].SolutionValue() != 0:
            assignments.append({ 'id': s, 'cohort': c})

with open('student-assignment.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Student ID', 'Cohort'])
    for a in assignments:
        writer.writerow([a['id'], a['cohort']])
log.info('csv written to student-assignment.csv.')