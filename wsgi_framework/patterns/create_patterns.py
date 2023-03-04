from quopri import decodestring
from copy import deepcopy

#абстрактный пользователь
class User:
    pass

# преподаватель
class Teacher(User):
    def __init__(self, name):
        self.name = name
    

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
    def create(cls, user_type):
        return cls.types[user_type]()

# порождающий паттерн Прототип
class TeacherRatingPrototype:
    # прототип рейтинга преподавателя

    def clone(self):
        return deepcopy(self)

class TeacherRating(TeacherRatingPrototype):

    def __init__(self, month, teacher, score):
        self.teacher = teacher
        self.score = score
        self.month = month

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
    def create_user(user_type):
        return UserFactory.create(user_type)

    @staticmethod
    def create_rating(month, teacher, score):
        return TeacherRatingFactory.create(month, teacher, score)

    def find_rating_by_month(self, month):
        result = []
        for rate in self.ratings:
            if rate.month == month:
                result.append(rate)
        return result

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

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
