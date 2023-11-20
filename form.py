from flask_wtf import FlaskForm
from wtforms import (
                    StringField, SubmitField,
                    SelectField, DateField, FloatField
                    )
from wtforms.validators import DataRequired
from datafield import *


class AssetForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    a_type = SelectField(
        "AcquisitionType", choices=[x for x in a_choices.values()],
        validators=[DataRequired()]
        )
    d_type = SelectField( 
        "DeviceType", choices=[x for x in d_choices.values()],
        validators=[DataRequired()]
        )
    a_loca = SelectField(
        "AcquisitionLocation", choices=[x for x in a_loca.values()],
        validators=[DataRequired()]
        )
    manufac = SelectField(
        "Manufacturer", choices=[x for x in m_choices.values()],
        validators=[DataRequired()]
        )
    sn = StringField(
        "SN", validators=[DataRequired()]
        )
    user = StringField(
        "UserID", validators=[DataRequired()]
        )
    c_loca = SelectField(
        "CurrentLocation", choices=[x for x in c_loca.values()],
        validators=[DataRequired()]
        )
    a_value = FloatField(
        "AcquisitionValue(CAD)", validators=[DataRequired()]
        )
    a_tax = FloatField(
        "Tax(CAD)", validators=[DataRequired()]
        )
    com1 = StringField(
        "Com1"
        )
    com2 = StringField(
        "Com2"
        )
    status = SelectField(
        "Status(1=Normal, 0=Obnormal)", choices=[0,1],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    a_code= StringField(
        "AssetCode", validators=[DataRequired()]
        )
    date = DateField('Date', validators=[DataRequired()])
    a_type = SelectField(
        "AcquisitionType", choices=[x for x in a_choices.values()],
        validators=[DataRequired()]
        )
    d_type = SelectField( 
        "DeviceType", choices=[x for x in d_choices.values()],
        validators=[DataRequired()]
        )
    a_loca = SelectField(
        "AcquisitionLocation", choices=[x for x in a_loca.values()],
        validators=[DataRequired()]
        )
    manufac = SelectField(
        "Manufacturer", choices=[x for x in m_choices.values()],
        validators=[DataRequired()]
        )
    sn = StringField(
        "SN", validators=[DataRequired()]
        )
    user = StringField(
        "UserID", validators=[DataRequired()]
        )
    c_loca = SelectField(
        "CurrentLocation", choices=[x for x in c_loca.values()],
        validators=[DataRequired()]
        )
    a_value = FloatField(
        "AcquisitionValue(CAD)", validators=[DataRequired()]
        )
    a_tax = FloatField(
        "Tax(CAD)", validators=[DataRequired()]
        )
    com1 = StringField(
        "Com1"
        )
    com2 = StringField(
        "Com2"
        )
    status = SelectField(
        "Status(1=Normal, 0=Obnormal)", choices=[0,1],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')