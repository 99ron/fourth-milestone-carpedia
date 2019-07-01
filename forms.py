from flask_wtf import FlaskForm, CsrfProtect
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, IntegerField, validators, TextAreaField, FileField
from wtforms.validators import DataRequired, NumberRange, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Enter your Username', validators=[DataRequired])
    password = PasswordField('Enter your Password', validators=[DataRequired])
    submit = SubmitField('Login')
    
class RegisterForm(FlaskForm):
    username = StringField('Enter desired username', validators=[DataRequired])
    password = PasswordField('Enter a password', validators=[DataRequired])
    submit = SubmitField('Register')

class CarToDatabase(FlaskForm):
    region = SelectField('Select Region', choices=[('', 'Please select a region'), ('JDM', 'Japanese'),('USDM', 'USA'),('Euro', 'Europe')], default='', validators=[InputRequired])
    make = SelectField('Select Make', choices=[('', 'Please select a make'), ('Aston Martin', 'Aston Martin'), ('Audi', 'Audi'), ('BMW', 'BMW'), ('Corvette', 'Corvette'), ('Chevrolet', 'Chevrolet'),
                       ('Ferrari', 'Ferrari'), ('Ford', 'Ford'), ('Honda', 'Honda'), ('Jaguar', 'Jaguar'), ('Lamborghini', 'Lamborghini'), ('Mercedez', 'Mercedez'),
                       ('Nissan', 'Nissan'), ('Renault', 'Renault'), ('Toyota', 'Toyota'), ('Rolls Royce', 'Rolls Royce'), ('VW', 'VW')], default='', validators=[DataRequired])
    model = StringField('Enter the model', validators=[DataRequired])
    car_img = FileField()
    trans = SelectField('Transmission Type', choices=[('Manual', 'Manual'), ('Semi-Auto', 'Semi-Auto'), ('Auto', 'Automatic'), ('Sequential', 'Sequential')], validators=[DataRequired])
    drive = SelectField('Select Drivetrain', choices=[('FWD', 'FWD'), ('RWD', 'RWD'), ('AWD', 'AWD'), ('4WD','4WD')], validators=[DataRequired])
    body = SelectField('Select Body Type', choices=[('Hatchback', 'Hatchback'), ('SUV', 'SUV'), ('Coupe', 'Coupe'), ('Saloon', 'Saloon'), ('Jeep', 'Jeep'),
                        ('Convertible', 'Convertible'), ('Crossover', 'Crossover')], validators=[DataRequired])
    year = IntegerField('Type in Year (Between 1960 and 2019)', validators=[NumberRange(min=1960, max=2019), DataRequired])
    hp = IntegerField('Horsepower', validators=[DataRequired])
    torque = IntegerField('Torque', validators=[DataRequired])
    accel = FloatField('0-60 Time', validators=[DataRequired])
    submit = SubmitField('Add Vehicle!')

class FilterCars(FlaskForm):
    region = SelectField('Select Region', choices=[('All' , 'All'), ('JDM', 'Japanese'),('USDM', 'USA'),('Euro', 'Europe')], default='All')
    drive = SelectField('Select Drivetrain', choices=[('All', 'All'), ('FWD', 'FWD'), ('RWD', 'RWD'), ('AWD', 'AWD'), ('4WD','4WD')], default='All')
    query = SelectField('Select Filter', choices=[('Brands', 'Brands  (A-Z)'),('BrandsOpp', 'Brands (Z-A)') ,('Likes', 'Liked'), ('BHP', 'Horsepower (High - Low)'), ('BHPOpp', 'Horsepower (Low - High)')])
    submit = SubmitField('Search Database') 

class EditCar(FlaskForm):
    region = SelectField('Select Region', choices=[('JDM', 'Japanese'),('USDM', 'USA'),('Euro', 'Europe')], default='', validators=[InputRequired])
    make = SelectField('Select Make', choices=[('Aston Martin', 'Aston Martin'), ('Audi', 'Audi'), ('BMW', 'BMW'), ('Corvette', 'Corvette'), ('Chevrolet', 'Chevrolet'),
                       ('Ferrari', 'Ferrari'), ('Ford', 'Ford'), ('Honda', 'Honda'), ('Jaguar', 'Jaguar'), ('Lamborghini', 'Lamborghini'), ('Mercedez', 'Mercedez'),
                       ('Nissan', 'Nissan'), ('Renault', 'Renault'), ('Toyota', 'Toyota'), ('Rolls Royce', 'Rolls Royce'), ('VW', 'VW')], default='', validators=[DataRequired])
    model = StringField('Enter the model', validators=[DataRequired])
    car_img = FileField()
    trans = SelectField('Transmission Type', choices=[('Manual', 'Manual'), ('Semi-Auto', 'Semi-Auto'), ('Auto', 'Automatic'), ('Sequential', 'Sequential')], validators=[DataRequired])
    drive = SelectField('Select Drivetrain', choices=[('FWD', 'FWD'), ('RWD', 'RWD'), ('AWD', 'AWD'), ('4WD','4WD')], validators=[DataRequired])
    body = SelectField('Select Body Type', choices=[('Hatchback', 'Hatchback'), ('SUV', 'SUV'), ('Coupe', 'Coupe'), ('Saloon', 'Saloon'), ('Jeep', 'Jeep'),
                        ('Convertible', 'Convertible'), ('Crossover', 'Crossover')], validators=[DataRequired])
    car_desc = TextAreaField('Enter a description', validators=[DataRequired])
    year = IntegerField('Type in Year (Between 1960 and 2019)', validators=[NumberRange(min=1960, max=2019), DataRequired])
    hp = IntegerField('Horsepower', validators=[DataRequired])
    torque = IntegerField('Torque', validators=[DataRequired])
    accel = FloatField('0-60 Time', validators=[DataRequired])
