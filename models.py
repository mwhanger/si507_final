#Separate models file to facilitate DB Loading
from flask_sqlalchemy import SQLAlchemy

#https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/
db = SQLAlchemy()

#Many to many models and association tables
states = db.Table('states',
    db.Column('state_id', db.Integer, db.ForeignKey('state.id'), primary_key=True),
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'), primary_key=True)
    )

places = db.Table('places',
    db.Column('place_id', db.Integer, db.ForeignKey('place.id'), primary_key=True),
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'), primary_key=True)
    )

publishers = db.Table('publishers',
    db.Column('publisher_id', db.Integer, db.ForeignKey('publisher.id'), primary_key=True),
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'), primary_key=True)
    )

frequencies = db.Table('frequencies',
    db.Column('frequency_id', db.Integer, db.ForeignKey('frequency.id'), primary_key=True),
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'), primary_key=True)
    )

languages = db.Table('languages',
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), primary_key=True),
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'), primary_key=True)
    )

subjects = db.Table('subjects',
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True),
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'), primary_key=True)
    )

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    place_of_publication = db.Column(db.String)
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    notes = db.Column(db.String)
    alt_titles = db.Column(db.String)
    lccn = db.Column(db.String,unique=True)
    #potential many-to-many foreign keys
    states = db.relationship('State', secondary=states, backref=db.backref('papers',lazy='dynamic'),lazy='dynamic')
    place = db.relationship('Place', secondary=places, backref=db.backref('papers',lazy='dynamic'),lazy='dynamic')
    publisher = db.relationship('Publisher', secondary=publishers, backref=db.backref('papers',lazy='dynamic'),lazy='dynamic')
    frequency = db.relationship('Frequency', secondary=frequencies, backref=db.backref('papers',lazy='dynamic'),lazy='dynamic')
    language = db.relationship('Language', secondary=languages, backref=db.backref('papers',lazy='dynamic'),lazy='dynamic')
    subject = db.relationship('Subject', secondary=subjects, backref=db.backref('papers',lazy='dynamic'),lazy='dynamic')

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,unique=True)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String,unique=True)

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

class Frequency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String,unique=True)

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String, unique=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, unique=True)
