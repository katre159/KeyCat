import numpy
from key_codes import key_label_dictionary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey,  LargeBinary


Base = declarative_base()


class Button(Base):
    __tablename__ = 'button'

    id = Column(String, primary_key=True)
    templates = relationship("Template", back_populates="button", cascade="all, delete-orphan")
    shortcuts = relationship("Shortcut", back_populates="button", cascade="all, delete-orphan")
    program = Column(String)
    name = Column(String)

    def __init__(self, id, program, name, templates, shortcuts):
        self.id = id
        self.templates = templates
        self.shortcuts = shortcuts
        self.program = program
        self.name = name

    def __eq__(self, other):
        return self.id == other.id and self.program == other.program

    def __repr__(self):
        return self.id + " " + self.program + " " + str(self.shortcuts) + " " + str(self.templates)


class Template(Base):
    __tablename__ = 'template'

    id = Column(Integer, primary_key=True)
    template_string = Column(LargeBinary)
    width = Column(Integer)
    height = Column(Integer)
    button_id = Column(Integer, ForeignKey('button.id'))
    button = relationship("Button", back_populates="templates")

    def __init__(self, template_string, height, width):
        self.template_string = template_string
        self.width = width
        self.height = height

    def get_template_as_numpy_array(self):
        return numpy.reshape(numpy.fromstring(self.template_string, dtype=numpy.uint8), (self.height, self.width))

    def __eq__(self, other):
        return self.template_string == other.template_string and self.width == other.width \
               and self.height == other.height

    def __repr__(self):
        return str(self.width) + " " + str(self.height)


class Shortcut(Base):
    __tablename__ = 'shortcut'

    id = Column(Integer, primary_key=True)
    button_id = Column(Integer, ForeignKey('button.id'))
    button = relationship("Button", back_populates="shortcuts")
    keycodes = Column(String)

    def get_keycodes_in_readable_format(self):
        return "+".join(map(lambda x: key_label_dictionary[int(x)], self.keycodes.split(",")))

    def __init__(self, keycodes):
        self.keycodes = keycodes

    def __eq__(self, other):
        return self.keycodes == other.keycodes

    def __repr__(self):
        return self.keycodes


class ShortcutStat(Base):
    __tablename__ = 'shortcut_stat'

    id = Column(Integer, primary_key=True)
    shortcut_id = Column(Integer, ForeignKey('shortcut.id'))
    shortcut = relationship("Shortcut")
    hit_count = Column(Integer)

    def __init__(self, shortcut, hit_count):
        self.shortcut = shortcut
        self.hit_count = hit_count

    def __eq__(self, other):
        return self.shortcut == other.shortcut and self.hit_count == other.hit_count


class ButtonStat(Base):
    __tablename__ = 'button_stat'

    id = Column(Integer, primary_key=True)
    button_id = Column(Integer, ForeignKey('button.id'))
    button = relationship("Button")
    hit_count = Column(Integer)

    def __init__(self, button, hit_count):
        self.button = button
        self.hit_count = hit_count

    def __eq__(self, other):
        return self.button == other.button and self.hit_count == other.hit_count
