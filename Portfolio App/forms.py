from flask_wtf import FlaskForm
from wtforms import SubmitField

class PhysicsButton(FlaskForm):
    phy = SubmitField('Physics')

class ProgrammingButton(FlaskForm):
    pro = SubmitField('Programming')
