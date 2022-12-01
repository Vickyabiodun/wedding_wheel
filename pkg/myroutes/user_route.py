
from crypt import methods
from email import message
from functools import cache
from select import select
from tkinter import W
from unicodedata import category
from flask import Flask, make_response,render_template,request,redirect,flash, url_for,session,jsonify
from sqlalchemy import all_
from flask_mail import Mail,Message
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app,db,mail
from pkg.mymodels import Admin, Category, Listing,Location,Couple, Myguest, Quotes,Vendor,State,Wishlist,Reviews,Task,Myguest,Wed_story
from pkg.myforms import newlisting,RequestForm,Couple_profile,Change_password,ReviewForm,To_do,Guest_list,Real_wedding,Vendor_profile
import os,random,string

##Homepage
@app.route('/home',methods =['POST','GET'])
def hompage():
    
    category = db.session.query(Category).all()
    state = db.session.query(State).all()
    firstrev =db.session.query(Reviews).filter(Reviews.review_id==20).first()
    secrev =db.session.query(Reviews).filter(Reviews.review_id==21).first()

    return render_template('home.html',category=category,state=state,firstrev=firstrev,secrev=secrev)

##couple error handler
@app.errorhandler(404)
def error_page_404(errormessage):
    if session.get('loggedin')!=None:
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()

        return render_template('couple_error_404.html', errormessage=errormessage,getcouple=getcouple),404

##vendor's error handler
@app.errorhandler(404)
def vendor_error_page_404(errormessage):
    if session.get('loggedin')!=None:
        getvendor = db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()

        return render_template('vendor_error_404.html', errormessage=errormessage,getvendor=getvendor),404

##couple signup
@app.route('/couple_signup',methods =['POST','GET'])
def couple_singup():
    if request.method == 'GET':

        return render_template('userform.html')
    else:
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if name==''or email==''or password=='':
            flash('please input details')
            return redirect ('/couple_login')
        
        else:
            enc_password = generate_password_hash(password)
            u = Couple(couple_name=name, couple_email=email,couple_pass=enc_password)
            db.session.add(u)
            db.session.commit()
            msg=Message(subject=f"Welcome to Wedding Wheel {name}", sender="weddingwheel@gmail.com", recipients=[email])
            msg.html=f"Hello {name}, thank you for choosing wedding wheel for your wedding planning. We are super excited to have you onboard."
            mail.send(msg)
            id=u.couple_id
            if id != None:
                flash(f'Thank you for signing up with us, your username is {name}')
            return redirect ('/couple_login')

##couple email check
@app.route('/email_check')
def email_check():
    email=request.args.get('email')
    coup=db.session.query(Couple).filter(Couple.couple_email==email).first()
    msg=""
    if coup:
        msg+="Email is already in use"
        return msg
    else:
        return msg

##couple username check
@app.route('/name_check')
def name_check():
    name=request.args.get('username')
    mycoup=db.session.query(Couple).filter(Couple.couple_name==name).first()
    themsg=""
    if mycoup:
        themsg+="name is already in use"
        return themsg
    else:
        return themsg

