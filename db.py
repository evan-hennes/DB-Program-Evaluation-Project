from sqlalchemy import Column, Integer, String, ForeignKey, Text, create_engine, select, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, selectinload
from sqlalchemy.sql import Select

Base = declarative_base()


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    code = Column(String(4), unique=True)
    faculty = relationship("Faculty", backref="department")
    programs = relationship("Program", backref="department")


class Faculty(Base):
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    rank = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))


class Program(Base):
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    in_charge_id = Column(Integer, ForeignKey("faculty.id"))
    courses = relationship("Course", secondary="program_courses")


class Course(Base):
    __tablename__ = "courses"
    id = Column(String, primary_key=True)  # Department Code + 4-digit number
    title = Column(String)
    description = Column(Text)
    department_id = Column(Integer, ForeignKey("departments.id"))
    sections = relationship("Section", backref="course")


class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    semester = Column(String)
    course_id = Column(String, ForeignKey("courses.id"))
    instructor_id = Column(Integer, ForeignKey("faculty.id"))
    enrollment_count = Column(Integer)


class LearningObjective(Base):
    __tablename__ = "learning_objectives"
    id = Column(String, primary_key=True)
    description = Column(Text)
    parent_id = Column(String, ForeignKey("learning_objectives.id"))
    sub_objectives = relationship("LearningObjective")


class ProgramCourses(Base):
    __tablename__ = "program_courses"
    program_id = Column(Integer, ForeignKey("programs.id"), primary_key=True)
    course_id = Column(String, ForeignKey("courses.id"), primary_key=True)


class CourseObjectives(Base):
    __tablename__ = "course_objectives"
    id = Column(Integer, primary_key=True)
    course_id = Column(String, ForeignKey("courses.id"))
    objective_id = Column(String, ForeignKey("learning_objectives.id"))
    program_id = Column(Integer, ForeignKey("programs.id"))


class SectionEvaluations(Base):
    __tablename__ = "section_evaluations"
    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("sections.id"))
    objective_id = Column(String, ForeignKey("learning_objectives.id"))
    evaluation_method = Column(String)
    students_met = Column(Integer)


