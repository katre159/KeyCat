import numpy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Unicode


Base = declarative_base()


class Button(Base):
    __tablename__ = 'button'

    id = Column(Integer, primary_key=True)
    templates = relationship("Template", back_populates="button")

    def __init__(self, templates):
        self.templates = templates


class Template(Base):
    __tablename__ = 'template'

    id = Column(Integer, primary_key=True)
    template_string = Column(String(convert_unicode=True))
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


class ProgramButton(object):
    def __init__(self, templates, key_codes):
        self.templates = templates
        self.key_codes = key_codes
