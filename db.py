from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    create_engine,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    code = Column(String(4), unique=True)
    faculty = relationship("Faculty", backref="department")
    programs = relationship("Program", backref="department")


class Faculty(Base):
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    rank = Column(String(50))
    department_code = Column(String(4), ForeignKey("departments.code"))


class Program(Base):
    __tablename__ = "programs"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    department_code = Column(String(4), ForeignKey("departments.code"))
    in_charge_id = Column(Integer, ForeignKey("faculty.id"))
    courses = relationship("Course", secondary="program_courses")


class Course(Base):
    __tablename__ = "courses"
    id = Column(String(10), primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    department_code = Column(String(4), ForeignKey("departments.code"))
    sections = relationship("Section", backref="course")


class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    semester = Column(String(20))
    year = Column(Integer)
    course_id = Column(String(10), ForeignKey("courses.id"))
    instructor_id = Column(Integer, ForeignKey("faculty.id"))
    enrollment_count = Column(Integer)


class LearningObjective(Base):
    __tablename__ = "learning_objectives"
    id = Column(String(50), primary_key=True)
    description = Column(Text)
    parent_id = Column(String(50), ForeignKey("learning_objectives.id"))
    sub_objectives = relationship("LearningObjective")


class ProgramCourses(Base):
    __tablename__ = "program_courses"
    program_id = Column(Integer, ForeignKey("programs.id"), primary_key=True)
    course_id = Column(String(10), ForeignKey("courses.id"), primary_key=True)


class CourseObjectives(Base):
    __tablename__ = "course_objectives"
    course_id = Column(String(10), ForeignKey("courses.id"), primary_key=True)
    objective_id = Column(
        String(50), ForeignKey("learning_objectives.id"), primary_key=True
    )
    program_id = Column(Integer, ForeignKey("programs.id"), primary_key=True)


class SectionEvaluations(Base):
    __tablename__ = "section_evaluations"
    section_id = Column(Integer, ForeignKey("sections.id"), primary_key=True)
    objective_id = Column(String(50), ForeignKey("learning_objectives.id"), primary_key=True)
    evaluation_method = Column(String(255), primary_key=True)
    students_met = Column(Integer)


class SessionManager:
    def __init__(self, database_uri):
        self.engine = create_engine(database_uri)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add(self, entry):
        try:
            self.session.add(entry)
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def add_department(self, name, code):
        new_department = Department(name=name, code=code)
        self.add(new_department)

    def add_faculty(self, name, email, rank, department_code):
        new_faculty = Faculty(
            name=name, email=email, rank=rank, department_code=department_code
        )
        self.add(new_faculty)

    def add_program(self, name, department_code, in_charge_id):
        new_program = Program(
            name=name, department_code=department_code, in_charge_id=in_charge_id
        )
        self.add(new_program)

    def add_course(self, id, title, description, department_code):
        new_course = Course(
            id=id, title=title, description=description, department_code=department_code
        )
        self.add(new_course)

    def add_section(
        self, number, semester, year, course_id, instructor_id, enrollment_count
    ):
        new_section = Section(
            number=number,
            semester=semester,
            year=year,
            course_id=course_id,
            instructor_id=instructor_id,
            enrollment_count=enrollment_count,
        )
        self.add(new_section)

    def add_learning_objective(self, id, description, parent_id=None):
        new_objective = LearningObjective(
            id=id, description=description, parent_id=parent_id
        )
        self.add(new_objective)

    def assign_course_to_program(self, program_id, course_id):
        new_assignment = ProgramCourses(program_id=program_id, course_id=course_id)
        self.add(new_assignment)

    def assign_objective_to_course(self, course_id, objective_id, program_id):
        new_assignment = CourseObjectives(
            course_id=course_id, objective_id=objective_id, program_id=program_id
        )
        self.add(new_assignment)

    def add_section_evaluation(
        self, section_id, objective_id, evaluation_method, students_met
    ):
        new_evaluation = SectionEvaluations(
            section_id=section_id,
            objective_id=objective_id,
            evaluation_method=evaluation_method,
            students_met=students_met,
        )
        self.add(new_evaluation)

    def query(self, query):
        return [[attr for attr in row] for row in self.session.execute(text(query))]

    # List all of its programs
    def get_department_programs_by_name(self, department_name):
        return self.query(
            f"SELECT p.name "
            f"FROM departments AS d "
            f"JOIN programs AS p "
            f"ON d.code = p.department_code "
            f"WHERE d.name= '{department_name}'"
        )

    # List all of its faculty (including what program each faculty is in charge of, if there is one)
    def get_department_faculty_by_name(self, department_name):
        return self.query(
            f"SELECT f.name, p.name "
            f"FROM departments AS d "
            f"JOIN faculty AS f "
            f"ON d.code = f.department_code "
            f"LEFT JOIN programs AS p "
            f"ON f.id = p.in_charge_id "
            f"WHERE d.name = '{department_name}'"
        )

    # List all the courses, together with the objectives/sub-objectives association with year

    def get_program_courses_by_name(self, program_name):
        return self.query(
            f"SELECT c.title, lo.description "
            f"FROM courses AS c "
            f"JOIN program_courses AS pc "
            f"ON c.id = pc.course_id "
            f"JOIN programs AS p "
            f"ON p.id = pc.program_id "
            f"LEFT JOIN course_objectives AS co "
            f"ON co.course_id = c.id "
            f"LEFT JOIN learning_objectives AS lo "
            f"ON co.objective_id = lo.id "
            f"WHERE p.name = '{program_name}'"
        )

    # List all of the objectives
    def get_program_objectives_by_name(self, program_name):
        return self.query(
            f"SELECT DISTINCT lo.description "
            f"FROM courses AS c "
            f"JOIN program_courses AS pc "
            f"ON c.id = pc.course_id "
            f"JOIN programs AS p "
            f"ON p.id = pc.program_id "
            f"JOIN course_objectives AS co "
            f"ON co.course_id = c.id "
            f"JOIN learning_objectives AS lo "
            f"ON co.objective_id = lo.id "
            f"WHERE p.name = '{program_name}'"
        )

    # List all of the evaluation results for each objective/sub-objective (If data for some sections has not been entered, indicate that information is not found)
    def get_results_by_semester(self, semester, program_name):
        semester = semester.split(" ")
        return self.query(
            f"SELECT c.title, s.number, se.evaluation_method, se.students_met "
            f"FROM courses AS c "
            f"JOIN sections AS s "
            f"ON c.id = s.course_id "
            f"JOIN program_courses AS pc "
            f"ON c.id = pc.course_id "
            f"JOIN programs AS p "
            f"ON p.id = pc.program_id "
            f"LEFT OUTER JOIN section_evaluations AS se "
            f"ON s.id = se.section_id "
            f"WHERE s.semester = '{semester[0]}' "  # semester[0] will contain "Fall" "Spring" etc
            f"AND s.year = {semester[1]} "  # semester[1] will contain year (i.e. 23, 24, etc.)
            f"AND p.name = '{program_name}'"
        )

    # List all of the evaluation results for each objective/sub-objective
    # Show course/section involved in evaluation, list result for each course/section, and aggregate the result to show the number (and percentage) of student
    def get_results_by_year(self, year):
        year = year.split("-")
        return self.query(
            f"SELECT lo.description, c.title, s.number, se.evaluation_method, se.students_met, ROUND(se.students_met * 100.0/s.enrollment_count) AS percent "
            f"FROM courses AS c "
            f"JOIN sections AS s "
            f"ON c.id = s.course_id "
            f"JOIN course_objectives AS co "
            f"ON c.id = co.course_id "
            f"JOIN learning_objectives AS lo "
            f"ON co.objective_id = lo.id "
            f"JOIN section_evaluations AS se "
            f"ON s.id = se.section_id AND lo.id = se.objective_id "
            f"WHERE (s.year = {year[0]} "
            f"AND s.semester = 'Summer') "
            f"OR (s.year = {year[0]} "
            f"AND s.semester = 'Fall') "
            f"OR (s.year = {year[1]} "
            f"AND s.semester = 'Spring') "
            f"GROUP BY lo.id, c.id, s.id, se.evaluation_method "
            f"ORDER BY c.id, s.id"
        )
