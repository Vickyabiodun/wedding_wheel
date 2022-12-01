import datetime

from sqlalchemy import false
from pkg import db


class Location(db.Model): 
    __tablename___='tbl_state'
    location_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    location_name = db.Column(db.String(255), nullable=False)

class Services(db.Model): 
    service_id = db.Column(db.Integer(),primary_key=True, nullable=False)
    service_name = db.Column(db.Float(), nullable=False)

class VendorServices(db.Model):
    vendor_id = db.Column(db.Integer(),db.ForeignKey('vendor.vendor_id'), nullable=True)
    service_id = db.Column(db.Integer(),db.ForeignKey('services.service_id'), nullable=True)
    vendorservices_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)

class Couple(db.Model): 
    couple_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    couple_email = db.Column(db.String(255), nullable=False)
    couple_pass = db.Column(db.String(255), nullable=False)
    couple_name = db.Column(db.String(255), nullable=False)
    couple_location = db.Column(db.Integer(),db.ForeignKey('location.location_id'), nullable=True)
    couple_phone = db.Column(db.String(100), nullable=True)
    couple_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    couple_image = db.Column(db.String(255), nullable=True)
    mystate = db.relationship('Location',backref='couples')

class Vendor(db.Model): 
    vendor_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    vendor_email = db.Column(db.String(255), nullable=False)
    vendor_pass = db.Column(db.String(255), nullable=False)
    vendor_name = db.Column(db.String(255), nullable=False)
    vendor_business_name = db.Column(db.String(255), nullable=False)
    vendor_specialty = db.Column(db.String(255), nullable=True)
    vendor_twitter = db.Column(db.String(255), nullable=True)
    vendor_ig = db.Column(db.String(255), nullable=True)
    vendor_website = db.Column(db.String(255), nullable=True)
    vendor_other_links = db.Column(db.String(255), nullable=True)

    vendor_location = db.Column(db.Integer(),db.ForeignKey('location.location_id'), nullable=True)
    vendor_phone = db.Column(db.String(100), nullable=True)
    vendor_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    vendor_image = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum('Approved','Not Approved','Suspended'), nullable=False)

    vendorloc = db.relationship('Location',backref='vendors')

class Admin(db.Model): 
    admin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_username = db.Column(db.String(255), nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)
    admin_lastlogin = db.Column(db.DateTime(), onupdate=datetime.datetime.utcnow)


class Category(db.Model): 
    cat_id = db.Column(db.Integer(),primary_key=True, nullable=False)
    cat_name = db.Column(db.String(255), nullable=False)


class Budget(db.Model): 
    budget_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    wedding_event = db.Column(db.String(255), nullable=False)
    estimate = db.Column(db.Integer(), nullable=False)
    actual = db.Column(db.Integer(), nullable=False)
    paid = db.Column(db.Integer(), nullable=False)
    pending = db.Column(db.Integer(), nullable=True)
    cat_budget_id = db.Column(db.Integer(),db.ForeignKey('category.cat_id'), nullable=True)
    couple_budget_id = db.Column(db.Integer(),db.ForeignKey('couple.couple_id'), nullable=True)
    couplebudget = db.relationship('Couple',backref='couplebud')
    couplecat = db.relationship('Category',backref='couplecat')
    
class State(db.Model): 
    state_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    state_name = db.Column(db.String(255), nullable=False)

class Listing(db.Model): 
    listing_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    address= db.Column(db.String(255), nullable=False)
    vendor_state = db.Column(db.Integer(),db.ForeignKey('state.state_id'), nullable=False)
    vendor_category = db.Column(db.Integer(),db.ForeignKey('category.cat_id'), nullable=False)
    postcode= db.Column(db.String(255), nullable=False)
    description= db.Column(db.String(255), nullable=False)
    gallery_of_venue= db.Column(db.String(255), nullable=False)
    video= db.Column(db.String(255), nullable=False)
    facebook= db.Column(db.String(255), nullable=False)
    twitter= db.Column(db.String(255), nullable=False)
    instagram= db.Column(db.String(255), nullable=False)
    youtube= db.Column(db.String(255), nullable=False)
    vendor_listing_id = db.Column(db.Integer(),db.ForeignKey('vendor.vendor_id'), nullable=False)

    vendor_listing = db.relationship('Vendor',backref='listingvendor')
    vendorcategory = db.relationship('Category',backref='listingcat')
    vendorstate = db.relationship('State',backref='listingstate')


