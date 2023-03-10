from quopri import decodestring
from copy import deepcopy
from sqlite3 import connect
from .behavior_patterns import FileWriter, Subject 
from .archi_system_unit_of_work import DomainObject

#абстрактный пользователь
class User:

    def __init__(self, name):
        self.name = name

# преподаватель
class Teacher(User, DomainObject):
    
    def __init__(self, name):
        self.ratings = []
        super().__init__(name)

# администратор
class Admin(User):
    pass

# студент
class Student(User):
    pass


class UserFactory:
    types = {
        'admin': Admin,
        'teacher': Teacher,
        'student': Student,
    }

    # порождающий паттерн фабричный метод
    @classmethod
    def create(cls, user_type, name):
        return cls.types[user_type](name)

# порождающий паттерн Прототип
class TeacherRatingPrototype:
    # прототип рейтинга преподавателя

    def clone(self):
        return deepcopy(self)

class TeacherRating(TeacherRatingPrototype, Subject):

    def __init__(self, month, teacher, score):
        self.teacher = teacher
        self.score = score
        self.month = month
        self.teachers = []
        super().__init__()

    def __getitem__(self, item):
        return self.teachers[item]

    def add_teacher(self, teacher: Teacher):
        self.teachers.append(teacher)
        teacher.ratings.append(self)
        self.notify()

class SeptemberTeacherRating(TeacherRating):
    pass

class OctoberTeacherRating(TeacherRating):
    pass

class NovemberTeacherRating(TeacherRating):
    pass

class DecemberTeacherRating(TeacherRating):
    pass

class JanuaryTeacherRating(TeacherRating):
    pass

class FabruaryTeacherRating(TeacherRating):
    pass

class MarchTeacherRating(TeacherRating):
    pass

class AprilTeacherRating(TeacherRating):
    pass

class MayTeacherRating(TeacherRating):
    pass

class TeacherRatingFactory:
    month = {
        'september': SeptemberTeacherRating,
        'october': OctoberTeacherRating,
        'november': NovemberTeacherRating,
        'december': DecemberTeacherRating,
        'january': JanuaryTeacherRating,
        'fabruary': FabruaryTeacherRating,
        'march': MarchTeacherRating,
        'april': AprilTeacherRating,
        'may': MayTeacherRating,
    }

    @classmethod
    def create(cls, month, teacher, score):
        return cls.month[month](month, teacher, score)

class Month:

    def __init__(self, name, month):
        self.name = name
        self.month = month
        self.teachers = []

class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.ratings = []

    @staticmethod
    def create_user(user_type, name):
        return UserFactory.create(user_type, name)

    @staticmethod
    def create_rating(month, teacher, score):
        return TeacherRatingFactory.create(month, teacher, score)

    def get_rating_by_month(self, month):
        for rate in self.ratings:
            if rate.month == month:
                return rate

    def get_teacher(self, name) -> Teacher:
        for item in self.teachers:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')

# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        print('log--->', text)
        self.writer.write(text)

class TeacherMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'teachers'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            teacher = Teacher(name)
            teacher.id = id
            result.append(teacher)
        return result


    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Teacher(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'teachers': TeacherMapper,
        #'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Teacher):

            return TeacherMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')

