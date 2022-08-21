# Instructions for setting up a new year

____
## Table of Contents:
### Before the semester
1. [ Part 1: Course Materials Repo](#coursemat)
1. [ Part 2: Forecasting Repo](#forecast)
1. [ Part 3: Homework and GitHub Classroom](#homework)
1. [ Part4: First week of class](#week1)


## Before the semester
___
<a name="coursemat"></a>
## Part 1: Setup the Course materials repo
0. If you don't have it already clone the master organization locally so you can use this to populate things.

1. Create an organization for the semester
- just use the free option
- Naming convention HAS-Tools-FallXX
- Go to settings and add 'Third-Party applications': Add GitKraken, GitHub Classroom, and atom GitHub package

2. Create a new empty repo called 'Course-MaterialsYY' (yy=current year)

3. Create a folder for the organization locally and clone the new course materials repo into this folder.

4. Copy the readme from the Git-Master course materials into this semester
  -  First check that links are all working and also check with the previous semester that this is up to Dataset

5. Update the syllabus and add this to the course materials repo main folder

6. Make folders for 'Assignments' and 'Content' in the new course repo.

7. Copy the Cheat Sheets into the Content Folder

7. Update assignment 1 in the master repo as needed and then copy into the assignments folder

___
<a name="forecast"></a>
## Part 2: Update the forecasting repo

1. Update the forecast dates in the **master** forcasting repo:
  1. Update `Weekly_Forecast_Dates.xls`
  2. Export this table to pdf,  take a picture of the table and copy it into the `ReadMe.md`
  3. Update the dates in the evaluator assignments of the readme
  4. Update the dates in the `scoreboard.md` file
  5. Update the dates in the `forecaste_entries/forecast_template.csv`

3. Create a forecasting repo in the organization for this years course
-  Make it public and use the naming convention "ForecastingYY"

4. Copy the initial materials from the master into this years competition:
  - Main `ReadMe.md` and `assets` folder
  - `Forecast_entries/forecast_template.csv`
  - To be continued

5. Copy the `Forecast_entries/forecast_template.csv` to create a csv for every student naming convention `lastname.csv`

6. Modify the getLastNames and getFirstNames functions in the `eval_functions.py` script

___
<a name="homework"></a>
## Part 3: Setup the Homework Template and GitHub classroom
1. Review the `Homework_Template` repo on the master organization and make any setup changes you wan there.
2. Login to github classroom and create a new classroom
  -  link to the **organizaiton for the current year**
  -  Name HAS Tools Master-classroom-YY
  - skip  other steps
3. Create a new assigment using the master Homework_Template
  - Assignment title: homework
  - Visibility: public
  - Grant students admin access: yes
  - Select template repository: HAS-Tools-Master/Homework_Template
  - Add a supported editor: VS Code
  - Copy the invitation link and add it to the week 1 assignment instructions
4. Create a homework_grading folder and copy the ReadMe, Token and mass_clone folder into this repo

___
<a name="week1"></a>
## Part 4: First week of class



# next steps --
- Record videos



- Go through the evaluation scripts folder and the outputs when I do my first forecast. Update them in the master, then pull them into this years.  Update step 4 above with what all needs to be copied into the inital forecast repo
