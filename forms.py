from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, FileField
from wtforms.validators import Length, EqualTo, DataRequired



class AddProduct(FlaskForm):
    name = StringField(label="name", validators=[Length(min=5), DataRequired()])
    file = FileField(label="file")
    price = IntegerField(label="price")
    password_hash = PasswordField(label="password")
    repeat_password = PasswordField(label="repeat password", validators=[Length(min=4), EqualTo("password_hash")])
    submit = SubmitField(label="submit")

    def __str__(self):
        return f"{self.name}"

class RegisterForm(FlaskForm):
    username = StringField(label="username")
    password = PasswordField(label="password")
    register = SubmitField(label="register")

class LoginForm(FlaskForm):
    username = StringField(label="username")
    password = PasswordField(label="password")
    login = SubmitField(label="login")