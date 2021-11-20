from operator import index
from typing import Mapping
from sqlalchemy import create_engine, Table, Column,Integer, String,Boolean, MetaData
from sqlalchemy.sql.expression import true

engine = create_engine("sqlite:///mydb1.db", echo = True)
meta = MetaData()
data = Table(
   'Study', meta, 
   Column('USN', String, primary_key = True), 
   Column('student_name', String),
   Column('Gender', String),
   Column('Entry_type', String),
   Column('YOA', Integer),
   Column('migrated', Boolean),
   Column('Details_of_migration', String),
   Column('admission_in_separate_division',Boolean),
   Column('adDetails', String),
   Column('YOP', Integer),
   Column('degree_type', String),
   Column('pu_marks', Integer),
   Column('entrance_marks', Integer),
)
meta.create_all(engine)

conn = engine.connect()

def create():
    N=int(input("Enter the number of student's details to be entered: "))
    for i in range(N):
        sUSN = input("Enter USN: ")
        sName = input("Enter the Name: ")
        sGender = input("Enter the Gender: ")
        sEntry_type = input("Enter the Entry type of students: ")
        sYearOfAdmission = input("Enter the year of admission: ")
        sMigrated = input("Has the student migrated to other programs / Institutions\nEnter Yes or No : ")
        if sMigrated == "Yes":
            sMigrated = True
        elif sMigrated == "No":
            sMigrated =  False
        sDetails = input("Enter the details of migration: ")
        sadmissionInSepDiv = input("Is the student has admission in separate division - Yes / No: ")
        if sadmissionInSepDiv == "Yes":
            sadmissionInSepDiv = True
        elif sadmissionInSepDiv == "No":
            sadmissionInSepDiv =  False
        admissionDetails = input("Enter the details: ")
        sYop = input("Enter the year of passing: ")
        sDegreeType = input("Enter the Degree: ")
        sPuMarks = input("Enter your PU Marks: ")
        sEntranceExams = input("Enter entrance exam marks: ")

        
        result = conn.execute(data.insert(),[
            {'USN' : sUSN, 'student_name' : sName, 'Gender' : sGender, 'Entry_Type': sEntry_type,'YOA': sYearOfAdmission, 'migrated': sMigrated,
             'Details_of_migration': sDetails, 'admission_in_separate_division': sadmissionInSepDiv,'adDetails': admissionDetails ,'YOP': sYop, 'degree_type': sDegreeType,
             'pu_marks': sPuMarks, 'entrance_marks': sEntranceExams}
        ])

def read():
    dataview = data.select()
    result = conn.execute(dataview)
    for row in result:
        print (row)
    

def update():
    option = int(input("Press 1 to update a parameter of a student:\nPress 2 to update a range of parameters: "))

    if option == 1:
        student_selected = input("Please provide the USN of the student: ")
        print("Please select the parameter to be updated: ")
        while(True):
            parameter = int(input(("""
                    Press 1 to update student name
                    Press 2 to update the Gender
                    Press 3 to update entry
                    Press 4 to update Year of admission
                    Press 5 to update migration status
                    Press 6 to update migration details
                    Press 7 to update separate division admission status
                    Press 8 to update Year of passing
                    Press 9 to update degree type
                    Press 10 to update PU Marks
                    Press 11 to update entrance marks: 
                    Press 0 to stop updating: """)))
            parameter_dict = {1:'student_name', 2:'Gender', 3: 'entry_type', 4:'YOA', 5:'migrated', 6:'details of migration',
                    7: 'admission_in_separate_division', 8:'YOP', 9:'degree_type', 10: 'pu_marks', 11: 'entrance_marks'}
            if parameter != 0:
                selection = parameter_dict[parameter]
                stripped = selection.strip('')
                new = input("Enter the "+ selection+ " values: ")
                updated = data.update().where(data.c.USN==student_selected).values(stripped = new)
                result = conn.execute(updated)
            elif parameter == 0:
                break
    elif option == 2:
        dict_input = input("Input the dictionary: ")
        dict_input = eval(dict_input)
        match = dict_input['USN']
        for key, value in dict_input.items():
            print(key,value)
            updated = data.update().where(data.c.USN==match).values(key = value)
        result = conn.execute(updated)
        
def delete():
    option = int(input("Enter the USN of the element to be deleted: "))
    deleted = data.delete().where(data.c.USN == option)
    result = conn.execute(deleted)
    read()
    
    
operation_dict = {1: create, 2: read,3: update, 4: delete}

while(True):
    operation = int(input("""To perform the following operations: 
          Press 1 to enter new values:
          Press 2 to view the table: 
          Press 3 to update the records: 
          Press 4 to delete a record: """))
    performing = operation_dict[operation]()
