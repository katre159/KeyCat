import numpy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey,  LargeBinary


Base = declarative_base()


class Button(Base):
    __tablename__ = 'button'

    id = Column(Integer, primary_key=True)
    templates = relationship("Template", back_populates="button")
    shortcuts = relationship("Shortcut", back_populates="button")
    program = Column(String)

    def __init__(self, program, templates, shortcuts):
        self.templates = templates
        self.shortcuts = shortcuts
        self.program = program

    def __eq__(self, other):
        return self.program == other.program and self.templates == other.templates and self.shortcuts == other.shortcuts

    def __repr__(self):
        return self.program + " " + str(self.shortcuts) + " " + str(self.templates)


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

    def __init__(self, keycodes):
        self.keycodes = keycodes

    def __eq__(self, other):
        return self.keycodes == other.keycodes

    def __repr__(self):
        return self.keycodes



