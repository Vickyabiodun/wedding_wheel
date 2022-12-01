from email import message
from tkinter import Button
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField,IntegerField,FileField,EmailField,DateField,PasswordField
from wtforms.validators import DataRequired,Length
from flask_wtf.file import FileAllowed

class newlisting(FlaskForm):
    title = StringField(validators=[DataRequired(message='Your listing cannot be without a title'), Length(min=10,message='The listing title cannot be less than 10')])
    capacity = IntegerField(validators=[DataRequired(message='Your Capacity cannot be empty')])
    price = IntegerField(validators=[DataRequired(message='Your listing enter the price')])
    address = StringField(validators=[DataRequired(message='Please enter address')])
    postcode = StringField()
    description = TextAreaField(validators=[DataRequired(message='Please input your description'), Length(min=200,message='The description cannot be less than 200 words' )])
    gallery_of_venue = FileField(validators=[DataRequired(message='You can only upload jpg or png'), FileAllowed('jpg','png')])
    video = StringField(validators=[DataRequired(message='Please input the link to your video')])
    facebook = StringField(validators=[DataRequired(message='Please input the link to your social media')])
    twitter = StringField(validators=[DataRequired(message='Please input the link to your social media')])
    instagram = StringField(validators=[DataRequired(message='Please input the link to your social media')])
    youtube = StringField(validators=[DataRequired(message='Please input the link to your social media')])
    submit = SubmitField()

class RequestForm(FlaskForm):
    name = StringField(validators=[DataRequired(message='Please enter your name')])
    email = EmailField(validators=[DataRequired(message='Please enter your email address')])
    phone = IntegerField(validators=[DataRequired(message='Email cannot be empty'), Length(min=11,message='Phone number must be at least 11')])
    wedding_date = DateField(validators=[DataRequired(message='Date cannot be empty')])
    message = TextAreaField(validators=[DataRequired(message='Please add a short message'), Length(min=80,message='The description cannot be less than 80 words' )])
    submit = SubmitField()

class Couple_profile(FlaskForm):
    name = StringField(' Name')
    couple_location = StringField('Location',validators=[DataRequired(message='Please enter your location')])
    couple_img = FileField('Upload Profile Picture',validators=[DataRequired(message='You can only upload jpg or png'), FileAllowed('jpg','png')])
    email = EmailField('Email Address')
    phone = IntegerField('Phone',validators=[DataRequired(message='Email cannot be empty'), Length(min=11,message='Phone number must be at least 11')])
    submit = SubmitField('Update Profile')

class Change_password(FlaskForm):
    current_pass = PasswordField('Current Password',validators=[DataRequired(message='Old password cannot be empty')])
    new_pass =PasswordField('New Password',validators=[DataRequired(message='New password cannot be empty')])
    confirm_pass =PasswordField('Confirm Password',validators=[DataRequired(message='Please confirm password')])
    submit = SubmitField('Save Change')

class ReviewForm(FlaskForm):
    thereview = TextAreaField('Write Your Review',validators=[DataRequired(message='Please add a comment to submit')])
    rname = StringField('Name',validators=[DataRequired(message='Name cannot be empty')])
    remail = EmailField('Email Address',validators=[DataRequired(message='Email cannot be empty')])

class To_do(FlaskForm):
    task = StringField('Task Title',validators=[DataRequired(message='Task cannot be empty')])
    task_date = DateField('Task Date',validators=[DataRequired(message='Date cannot be empty')])
    submit = SubmitField('Submit To Do')

class Guest_list(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired(message='First Name cannot be empty')])
    last_name = StringField('Last Name',validators=[DataRequired(message='Last Name cannot be empty')])
    address_one = StringField('Address Line 1',validators=[DataRequired(message='Address cannot be empty')])
    address_two = StringField('Address Line 2')
    email = EmailField('Email',validators=[DataRequired(message='Email cannot be empty')])
    city = StringField('City')
    country = StringField('Country')
    post_code = IntegerField('Postal Code')
    submit = SubmitField('Save Guest Details')

class Vendor_profile(FlaskForm):
    name = StringField(' Name')
    vend_location = StringField('Location',validators=[DataRequired(message='Please enter your location')])
    vend_img = FileField('Upload Profile Picture',validators=[DataRequired(message='You can only upload jpg or png'), FileAllowed('jpg','png')])
    email = EmailField('Email Address')
    vend_specialty=StringField('Specialty')
    phone = IntegerField('Phone',validators=[DataRequired(message='Email cannot be empty'), Length(min=11,message='Phone number must be at least 11')])
    vend_instagram = StringField('Instagram',validators=[DataRequired(message='Social Media link cannot be empty')])
    vend_twitter = StringField('Twitter',validators=[DataRequired(message='Social Media link cannot be empty')])
    vend_website = StringField('Website')
    vend_other_links = StringField('Other Links')
    submit = SubmitField('Update Profile')

class Real_wedding(FlaskForm):
    featured_image = FileField('Upload Featured Image',validators=[DataRequired(message='Upload Image')])
    featured_story = TextAreaField('Write about your wedding journey.',validators=[DataRequired(message='Write about your wedding journey')])
    add_vendor = StringField('Add your vendor.',validators=[DataRequired(message='Add yoiur vendor')])
    add_vendor2 = StringField('Add your vendor.')
    vend_cat = StringField('Select Vendor Category')
    submit = SubmitField('Submit Real Wedding')