class SessionManager:

    def __init__(self, database_uri):
        self.engine = create_engine(database_uri)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_department(self, name, code):
        new_department = Department(name=name, code=code)
        self.session.add(new_department)
        self.session.commit()

    def add_faculty(self, name, email, rank, department_id):
        new_faculty = Faculty(name=name,
                              email=email,
                              rank=rank,
                              department_id=department_id)
        self.session.add(new_faculty)
        self.session.commit()

    def add_program(self, name, department_id, in_charge_id):
        new_program = Program(name=name,
                              department_id=department_id,
                              in_charge_id=in_charge_id)
        self.session.add(new_program)
        self.session.commit()

    def add_course(self, id, title, description, department_id):
        new_course = Course(id=id,
                            title=title,
                            description=description,
                            department_id=department_id)
        self.session.add(new_course)
        self.session.commit()

    def add_section(self, id, number, semester, course_id, instructor_id,
                    enrollment_count):
        new_section = Section(
            id=id,
            number=number,
            semester=semester,
            course_id=course_id,
            instructor_id=instructor_id,
            enrollment_count=enrollment_count,
        )
        self.session.add(new_section)
        self.session.commit()

    def add_learning_objective(self, id, description, parent_id=None):
        new_objective = LearningObjective(id=id,
                                          description=description,
                                          parent_id=parent_id)
        self.session.add(new_objective)
        self.session.commit()

    def assign_course_to_program(self, program_id, course_id):
        new_assignment = ProgramCourses(program_id=program_id,
                                        course_id=course_id)
        self.session.add(new_assignment)
        self.session.commit()

    def assign_objective_to_course(self, course_id, objective_id):
        new_assignment = CourseObjectives(course_id=course_id,
                                          objective_id=objective_id)
        self.session.add(new_assignment)
        self.session.commit()

    def add_section_evaluation(self, section_id, objective_id,
                               evaluation_method, students_met):
        new_evaluation = SectionEvaluations(
            section_id=section_id,
            objective_id=objective_id,
            evaluation_method=evaluation_method,
            students_met=students_met,
        )
        self.session.add(new_evaluation)
        self.session.commit()
    
    # def query(self, query):
    #     # Get column names from the query
    #     columns = []
    #     if isinstance(query, Select):
    #         columns = [col.name for col in query.selected_columns]

    #     # Execute the query
    #     results = self.session.execute(query)
    #     string = '\n'.join([','.join([str(getattr(row[0], col)) for col in columns]) for row in results])

    #     return [results, string]

    # def query(self, query):
    #     # Execute the query
    #     result = self.session.execute(query)

    #     # Check if it's a Select statement
    #     if isinstance(query, Select):
    #         # Get column names from the Select statement
    #         columns = [col.name for col in query.columns]

    #         # Convert rows to string
    #         results_str = '\n'.join([','.join([str(getattr(row[0], col)) for col in columns]) for row in result])

    #         return [result, results_str]

    #     else:
    #         # For non-select queries, return the raw result and an empty string
    #         return [result, ""]

    def query(self, query):
        # Execute the query
        result = self.session.execute(query)

        # Check if it's a Select statement
        if isinstance(query, Select):
            # Convert rows to string, including related objects
            results_str = '\n'.join([self.convert_row_to_string(row) for row in result.scalars().all()])
            return [result, results_str]

        else:
            # For non-select queries, return the raw result and an empty string
            return [result, ""]

    # Takes a DB object and converts it to a string
    def convert_row_to_string(self, row):
        row_str = '\n'.join([f"{col.name}: {getattr(row, col.name)}" for col in row.__table__.columns])

        # Handle related objects
        for relation in row.__mapper__.relationships.keys():
            related_objects = getattr(row, relation)
            related_str = '\n'.join([','.join([str(getattr(relation, col.name)) for col in relation.__table__.columns]) for relation in related_objects])
            row_str += f"\n{relation}: [{related_str}]"

        return row_str
    
    # List all of its programs
    def get_department_programs_by_id(self, department_id):
        [results, string] = self.query(select(Department).where(Department.id == department_id).options(selectinload(Department.programs)))
        return string
    def get_department_programs_by_name(self, department_name):
        [results, string] = self.query(select(Department).where(Department.name == department_name).options(selectinload(Department.programs)))
        return string

    # List all of its faculty (including what program each faculty is in charge of, if there is one)
    def get_department_faculty_by_id(self, department_id):
        [results, string] = self.query(select(Department).where(Department.id == department_id).options(selectinload(Department.faculty)))
        return string
    def get_department_faculty_by_name(self, department_name):
        [results, string] = self.query(select(Department).where(Department.name == department_name).options(selectinload(Department.faculty)))
        return string

    # List all the courses, together with the objectives/sub-objectives association with year
    def get_program_courses_by_id(self, program_id):
        [results, string] = self.query(select(Program).where(Program.id == program_id))
        return string
    def get_program_courses_by_name(self, program_name):
        [results, string] = self.query(select(Program).where(Program.name == program_name))
        return string
    
    # List all of the objectives
    def get_program_objectives_by_id(self, program_id):
        [results, string] = self.query(select(Program).where(Program.id == program_id))
        return string
    def get_program_objectives_by_name(self, program_name):
        [results, string] = self.query(select(Program).where(Program.name == program_name))
        return string

    # List all of the evaluation results for each objective/sub-objective (If data for some sections has not been entered, indicate that information is not found)
    def get_results_by_semester(self, semester, program_id):
        [results, string] = self.query(select(ProgramCourses).where(ProgramCourses.program_id == program_id))
        return string

    # List all of the evaluation results for each objective/sub-objective
    # Show course/section involved in evaluation, list result for each course/section, and aggregate the result to show the number (and percentage) of student
    def get_results_by_year(self, year):
        print("hey")