class Wishlist(db.Model):
    wish_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    wish_listing_id= db.Column(db.Integer(),db.ForeignKey('listing.listing_id'), nullable=True)
    couple_wish_id= db.Column(db.Integer(),db.ForeignKey('couple.couple_id'), nullable=False)

    wish_item = db.relationship('Listing',backref='wishes')
    thecoup = db.relationship('Couple',backref='coupwish')

class Quotes(db.Model):
    quote_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    couple_name = db.Column(db.String(255), nullable=False)
    couple_email = db.Column(db.String(255), nullable=False)
    couple_phone = db.Column(db.String(255), nullable=False)
    date_sent = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    couple_message =  db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer(),db.ForeignKey('couple.couple_id'), nullable=False)
    listeditem_id = db.Column(db.Integer(),db.ForeignKey('listing.listing_id'), nullable=False)

    couple_requesting = db.relationship('Couple',backref='couplerequesting')
    items = db.relationship('Listing',backref='itemquoted')

class Reviews(db.Model):
    review_id = db.Column(db.Integer(),primary_key=True, nullable=False)
    couple_name = db.Column(db.String(255), nullable=False)
    couple_email = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.String(1000), nullable=False)
    thecouple_id = db.Column(db.Integer(),db.ForeignKey('couple.couple_id'), nullable=False)
    thelisteditem_id = db.Column(db.Integer(),db.ForeignKey('listing.listing_id'), nullable=False)
    thelisting_vendor_id = db.Column(db.Integer(),db.ForeignKey('vendor.vendor_id'), nullable=False)

    couple_requesting = db.relationship('Couple',backref='couplecommenting')
    review_item = db.relationship('Listing',backref='reviewed_item')
    review_vendor= db.relationship('Vendor',backref='reviewed_vendor')

class Task(db.Model):
        task_id = db.Column(db.Integer(),primary_key=True, nullable=False)
        the_task= db.Column(db.String(255), nullable=False)

        task_date =db.Column(db.Date())
        c_id = db.Column(db.Integer(),db.ForeignKey('couple.couple_id'), nullable=False)
        status = db.Column(db.Enum('Completed','Not Completed','Due'),default='Not Completed', nullable=False)

        couple_tasking = db.relationship('Couple',backref='couplet')

class Myguest(db.Model):
        invite_id = db.Column(db.Integer(),primary_key=True, nullable=False)
        couple_adding_id = db.Column(db.Integer(),db.ForeignKey('couple.couple_id'), nullable=False)
        first_name= db.Column(db.String(255), nullable=False)
        last_name= db.Column(db.String(255), nullable=False)
        address_one= db.Column(db.String(255), nullable=False)
        address_two= db.Column(db.String(255), nullable=True)
        email= db.Column(db.String(255), nullable=False)
        relationship= db.Column(db.String(255), nullable=False)
        city= db.Column(db.String(255), nullable=True)
        country= db.Column(db.String(255), nullable=True)
        post_code= db.Column(db.String(255), nullable=True)
        rsvp_status = db.Column(db.Enum('Confirmed','Declined','No Response'),default='No Response', nullable=False)
        invite_status = db.Column(db.Enum('Sent','Not Sent'),default='Not Sent', nullable=False)                    

        couple_adding = db.relationship('Couple',backref='coupleguest')

class Wed_story(db.Model): 
    real_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    real_coupl_id = db.Column(db.Integer(),db.ForeignKey('couple.couple_id'), nullable=False)
    real_img = db.Column(db.String(255), nullable=False)
    real_vend_cat1 = db.Column(db.String(255), nullable=False)
    real_vend_cat2 =  db.Column(db.String(255), nullable=True)
    real_vend1 = db.Column(db.String(255), nullable=False)
    real_vend2 =  db.Column(db.String(255), nullable=True)
    wedding_story = db.Column(db.String(1000), nullable=True)

    couple_story = db.relationship('Couple',backref='storycouple')


