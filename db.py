from sqlalchemy import Column, Integer, String, ForeignKey, Text, create_engine, select, inspect, text
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

    def query(self, query):
        return [[attr for attr in row] for row in self.session.execute(text(query))]
    
    # List all of its programs
    def get_department_programs_by_id(self, department_id):
        return self.query(f"SELECT p.name FROM departments AS d JOIN programs AS p ON d.id = p.department_id WHERE d.id = {department_id}")
    def get_department_programs_by_name(self, department_name):
        return self.query(f"SELECT p.name FROM departments AS d JOIN programs AS p ON d.id = p.department_id WHERE d.name = '{department_name}'")

    # List all of its faculty (including what program each faculty is in charge of, if there is one)
    def get_department_faculty_by_id(self, department_id):
        return self.query(f"SELECT f.name, p.name FROM departments AS d JOIN faculty AS f ON d.id = f.department_id LEFT JOIN programs AS p ON f.id = p.in_charge_id WHERE d.id = {department_id}")
    def get_department_faculty_by_name(self, department_name):
        return self.query(f"SELECT f.name, p.name FROM departments AS d JOIN faculty AS f ON d.id = f.department_id LEFT JOIN programs AS p ON f.id = p.in_charge_id WHERE d.name = '{department_name}'")

    # List all the courses, together with the objectives/sub-objectives association with year
    def get_program_courses_by_id(self, program_id):
        return self.query(f"SELECT c.name, lo1.description, lo2.description FROM programs AS p JOIN program_courses AS pc ON p.id = pc.program_id JOIN courses AS c ON pc.course_id = c.id JOIN course_objectives AS co ON c.id = co.course_id JOIN learning_objectives AS lo1 ON co.objective_id = lo1.id JOIN learning_objectives AS lo2 ON lo2.parent_id = lo1.id WHERE p.id = {program_id}")
    def get_program_courses_by_name(self, program_name):
        return self.query(f"SELECT c.name, lo1.description, lo2.description FROM programs AS p JOIN program_courses AS pc ON p.id = pc.program_id JOIN courses AS c ON pc.course_id = c.id JOIN course_objectives AS co ON c.id = co.course_id JOIN learning_objectives AS lo1 ON co.objective_id = lo1.id JOIN learning_objectives AS lo2 ON lo2.parent_id = lo1.id WHERE p.name = '{program_name}'")
    
    # List all of the objectives
    def get_program_objectives_by_id(self, program_id):
        return self.query(f"SELECT DISTINCT lo.description FROM programs AS p JOIN program_courses AS pc ON p.id = pc.program_id JOIN courses AS c ON pc.course_id = c.id JOIN course_objectives AS co ON c.id = co.course_id JOIN learning_objectives AS lo ON co.objective_id = lo.id WHERE p.id = {program_id}")
    def get_program_objectives_by_name(self, program_name):
        return self.query(f"SELECT DISTINCT lo.description FROM programs AS p JOIN program_courses AS pc ON p.id = pc.program_id JOIN courses AS c ON pc.course_id = c.id JOIN course_objectives AS co ON c.id = co.course_id JOIN learning_objectives AS lo ON co.objective_id = lo.id WHERE p.name = '{program_name}'")

    # List all of the evaluation results for each objective/sub-objective (If data for some sections has not been entered, indicate that information is not found)
    def get_results_by_semester(self, semester, program_id):
        return self.query(f"SELECT s.name, s.enrollment_count, se.evaluation_method, se.students_met FROM programs AS p JOIN program_courses AS pc ON p.id = pc.program_id JOIN courses AS c ON pc.course_id = c.id JOIN sections AS s ON c.id = s.course_id LEFT JOIN section_evaluations AS se ON s.id = se.section_id WHERE s.semester = '{semester}' AND p.program_id = {program_id}")

    # List all of the evaluation results for each objective/sub-objective
    # Show course/section involved in evaluation, list result for each course/section, and aggregate the result to show the number (and percentage) of student
    def get_results_by_year(self, year):
        return self.query(f"SELECT * FROM course_objectives")