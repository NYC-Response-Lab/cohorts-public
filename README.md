This is the source code used for our [Medium article](https://medium.com/nyc-response-lab/helping-school-reopening-using-operation-research-cfbb421fefde).

`python generate_student_population.py` is used to generate a fake student population.

`python solver_base.py` is used to compute a valid assignment. It assumes the existence of `student-population.csv`.

# To run the code
* install a Python virtual env: `python3 -m venv .py-env`
* activate the virtual env: `. .py-env/bin/activate`
* install the dependencies: `pip install -r requirements.txt`
* run the code (see above)