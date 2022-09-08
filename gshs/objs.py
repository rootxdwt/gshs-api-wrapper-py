from bs4 import BeautifulSoup

baseURL = "https://student.gs.hs.kr/student"


class User:
    def __init__(self, id: str, name: str, phone: str) -> None:
        self.id = id
        self.name = name
        self.phone = phone

    def __repr__(self):
        return f'User({self.id}, {self.name}, {self.phone})'


class Student(User):
    def __init__(self, id, name, phone, year, _class):
        super().__init__(id, name, phone)
        self.year = year
        self._class = _class

    def __repr__(self):
        return f'Student({self.id}, {self.name}, {self.phone}, class: {self.year}-{self._class})'


class Teacher(User):
    def __init__(self, id, name, phone):
        super().__init__(id, name, phone)

    def __repr__(self):
        return f'Teacher({self.id}, {self.name}, {self.phone})'


class WritingAuthor:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return f'WritingAuthor({self.name}, {self.type})'


class Writing:
    def __init__(self, author, title: str, date: str, id: str) -> None:
        self.author = author
        self.title = title
        self.date = date
        self.id = id

    def __repr__(self):
        return f'Writing({self.author}, {self.title}, {self.date}, {self.id})'


class LostWriting(Writing):
    def __init__(self, id: str, title: str, author, date: str, _type: str) -> None:
        super().__init__(author, title, date, id)
        self.type = _type

    def __repr__(self):
        return f'Writing({self.author}, {self.title}, {self.date}, {self.id}, {self.type})'