##couple login
@app.route('/couple_login',methods =['POST','GET'])
def couple_login():
    

    if request.method == 'GET':
        return render_template('userform.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        record = db.session.query(Couple).filter(Couple.couple_name==username).first()
        if username=='admin' and password=='1234':
            theadmin = db.session.query(Admin).filter(Admin.admin_username==username).first()
            session['admin']=theadmin.admin_id
            return redirect('/admin_dashboard')

        elif record and check_password_hash(record.couple_pass,password):           
                session['loggedin']=record.couple_id
                return redirect('/user_dashboard')

        else:
            flash('Failed login')
            return redirect('/couple_login')


##vendor signup
@app.route('/vendor_signup',methods =['POST','GET'])
def vendor_singup():
    if request.method == 'GET':

        return render_template('vendorform.html')
    else:
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        bizname = request.form.get('businessname')
        enc_password = generate_password_hash(password)
        ven = Vendor(vendor_name=name, vendor_business_name = bizname,vendor_email=email,vendor_pass=enc_password,status='Not Approved')
        db.session.add(ven)
        db.session.commit()
        msg=Message(subject=f"Welcome to Wedding Wheel {name}", sender="weddingwheel@gmail.com", recipients=[email])
        msg.html=f"Hello {name}, thank you for bringing your business {bizname} onboard. To proceed, kindly visit the update profile section and update your profilr to enjoy full access to the platform."
        Mail.send(msg)

        id=ven.vendor_id
        if id != None:
            flash('Thank you for signing up')
        return redirect ('/vendor_login')

##vendor email check
@app.route('/vend_email_check')
def vend_email_check():
    email=request.args.get('email')
    coup=db.session.query(Vendor).filter(Vendor.vendor_email==email).first()
    msg=""
    if coup:
        msg+="Email is already in use"
        return msg
    else:
        msg+=''
        return msg

 ##vendor username check
@app.route('/vend_name_check')
def vend_name_check():
    name=request.args.get('username')
    myvend=db.session.query(Vendor).filter(Vendor.vendor_name==name).first()
    themsg=""
    if myvend:
        themsg+="name is already in use"
        return themsg
    else:
        return themsg
   
@app.route('/vendor_login',methods =['POST','GET'])
def vendor_login():

    if request.method == 'GET':
        return render_template('vendorform.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        """Method 1"""
        venlogin = db.session.query(Vendor).filter(Vendor.vendor_name==username).first()
        """You can pass record to a test template to see the contents"""
        if venlogin and check_password_hash(venlogin.vendor_pass,password):           
            session['loggedin']= venlogin.vendor_id
            return redirect('/vendor_dashboard')
        else:
            flash('Failed login')
            return redirect ('/vendor_login')
    

##couple dashbboard
@app.route('/user_dashboard',methods =['POST','GET'])
def main_user_dashboard():
    if session.get('loggedin') !=None:
        record = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()
        allwish = db.session.query(Wishlist).filter(Wishlist.couple_wish_id==session.get('loggedin')).all()
        quotesent = db.session.query(Quotes).filter(Quotes.user_id==session.get('loggedin')).all()
        theuser = session.get('loggedin')
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()
        all_guest=db.session.query(Myguest).filter(Myguest.couple_adding_id==session.get('loggedin')).all()
        thet=db.session.query(Task).filter(Task.c_id==session.get('loggedin')).all()
        

        return render_template('user_dashboard.html',record=record,allwish=allwish,quotesent=quotesent,theuser=theuser,getcouple=getcouple,all_guest=all_guest,thet=thet)
    else:
        return redirect('/couple_login')

##couple wishlist
@app.route('/wishlist_list/<id>',methods =['POST','GET'])
def wishlist_list(id):
        if session.get('loggedin') !=None:
            clickeditem = db.session.query(Listing).filter(Listing.listing_id==id).all()
            thecouple=session.get('loggedin')
            clickwish = Wishlist(wish_listing_id=id,couple_wish_id=thecouple)
            db.session.add(clickwish)
            db.session.commit()

            thewish=clickwish.wish_id
            if thewish !=None:
                flash('Item Successfully Added to your wish list')
                return redirect('/wishlist_dashboard')

            else:
                return redirect('/couple_login')

       

##couple wishlist dashboard
@app.route('/wishlist_dashboard')
def wishlist_dashboard():
    if session.get('loggedin') !=None:
        mywish = db.session.query(Wishlist).filter(Wishlist.couple_wish_id==session.get('loggedin')).all()
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()

        return render_template('user_wishlist.html',mywish=mywish,getcouple=getcouple)

##the layout for couple dashboard
@app.route('/layout_couple',methods =['POST','GET'])
def couple_dashboard_layout():
    if session.get('loggedin') !=None:
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()
        return render_template('dashboard_layout.html',getcouple=getcouple)

##the vendor dashboard layout
@app.route('/layout_vendor',methods =['POST','GET'])
def vendor_dashboard_layout():
    if session.get('loggedin') !=None:
        getvendor = db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()

        return render_template('dashboard_vendor.html',getvendor=getvendor)

            
##couple todo list
@app.route('/todo_dashboard',methods =['POST','GET'])
def todo_dashboard():
    if session.get('loggedin') !=None:
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()
        mytodo =To_do()
        if request.method=='GET':
            thet=db.session.query(Task).filter(Task.c_id==session.get('loggedin')).all()
            complete_task=db.session.query(Task).filter(Task.status=='Completed').filter(Task.c_id==session.get('loggedin')).all()
            uncomplete_task=db.session.query(Task).filter(Task.status=='Not Completed').filter(Task.c_id==session.get('loggedin')).all()

            return render_template('todo_dashboard.html',getcouple=getcouple,mytodo=mytodo,thet=thet,complete_task=complete_task,uncomplete_task=uncomplete_task)
        else:
            thetask = request.form.get('task')
            thedate =request.form.get('task_date')
            coup =session.get('loggedin')
            todo_task =Task(the_task=thetask,task_date=thedate,c_id=coup,status='Not Completed')
            db.session.add(todo_task)
            db.session.commit()
            theid = todo_task.task_id
            if theid !=None:
                flash('Task succesfully added')
                return redirect('/todo_dashboard')
            else:
                flash('Task was not added')
                return redirect('/couple_login')

##couple's completed task route
@app.route('/task_completed/<id>')
def task_completed(id):
    if session.get('loggedin')!=None:
        thetasks=db.session.query(Task).filter(Task.task_id==id).first()
        thetasks.status='Completed'
        db.session.commit()
        flash(f'Task "{thetasks.the_task}" has been completed')
        return redirect('/todo_dashboard')

    else:
        return('/couple_login')

##couple's guest list

@app.route('/guest_list',methods =['POST','GET'])
def couple_guestlist():
    if session.get('loggedin') !=None:
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()
        guest_list =Guest_list()
        if request.method=='GET':
            all_guest=db.session.query(Myguest).filter(Myguest.couple_adding_id==session.get('loggedin')).all()
            all_accept=db.session.query(Myguest).filter(Myguest.couple_adding_id==session.get('loggedin')).filter(Myguest.rsvp_status=='Confirmed').all()
            all_decline=db.session.query(Myguest).filter(Myguest.couple_adding_id==session.get('loggedin')).filter(Myguest.rsvp_status=='Declined').all()
            all_wait=db.session.query(Myguest).filter(Myguest.couple_adding_id==session.get('loggedin')).filter(Myguest.rsvp_status=='No Response').all()
            return render_template('guestlist.html',getcouple=getcouple,guest_list=guest_list,all_guest=all_guest,all_accept=all_accept,all_decline=all_decline,all_wait=all_wait)
        else:
            fname = request.form.get('first_name')
            lname = request.form.get('last_name')
            address1 = request.form.get('address_one')
            address2 = request.form.get('address_two')
            myemail = request.form.get('email')
            mycity = request.form.get('city')
            mycountry = request.form.get('country')
            mypost_code= request.form.get('post_code')
            relation=request.form.get('therelation')
            theguests = Myguest(couple_adding_id=session.get('loggedin'),first_name=fname,last_name=lname,address_one=address1,address_two=address2,email=myemail,city=mycity,country=mycountry,post_code=mypost_code,rsvp_status='No Response',invite_status='Not Sent',relationship=relation)
            db.session.add(theguests)
            db.session.commit()
            theid = theguests.invite_id
            if theid !=None:
                flash('Guest Succesfully added')
                return redirect('/guest_list')
            else:
                return redirect('/couple_login')

##couple's sent invite route
@app.route('/invite_sent/<id>')
def invite_sent(id):
    if session.get('loggedin')!=None:
        theiv=db.session.query(Myguest).filter(Myguest.invite_id==id).first()
        theiv.invite_status='Sent'
        db.session.commit()
        flash(f'Invite for {theiv.first_name} {theiv.last_name} has been sent')
        return redirect('/guest_list')

    else:
        return('/couple_login')
        
##couple's confirmed guest route
@app.route('/comfirmed_guest/<id>')
def confirmed_guest(id):
    if session.get('loggedin')!=None:
        theiv=db.session.query(Myguest).filter(Myguest.invite_id==id).first()
        theiv.rsvp_status='Confirmed'
        db.session.commit()
        flash(f'{theiv.first_name} {theiv.last_name} has been Confirmed their attendance')
        return redirect('/guest_list')

    else:
        return('/couple_login')

##declined guest
@app.route('/declined_duest/<id>')
def declined_guest(id):
    if session.get('loggedin')!=None:
        theiv=db.session.query(Myguest).filter(Myguest.invite_id==id).first()
        theiv.rsvp_status='Declined'
        db.session.commit()
        flash(f'Invite for {theiv.first_name} {theiv.last_name} has been declined')
        return redirect('/guest_list')

    else:
        return('/couple_login')

##delete todo task
@app.route('/delete_task/<id>')
def delete_task(id):
    if session.get('loggedin')!=None:
        thetasks=db.session.query(Task).filter(Task.task_id==id).first()
        db.session.delete(thetasks)
        db.session.commit()
        flash(f'Task "{thetasks.the_task}" has been deleted')
        return redirect('/todo_dashboard')

    else:
        return('/couple_login')


##budget planner
@app.route('/budgetplanner',methods =['POST','GET'])
def budgetplanner():
    if session.get('loggedin') !=None:
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()

        return render_template('budgetplanner.html',getcouple=getcouple)

##vendor dashboard
@app.route('/vendor_dashboard',methods =['POST','GET'])
def vendor_dashboard():
    if session.get('loggedin') !=None:
        all_listings = db.session.query(Listing).filter(Listing.vendor_listing_id==session.get('loggedin')).all()
        all_quote =db.session.query(Quotes).filter(Listing.vendor_listing_id==session.get('loggedin'), Quotes.listeditem_id !=None).all()
        getvendor = db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()
        all_reviews =db.session.query(Reviews).filter(Reviews.thelisting_vendor_id==session.get('loggedin'), Reviews.thelisteditem_id !=None).all()
        return render_template('vendor_dashboard.html',all_listings=all_listings,all_quote=all_quote,getvendor=getvendor,all_reviews=all_reviews)


##listed item
@app.route('/listeditem',methods =['POST','GET'])
def listeditem():
    if session.get('loggedin') !=None:
        listeditems = db.session.query(Listing).filter(Listing.vendor_listing_id==session.get('loggedin')).all()
        getvendor = db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()

        return render_template('listeditem.html',listeditems=listeditems,getvendor=getvendor)


##new listing
@app.route('/newlisting',methods =['POST','GET'])
def newlisted():
    if session.get('loggedin') !=None:
        if request.method == 'GET':
            frm = newlisting()
            category = db.session.query(Category).all()
            state = db.session.query(State).all()
            getvendor = db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()

            return render_template('newlisting.html', frm=frm,category=category,state=state,getvendor=getvendor)
        else:


            title = request.form.get('title')
            capacity = request.form.get('capacity')
            price = request.form.get('price')
            address = request.form.get('address')
            postcode = request.form.get('postcode')
            description = request.form.get('description')
            fileobj = request.files['gallery_of_venue']
            video = request.form.get('video')
            facebook = request.form.get('facebook')
            twitter = request.form.get('twitter')
            instagram = request.form.get('instagram')
            youtube = request.form.get('youtube')
            stet_vendor = request.form.get('loc')
            category_list = request.form.get('cat')

            error =[]
            newfilename=''
            allowed =['.jpg','.png','.jpeg']

            if fileobj.filename !='':

                original_name = fileobj.filename
                filename,ext = os.path.splitext(original_name)
                """Check if extension is allowed"""
                if ext.lower() in allowed:
                    """Generate a random name"""
                    newfilename = random.random()
                    xter_list = random.sample(string.ascii_letters,12)
                    newfilename = ''.join(xter_list) + ext
                    fileobj.save(f'pkg/static/uploads/{newfilename}')
                    newitem = Listing(title=title,capacity=capacity,price=price,address=address,postcode=postcode,description=description,gallery_of_venue=newfilename,video=video,facebook=facebook,twitter=twitter,instagram=instagram,youtube=youtube,vendor_listing_id=session.get('loggedin'),vendor_category=category_list, vendor_state=stet_vendor)
                    db.session.add(newitem)
                    db.session.commit()
                    id=newitem.listing_id

                    if id != None:
                        flash('List Succesfully Added')
                        return redirect('/newlisting')
                else:
                    error.append('Extension not allowed')
            else:
                error.append('Extension not allowed')
    else:
        return redirect('/vendor_login')
        

##pricing plan
@app.route('/pricing_plan',methods =['POST','GET'])
def pricing_plan():
    if session.get('loggedin') !=None:

        getvendor = db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()

        return render_template('pricingplan.html',getvendor=getvendor)


##find vendors - the search section for couples
@app.route('/findvendors',methods =['POST','GET'])
def find_vendors():
    if session.get('loggedin') !=None:
        category = db.session.query(Category).all()
        state = db.session.query(State).all()
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()

        return render_template('search_vendors.html',state=state,category=category,getcouple=getcouple)

##quotes received by vendors
@app.route('/requested_quotes',methods =['POST','GET'])
def requested_quotes():
    if session.get('loggedin') !=None:
        itemquote = db.session.query(Quotes).all()
        thevendor = session.get('loggedin')
        getvendor = db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()

        return render_template('request_quote.html',thevendor=thevendor,itemquote=itemquote,getvendor=getvendor)



##the couple listing homepage
@app.route('/listing_homepage/<id>',methods =['POST','GET'])
def listing_homepage(id):
    if session.get('loggedin') !=None:
        myfrm = RequestForm()
        clickeditem = db.session.query(Listing).filter(Listing.listing_id==id)
        reviewfrm =ReviewForm()
        revs = db.session.query(Reviews).filter(Reviews.thelisteditem_id==id).limit(3)
        if request.method == 'GET':
            
            return render_template('listing_homepage.html',clickeditem=clickeditem,myfrm=myfrm,reviewfrm=reviewfrm,revs=revs)
        else:
                
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            wedding_date = request.form.get('wedding_date')
            message = request.form.get('message')
            rquote = Quotes(couple_name=name, couple_email = email,couple_phone=phone,date_sent=wedding_date,couple_message=message,user_id=session.get('loggedin'),listeditem_id =id)
            db.session.add(rquote)
            db.session.commit()
            id= rquote.quote_id
            if id != None:
                return redirect('/user_quotes')
            else:
                return redirect('/couple_login')
##the vendor's update profile section
@app.route('/vendorprofile',methods =['POST','GET'])
def vendorprofile():
    if session['loggedin'] !=None:
            getvendor = db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()
            updfrm=Vendor_profile()
            chgpwd=Change_password()
            state =db.session.query(State).all()
            if request.method=='GET':
                    return render_template('vendor_profile.html',getvendor=getvendor,updfrm=updfrm,chgpwd=chgpwd,state=state)
            
            else:
                    fileobj= request.files['vend_img']
                    allowed =['.jpg','.png','.jpeg']
                    error =[]
                    newfilename=''
                    if fileobj.filename !='':

                        original_name = fileobj.filename
                        filename,ext = os.path.splitext(original_name)
                        """Check if extension is allowed"""
                        if ext.lower() in allowed:
                            """Generate a random name"""
                            myfilename = random.random()
                            xter_list = random.sample(string.ascii_letters,12)
                            newfilename = ''.join(xter_list) + ext
                            fileobj.save(f'pkg/static/uploads/{myfilename}')
                        else:
                            error.append('Extension not allowed')
                    else:
                        error.append('Extension not allowed')


                    name= request.form.get('name')
                    couple_location= request.form.get('vend_location')
                    email= request.form.get('email')
                    phone= request.form.get('phone')
                    spec= request.form.get('vend_specialty')
                    ig= request.form.get('vend_instagram')
                    twt= request.form.get('vend_twitter')
                    web= request.form.get('vend_website')
                    other_links= request.form.get('vend_other_links')
        

                    getvendor = db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()
                    
                    getvendor.vendor_name = name
                    getvendor.vendor_location= couple_location
                    getvendor.vendor_email= email
                    getvendor.vendor_phone= phone
                    getvendor.vendor_image= myfilename
                    getvendor.vendor_specialty=spec
                    getvendor.vendor_twitter=twt
                    getvendor.vendor_ig=ig
                    getvendor.vendor_website=web
                    getvendor.vendor_other_links=other_links
                    db.session.commit()
                    flash('Details Updated')
                    return redirect('/vendorprofile')
    else:
        return redirect('/vendor_login')

##the couplechoice - searched vendor
@app.route('/couplechoice',methods =['POST','GET'])
def couple_choice():
    if session.get('loggedin') !=None:
        myfrm = RequestForm()
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()

        location= request.form.get('local')
        cate = request.form.get('cat')
        data = db.session.query(Listing).filter(Listing.vendor_category==cate, Listing.vendor_state==location).all()
        return render_template('couple_choice.html',data=data, myfrm=myfrm,getcouple=getcouple)
    else:
        return redirect('/couple_login')

##vendor listing homepage
@app.route('/vendor_listing_homepage/<id>')
def vendor_listing_homepage(id):
    if session.get('loggedin') !=None:
        clickeditem = db.session.query(Listing).filter(Listing.listing_id==id)
        getvendor = db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()

        return render_template('vendor_listing_homepage.html',clickeditem=clickeditem,getvendor=getvendor)

##quotes sent
@app.route('/user_quotes')
def user_quotes():
    if session.get('loggedin') !=None:
        quotesent = db.session.query(Quotes).all()
        theuser = session.get('loggedin')
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()

        return render_template('users_quote.html',quotesent=quotesent,theuser=theuser,getcouple=getcouple)

##vendor logout
@app.route('/vendor_logout')
def vendor_logout():
    if session.get('loggedin') !=None:
        session.pop('loggedin')

    return redirect('/home')

##couple logout
@app.route('/couple_logout')
def couple_logout():
    if session.get('loggedin') !=None:
        session.pop('loggedin')

    return redirect('/home')

##admin logout
@app.route('/admin_logout')
def admin_logout():
    if session.get('admin') !=None:
        session.pop('admin')

    return redirect('/home')
##vendor listing delete          
@app.route('/vendor/delete/<id>')
def delete_item(id):
    if session.get('loggedin'):
        itemdelete = db.session.query(Listing).get(id)
        Listing.listing_id==id
        db.session.delete(itemdelete)
        db.session.commit()
        flash('Item Successfully deleted')
        return redirect('/listeditem')
    else:
        return redirect('/vendor_login')

##delete from couple wishlist
@app.route('/couple_wish/delete/<id>')
def wish_item(id):
    if session.get('loggedin'):
        wishdelete = db.session.query(Wishlist).get(id)
        Wishlist.wish_id==id
        db.session.delete(wishdelete)
        db.session.commit()
        flash('Item Successfully deleted')
        return redirect('/wishlist_dashboard')
    else:
        return redirect('/couple_login')

##couple profile
@app.route('/couple_profile',methods =['POST','GET'])
def couple_profile():
    if session.get('loggedin') !=None:
        if request.method =='GET':
            getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()
            updfrm=Couple_profile()
            chgpwd=Change_password()
            state =db.session.query(State).all()
            return render_template('user_profile.html',getcouple=getcouple,updfrm=updfrm,chgpwd=chgpwd,state=state)
        else:
            fileobj= request.files['couple_img']
            allowed =['.jpg','.png','.jpeg']
            error =[]
            newfilename=''
            if fileobj.filename !='':

                original_name = fileobj.filename
                filename,ext = os.path.splitext(original_name)
                """Check if extension is allowed"""
                if ext.lower() in allowed:
                    """Generate a random name"""
                    newfilename = random.random()
                    xter_list = random.sample(string.ascii_letters,12)
                    newfilename = ''.join(xter_list) + ext
                    fileobj.save(f'pkg/static/uploads/{newfilename}')
                else:
                    error.append('Extension not allowed')
            else:
                error.append('Extension not allowed')


            name= request.form.get('name')
            couple_location= request.form.get('couple_location')
            email= request.form.get('email')
            phone= request.form.get('phone')
            updcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()
            
            updcouple.couple_name = name
            updcouple.couple_location= couple_location
            updcouple.couple_email= email
            updcouple.couple_phone= phone
            updcouple.couple_image= newfilename
            db.session.commit()
            flash('Details Updated')
            return redirect('/couple_profile')
    else:
        return redirect('/couple_login')


##reviews

@app.route('/reviews/<id>',methods =['POST','GET'])
def thereviews(id):
    if session.get('loggedin') !=None:

            rname=request.form.get('rname')
            remail=request.form.get('remail')
            rmessage =request.form.get('thereview')
            vend = db.session.query(Listing).filter(Listing.listing_id==id).first()
            rev = Reviews(couple_name=rname, couple_email=remail, thecouple_id=session.get('loggedin'), rating=rmessage, thelisteditem_id=id, thelisting_vendor_id=vend.vendor_listing_id)
            db.session.add(rev)
            db.session.commit()
            
            myid = rev.review_id
            
            if myid !=None:
                data ={'Posted By':rname, "Review":rmessage}
                data_json =jsonify(data)
                return data_json          
            else:
                flash('Review not added')
                return redirect('/user_dashboard')
##review per listing
@app.route('/vendor_reviews',methods =['POST','GET'])
def vendor_reviews():
    if session.get('loggedin') !=None:

        getvendor = db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()
        myvendor = session.get('loggedin')
        getreviews = db.session.query(Reviews).all()
        return render_template('vendor_review.html',getvendor=getvendor,myvendor=myvendor,getreviews=getreviews)

##admin dashboard layout
@app.route('/admin_layout',methods =['POST','GET'])
def admin_dashboard():
    if session.get('admin')!=None:
        return render_template('admin_layout.html')

##admin dashboard 

@app.route('/admin_dashboard',methods =['POST','GET'])
def admin():
    if session.get('admin') !=None:
        vendorslist= db.session.query(Vendor).all()
        clist =db.session.query(Couple).all()
        alllisting=db.session.query(Listing).all()
        return render_template('admin_dashboard.html',vendorslist=vendorslist,clist=clist,alllisting=alllisting)
    else:
        return redirect('/couple_login')
##all vendors
@app.route('/admin/vendors',methods =['POST','GET'])
def thevendors():
    if session.get('admin')!=None:
        vendorslist= db.session.query(Vendor).all()

        return render_template('all_vendors.html',vendorslist=vendorslist)

##each vendor details
@app.route('/admin/vendors/<id>')
def eachvendors(id):
    if session.get('admin')!=None:
        eachvend= db.session.query(Vendor).filter(Vendor.vendor_id==id).all()

        return render_template('each_vendor.html',eachvend=eachvend)

##all couples
@app.route('/admin/couples',methods =['POST','GET'])
def thecouples():
    if session.get('admin')!=None:
        couplelist= db.session.query(Couple).all()

        return render_template('all_couples.html',couplelist=couplelist)
##each couple details
@app.route('/admin/couples/<id>')
def eachcouples(id):
    if session.get('admin')!=None:
        eachcouple= db.session.query(Couple).filter(Couple.couple_id==id).all()

        return render_template('each_couples.html',eachcouple=eachcouple)

#all listing
@app.route('/admin/listings',methods =['POST','GET'])
def listings():
    if session.get('admin')!=None:
        alllisting=db.session.query(Listing).all()

        return render_template('all_listing.html',alllisting=alllisting)
##approve vendor
@app.route('/admin/approve/<id>',methods =['POST','GET'])
def approve_vendors(id):
    if session.get('admin')!=None:
        vendors=db.session.query(Vendor).filter(Vendor.vendor_id==id).first()
        vendors.status='Approved'
        db.session.commit()
        flash(f'Vendor {vendors.vendor_name} has been approved')
        return redirect('/admin/vendors')

    else:
        return('/couple_login')
##susppend vendor
@app.route('/admin/ban/<id>',methods =['POST','GET'])
def ban_vendors(id):
    if session.get('admin')!=None:
        vendors=db.session.query(Vendor).filter(Vendor.vendor_id==id).first()
        vendors.status='Suspended'
        db.session.commit()
        flash(f'Vendor {vendors.vendor_name} has been Suspended')
        return redirect('/admin/vendors')

    else:
        return('/couple_login')
##guest seating arrangement
@app.route('/guest_seat')
def guest_seat():
    if session.get('loggedin') !=None:
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()

        return render_template('guest_sitting.html',getcouple=getcouple,)
##real wedding blog
@app.route('/real_wedding',methods =['POST','GET'])
def real_wedding():
    if session.get('loggedin') !=None:
        getcouple = db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()
        wed=Real_wedding()
        myvend=db.session.query(Category).all()
        if request.method =='GET':
            return render_template('real_wedding.html',getcouple=getcouple,wed=wed,myvend=myvend)
        else:
            myobj= request.files['featured_image']
            allowed =['.jpg','.png','.jpeg']
            error =[]
            newfilename=''
            if myobj.filename !='':

                original_name = myobj.filename
                filename,ext = os.path.splitext(original_name)
                """Check if extension is allowed"""
                if ext.lower() in allowed:
                    """Generate a random name"""
                    newfilename = random.random()
                    xter_list = random.sample(string.ascii_letters,12)
                    newfilename = ''.join(xter_list) + ext
                    myobj.save(f'pkg/static/uploads/{newfilename}')
                else:
                    error.append('Extension not allowed')
            else:
                error.append('Extension not allowed')
            cat = request.form.get('vendor')
            cat2 = request.form.get('vendor2')
            cat_name1 = request.form.get('add_vendor')
            cat_name2 = request.form.get('add_vendor2')
            wed_wed = request.form.get('featured_story')

            mystory=Wed_story(real_coupl_id=session.get('loggedin'),real_img=newfilename,real_vend_cat1=cat_name1,real_vend_cat2=cat_name2,real_vend1=cat,real_vend2=cat2,wedding_story=wed_wed)
            db.session.add(mystory)
            db.session.commit()
            id=mystory.real_id
            if id !=None:
                flash('Story subhmitted succesfully')
                return redirect('/real_wedding')
            else:
                return redirect('/couple_login')


##admin_listing_hompage
@app.route('/admin_listing_hompage/<id>',methods =['POST','GET'])
def admin_listing_hompage(id):
    if session.get('admin') !=None:
        myfrm = RequestForm()
        clickeditem = db.session.query(Listing).filter(Listing.listing_id==id)
        reviewfrm =ReviewForm()

        if request.method == 'GET':
            
            return render_template('admin_listing_homepage.html',clickeditem=clickeditem,myfrm=myfrm,reviewfrm=reviewfrm)
        else:
                
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            wedding_date = request.form.get('wedding_date')
            message = request.form.get('message')
            rquote = Quotes(couple_name=name, couple_email = email,couple_phone=phone,date_sent=wedding_date,couple_message=message,user_id=session.get('admin'),listeditem_id =id)
            db.session.add(rquote)
            db.session.commit()
            id= rquote.quote_id
            if id != None:
                return redirect('/admin_dashboard')
            else:
                return redirect('/couple_login')

##couple change password
@app.route('/coup_changepwd',methods =['POST','GET'])
def coup_changepwd():
    if session.get('loggedin'):
                current_pass= request.form.get('current_pass')
                theperson= db.session.query(Couple).filter(Couple.couple_id==session.get('loggedin')).first()
                if theperson and check_password_hash(theperson.couple_pass,current_pass) ==True:
                    new_pass = request.form.get('new_pass') 
                    confirm_pass = request.form.get('confirm_pass')    
                    if new_pass==confirm_pass:
                            encrypted_password = generate_password_hash(new_pass)
                            theperson.couple_pass=encrypted_password
                            db.session.commit()

                            flash('Password Succesfully Changed')
                            return redirect('/couple_profile')
                    
                    else:
                        flash('Password does not match')

                        return redirect('/couple_profile')
                else:
                    flash('Incorrect Password')

                    return redirect('/couple_profile')

    else:
        return redirect('/couple_login')

##vendor change password

@app.route('/vend_changepwd',methods =['POST','GET'])
def vend_changepwd():
    if session.get('loggedin'):
                current_pass= request.form.get('current_pass')
                theperson= db.session.query(Vendor).filter(Vendor.vendor_id==session.get('loggedin')).first()
                new_pass = request.form.get('new_pass') 
                confirm_pass = request.form.get('confirm_pass') 
                if check_password_hash(theperson.vendor_pass,current_pass) ==True:                       
                    if new_pass==confirm_pass:
                            encrypted_password = generate_password_hash(new_pass)
                            theperson.vendor_pass=encrypted_password
                            db.session.commit()
                            flash('Password Succesfully Changed')
                            return redirect('/vendorprofile')
                    
                    else:
                        flash('Password does not match')

                        return redirect('/vendorprofile')
                else:
                    flash('Incorrect Password')

                    return redirect('/vendorprofile')

    else:
        return redirect('/vendor_login')


