from sqlalchemy import Column, Integer, String, ForeignKey, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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
