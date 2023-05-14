from flask import Blueprint, session, render_template,redirect,url_for,request,flash,redirect,current_app, session,copy_current_request_context
from flask_security import login_required, current_user,logout_user
from flask_security.forms import LoginForm,RegisterForm
from app.models import User, Notification, Post, Comments, Hashtag_counter, Hashtag
from app import db , app , socketio , thread_lock, thread 
from flask_security.utils import hash_password, verify_and_update_password
from app.forms import MoreAboutForm,BirthDayForm,LikesForm,DislikesForm, PostForm, CaptionForm, EventForm, PhoneForm, PhotoForm, ProfileForm
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import secrets
import os
from datetime import datetime, date
from PIL import Image
import json, re


from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect


from flask import jsonify




index_blueprint = Blueprint('home', __name__, 
    static_folder='static', static_url_path = '/static')



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



# UPLOAD  PICTURE FUNTIONS

# funtion to check if the uploaded file is in the  allowed file extenion list
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# funtion that simply returns the file extenion 
def file_ext(filename):
    return str(filename.rsplit('.', 1)[1].lower()) 

# funtion prints the current time of posting in the format -- 'Saturday 17 October 2020'
def current_time():
    return str(datetime.now().strftime("%A %d %B %Y"))



#funtion to generate random name
def random_name(filename):
    random_hex = str(secrets.token_hex(8))
    #the return statement below returns a random name for each file with different parameters separated by underscores 
    return   current_user.first_name + '_' + current_user.last_name + '_' + name_list[0] + '__' + random_hex + '__' + current_time() + '.' + ex




# function to print all the hashtags in a text
def extract_hashtags(text):
    
    # the regular expression
    regex = "#(\w+)"
    
    # extracting the hashtags
    hashtag_list = re.findall(regex, text)
    
    # printing the hashtag_list
    print("The hashtags in \"" + text + "\" are :")
    for hashtag in hashtag_list:
        print(hashtag)

    return hashtag_list







    # procesed_date = [

    # {'day' : difference.days},
    # {'min' : difference.min},
    # {'second' : difference.seconds},

    # ]




@app.template_filter()
def format_datetime(the_datetime_object):

    #print('now---> ',datetime.now() ,'\n', 'then--->', the_datetime_object, '\n\n' )

    difference = datetime.now() - the_datetime_object

    #print('difference---> ', difference)

    processed_date = difference

    if difference.days == 0 and difference.seconds < 60:
        processed_date = 'just now'

    elif difference.days == 0 and difference.seconds > 60 and int((difference.seconds/60)) == 1:
        processed_date = "1 min ago"

    elif difference.days == 0 and int((difference.seconds/60)) >= 1 and int((difference.seconds/60)) < 60 :
        processed_date = str(int((difference.seconds/60))) + " mins ago"

    elif difference.days == 0 and int((difference.seconds/3600)) == 1  :
        processed_date = " 1 hr ago"

    elif difference.days == 0 and int((difference.seconds/3600)) > 1 and int((difference.seconds/3600)) < 24  :
        processed_date = str(int((difference.seconds/3600))) + " hrs ago"

    elif difference.days == 1 :
        processed_date =  " 1 day ago"

    elif difference.days > 1  and difference.days < 2 :
        processed_date =  "yesterday"

    elif difference.days > 1 and int(difference.days/30) < 1:
        processed_date = str(difference.days) +  " days ago "

    elif difference.days > 1 and int(difference.days/30) == 1 :
        processed_date = str(int(difference.days/30)) +  " month ago"

    elif difference.days > 1 and int(difference.days/30) > 1 and int(difference.days/30) < 12 :
        processed_date = str(int(difference.days/30)) +  " months ago"

    elif difference.days == 365 and int(difference.days/30) == 12 :
        processed_date =  " 1 year ago"

    elif difference.days > 365 and int(difference.days/30) > 12 :
        processed_date = str(int(difference.days/30)) +  " years ago"


    return processed_date






banks = [

("ALAT by Wema","ALAT by Wema"),
("Access Bank PLC","Access Bank PLC"),
("Aso Savings","Aso Savings"),
("Ecobank","Ecobank"),
("Ekondo Microfinance Bank","Ekondo Microfinance Bank"),
("Fidelity Bank Nigeria","Fidelity Bank Nigeria"),
("First Bank Nigeria","First Bank Nigeria"),
("First City Monument Bank Ltd","First City Monument Bank Ltd"),
("Guaranty Trust Bank","Guaranty Trust Bank"),
("Heritage Bank PLC","Heritage Bank PLC"),
("Keystone Bank Limited","Keystone Bank Limited"),
("Mainstreet Bank","Mainstreet Bank"),
("Polaris Bank","Polaris Bank"),
("Stanbic IBTC Bank","Stanbic IBTC Bank"),
("Sterling Bank Plc","Sterling Bank Plc"),
("Union Bank Nigeria","Union Bank Nigeria"),
("United Bank for Africa","United Bank for Africa"),
("Wema Bank","Wema Bank"),
("Zenith Bank","Zenith Bank"),

]



star_signs =    [

("♈ aries","♈ aries"),
(" ♉ taurus"," ♉ taurus"),
(" ♊ gemini"," ♊ gemini"),
(" ♋ cancer"," ♋ cancer"),
(" ♌ leo"," ♌ leo"),
(" ♌ leo"," ♌ leo"),
(" ♍ virgo"," ♍ virgo"),
(" ♎ libra"," ♎ libra"),
(" ♏ scorpio"," ♏ scorpio"),
(" ♐ sagittarius"," ♐ sagittarius"),
(" ♑ capricorn"," ♑ capricorn"),
(" ♒ aquarius"," ♒ aquarius"),
(" ♓ pisces"," ♓ pisces")

]



price_range = [

('Greater than 10k', 'Greater than 10k'),
('Greater than 20k', 'Greater than 20k'),
('Greater than 30k', 'Greater than 30k'),
('Greater than 40k', 'Greater than 40k'),
('50k and above', '50k and above')

]


relationships=[

("single", 'single'),
("situationship", 'situationship'),
("complicated", 'complicated'),
("im an engineering Student ", 'im an engineering Student '),
("in an abusive relationship ", 'in an abusive relationship'),
("dont have the time ", 'dont have the time '),
("waiting for someone", 'waiting for someone'),
("prefer not to say", 'prefer not to say')

]



levels=[

("high school graduate", 'high school graduate'),
("fresher", 'fresher'),
("200L", '200L'),
("300L", '300L'),
("400L", '400L'),
("final year", 'final year'),
("alumni", 'alumni')


]



answers=[

("YES", 'YES'),
("NO", 'NO')


]




departments = [

("AGRIC-ECONOMICS AND EXTENSION" , 'AGRIC-ECONOMICS AND EXTENSION'),
("AGRICULTURAL AND BIORESOURCES ENGINEERING" , 'AGRICULTURAL AND BIORESOURCES ENGINEERING'),
("AGRICULTURE" , 'AGRICULTURE'),
("ANIMAL PRODUCTION" , 'ANIMAL PRODUCTION'),
("APPLIED GEOPHYSICS" , 'APPLIED GEOPHYSICS'),
("ARCHITECTURE" , 'ARCHITECTURE'),
("BIOCHEMISTRY" , 'BIOCHEMISTRY'),
("BIOLOGY" , 'BIOLOGY'),
("BOTANY" , 'BOTANY'),
("BUILDING" , 'BUILDING'),
("CHEMICAL ENGINEERING:" , 'CHEMICAL ENGINEERING:'),
("CHEMISTRY" , 'CHEMISTRY'),
("CIVIL ENGINEERING" , 'CIVIL ENGINEERING'),
("COMPUTER ENGINEERING:" , 'COMPUTER ENGINEERING:'),
("COMPUTER SCIENCE" , 'COMPUTER SCIENCE'),
("COMPUTER WITH STATISTICS" , 'COMPUTER WITH STATISTICS'),
("CROP PRODUCTION" , 'CROP PRODUCTION'),
("CYBER SECURITY SCIENCE" , 'CYBER SECURITY SCIENCE'),
("EDUCATION AND BIOLOGY" , 'EDUCATION AND BIOLOGY'),
("EDUCATION AND CHEMISTRY:" , 'EDUCATION AND CHEMISTRY:'),
("EDUCATION AND GEOGRAPHY" , 'EDUCATION AND GEOGRAPHY'),
("EDUCATION AND MATHEMATICS" , 'EDUCATION AND MATHEMATICS'),
("EDUCATION AND PHYSICS" , 'EDUCATION AND PHYSICS'),
("EDUCATION AND SCIENCE" , 'EDUCATION AND SCIENCE'),
("EDUCATION TECHNOLOGY" , 'EDUCATION TECHNOLOGY'),
("ELECTRICAL AND COMPUTER ENGINEERING" , 'ELECTRICAL AND COMPUTER ENGINEERING'),
("ESTATE MANAGEMENT" , 'ESTATE MANAGEMENT'),
("FISHERIES AND AQUACULTURE:" , 'FISHERIES AND AQUACULTURE:'),
("FOOD SCIENCE AND TECHNOLOGY" , 'FOOD SCIENCE AND TECHNOLOGY'),
("GEOGRAPHY" , 'GEOGRAPHY'),
("GEOLOGY" , 'GEOLOGY'),
("HORTICULTURE:" , 'HORTICULTURE:'),
("INDUSTRIAL EDUCATION TECHNOLOGY" , 'INDUSTRIAL EDUCATION TECHNOLOGY'),
("INFORMATION AND MEDIA TECHNOLOGY" , 'INFORMATION AND MEDIA TECHNOLOGY'),
("MATHEMATICS WITH COMPUTER SCIENCE" , 'MATHEMATICS WITH COMPUTER SCIENCE'),
("MATHEMATICS WITH STATISTICS" , 'MATHEMATICS WITH STATISTICS'),
("MECHANICAL ENGINEERING" , 'MECHANICAL ENGINEERING'),
("MECHATRONICS ENGINEERING" , 'MECHATRONICS ENGINEERING'),
("METALLURGICAL AND MATERIAL ENGINEERING" , 'METALLURGICAL AND MATERIAL ENGINEERING'),
("MICROBIOLOGY" , 'MICROBIOLOGY'),
("PHYSICS" , 'PHYSICS'),
("QUANTITY SURVEYING" , 'QUANTITY SURVEYING'),
("SCIENCE EDUCATION" , 'SCIENCE EDUCATION'),
("STATISTICS" , 'STATISTICS'),
("SURVEYING AND GEOINFORMATICS" , 'SURVEYING AND GEOINFORMATICS'),
("TELECOMMUNICATION ENGINEERING" , 'TELECOMMUNICATION ENGINEERING'),
("URBAN AND REGIONAL PLANNING:" , 'URBAN AND REGIONAL PLANNING:'),
("WATER RESOURCES, AQUACULTURE AND FISHERIES TECHNOLOGY" , 'WATER RESOURCES, AQUACULTURE AND FISHERIES TECHNOLOGY'),
("ZOOLOGY" , 'ZOOLOGY')


]



religions = [

('Atheism', 'Atheism'),
('Buddhism', 'Buddhism'       ),
('Christianity', 'Christianity'   ),
('Confucianism', 'Confucianism'            ),
('Hinduism', 'Hinduism'        ),
('Islam', 'Islam'  ),
('Jainism', 'Jainism'     ),
('Judaism', 'Judaism' ),
('Sikhism', 'Sikhism'    ),
('Shintoism', 'Shintoism'           ),
('Taoism', 'Taoism'             ),
('Zoroastrianism', 'Zoroastrianism'            ),
('Druze', 'Druze'   ),
('Sikhism', 'Sikhism' ),
('Taoism', 'Taoism' ),
('Shinto', 'Shinto'  ),
('Judaism', 'Judaism' ),
('Confucianism', 'Confucianism'    ),
('Spiritism', 'Spiritism'  ),
('TST', 'TST'  ),
('shamanism', 'shamanism'    ),
('Caodaism', 'Caodaism'   ),
('Baháʼí_Faith', 'Baháʼí_Faith'    ),
('Jainism', 'Jainism'),
('Cheondoism', 'Cheondoism'  ),
('Hoahaoism', 'Hoahaoism'  ),
('Tenriism', 'Tenriism'),
("prefer not to say", 'prefer not to say')

]



genders = [

('Male', 'Male'),
('Female', 'Female'),
("Agender", "Agender"),
("Androgyne", "Androgyne"),
("Androgynous", "Androgynous"),
("Bigender", "Bigender"),
("Cis", "Cis"),
("Cisgender", "Cisgender"),
("Cis Female", "Cis Female"),
("Cis Male", "Cis Male"),
("Cis Man", "Cis Man"),
("Cis Woman", "Cis Woman"),
("Cisgender Female", "Cisgender Female"),
("Cisgender Male", "Cisgender Male"),
("Cisgender Man", "Cisgender Man"),
("Cisgender Woman", "Cisgender Woman"),
("Female to Male", "Female to Male"),
("FTM", "FTM"),
("Gender Fluid", "Gender Fluid"),
("Gender Nonconforming", "Gender Nonconforming"),
("Gender Questioning", "Gender Questioning"),
("Gender Variant", "Gender Variant"),
("Genderqueer", "Genderqueer"),
("Intersex", "Intersex"),
("Male to Female", "Male to Female"),
("MTF", "MTF"),
("Neither", "Neither"),
("Neutrois", "Neutrois"),
("Non-binary", "Non-binary"),
("Other", "Other"),
("Pangender", "Pangender"),
("Trans", "Trans"),
("Trans*", "Trans*"),
("Trans Female", "Trans Female"),
("Trans* Female", "Trans* Female"),
("Trans Male", "Trans Male"),
("Trans* Male", "Trans* Male"),
("Trans Man", "Trans Man"),
("Trans* Man", "Trans* Man"),
("Trans Person", "Trans Person"),
("Trans* Person", "Trans* Person"),
("Trans Woman", "Trans Woman"),
("Trans* Woman", "Trans* Woman"),
("Transfeminine", "Transfeminine"),
("Transgender", "Transgender"),
("Transgender Female", "Transgender Female"),
("Transgender Male", "Transgender Male"),
("Transgender Man", "Transgender Man"),
("Transgender Person", "Transgender Person"),
("Transgender Woman", "Transgender Woman"),
("Transmasculine", "Transmasculine"),
("Transsexual", "Transsexual"),
("Transsexual Female", "Transsexual Female"),
("Transsexual Male", "Transsexual Male"),
("Transsexual Man", "Transsexual Man"),
("Transsexual Person", "Transsexual Person"),
("Transsexual Woman", "Transsexual Woman"),
("Two-Spirit", "Two-Spirit"),
("prefer not to say", 'prefer not to say')

]



locations = [


("Bosso","Bosso"),
("Gidan Kwano","Gidan Kwano"),
("Tunga","Tunga"),
("Talba Road","Talba Road"),
("Dama","Dama"),
("Gidan kwano campus hostel","Gidan kwano campus hostel"),
("Bosso campus hostel","Bosso campus hostel"),



]









@index_blueprint.route('/view-notifications')
@login_required
def notifications():
    notifications = current_user.new_notifications()

    return render_template("home/notifications.html", notifications = notifications)







@index_blueprint.route('/search_db_general', methods=['POST'] )  
def search_db_general():

    query = request.get_json() or {}

    print('\n', json.dumps(query) )

    try:

        form_data = query['value']

        search_type = query['search_type']

    except KeyError:
        pass


    posts = Post.query.filter(Post.content.contains( str(form_data.strip().lower()) ) ).limit(5).all()

    s = Post.query.whoosh_search('a').all()

    print('s---> ', s )


    return render_template("home/searched_items_template.html", posts = posts, keyword = form_data, search_type = search_type) 






@index_blueprint.route('/search_db_general_see_all_posts', methods=['POST'] )  
def search_db_general_see_all_posts():

    query = request.get_json() or {}

    print('\n', json.dumps(query) )

    try:

        form_data = query['value']

        search_type = query['search_type']

    except KeyError:
        pass


    posts = Post.query.filter(Post.content.contains( str(form_data.strip().lower()) ) ).all()


    return render_template("home/searched_items_template.html", posts = posts, keyword = form_data, search_type = search_type) 







@index_blueprint.route('/search_specific', methods=['POST'] )  
def search_specific():

    query = request.get_json() or {}

    print('\n', json.dumps(query) )

    try:

        form_data = query['value']

        search_type = query['search_type']

    except KeyError:
        pass


    if search_type == 'posts':

        posts = Post.query.filter(Post.content.contains( str(form_data.strip().lower()) ) ).limit(5).all()


    if search_type == 'people':

        # users = User.query.all()

        # for user in users:
        #     user.first_name = user.first_name.lower()
        #     user.last_name = user.last_name.lower()
        #     db.session.commit()


        one = User.query.filter(User.first_name.contains( str(form_data.strip()) )  ).order_by(User.id.asc()).all()

        two = User.query.filter(User.last_name.contains( str(form_data.strip()) )  ).order_by(User.id.asc()).all()

        three = User.query.filter(User.email.contains( str(form_data.strip()) )  ).order_by(User.id.asc()).all()

        if one != none:
            posts = one.extend(two)
            print('1--->', posts)

        if two != none:
            posts = posts.extend(three)
            print('2--->', posts)


        posts = list(set(posts))
        print('3--->', posts)



    if search_type == 'places':

        posts = User.query.filter(User.first_name.startswith( str(form_data.strip()) )  ).order_by(User.id.asc()).limit(5).all()

        print(posts)






    return render_template("home/searched_items_template.html", posts = posts, keyword = form_data, search_type = search_type) 











# @index_blueprint.route('/',methods=['GET', 'POST']) 
# def index():

#     return render_template("home/home.html")










@index_blueprint.route('/',methods=['GET', 'POST']) 
def index():

    return render_template("home/new_index.html")









@index_blueprint.route('/general',methods=['GET', 'POST']) 
@login_required
def general():

    return render_template("home/new_general.html")




















@index_blueprint.route('/make_post',methods=['GET', 'POST']) 
@login_required
def make_post():

    #funtion to generate random reference code
    def random_reference_code():
        random_hex = str(secrets.token_hex(8))
        return   current_user.email + '_' + random_hex 


    form = PostForm(CombinedMultiDict((request.files, request.form)))

    user_bank_accounts = json.loads(current_user.account_numbers)

    comments = Comments.query.filter_by(post_id = 0)

    # logic for other post fields
    if  request.method == 'POST' :

        print('posted')

        #print(form)
    # logic for uploading profile pic only
        #the request.files object intance

        file = form.photo.data

        venue =  form.venue.data.lower().lstrip()
        title =  form.title.data or ''
        content =  form.content.data.lower().lstrip()
        price =  form.price.data
        normal_post_indicator =  form.normal_post_indicator.data.lower().lstrip() 
        event_indicator = form.event_indicator.data.lower()
        lost_item_indicator = form.lost_item_indicator.data or ''
        found_item_indicator = form.found_item_indicator.data
        add_account_indicator = form.add_account_indicator.data
        possession = form.possession.data
        bank  = form.bank.data



        print(

       'venue--->', venue , '\n' ,
        'title--->', title , '\n' ,
        'content--->', content , '\n' ,
        'price--->', price , '\n' ,
        'normal_post_indicator--->', normal_post_indicator , '\n' ,
        'event_indicator--->', event_indicator , '\n' ,
        'lost_item_indicator--->', lost_item_indicator , '\n' ,
        'found_item_indicator--->', found_item_indicator , '\n' ,
        'add_account_indicator--->', add_account_indicator , '\n' ,
        'possession--->', possession , '\n' ,
        'bank--->', bank  



            )




        date = request.form.get('datepicker')

        date_range_start = request.form.get('datepicker_start')

        date_range_stop = request.form.get('datepicker_end')
     


        #generate random string 8 digits long
        random_hex = secrets.token_hex(5)

       # print(date, venue, title, content)


        if event_indicator and venue and date and content:

            print("event form")

            print(event_indicator,'\n\n', venue,'\n\n', date,'\n\n', content,'\n\n', file)

            if file and allowed_file(file.filename) and file.filename != '' and venue  and content and date :
                print("entere last block")
                split_file_name = os.path.splitext(file.filename)
                name_list = list(split_file_name)
                ex = str(file_ext(file.filename))
                secure = secure_filename(file.filename)

                #funtion to generate random name
                def random_name(filename):
                    random_hex = str(secrets.token_hex(8))
                    #the return statement below returns a random name for each file with different parameters separated by underscores 
                    return   current_user.first_name + '_' + current_user.last_name + '_' + name_list[0] + '__' + random_hex + '__' + current_time() + '.' + ex


                #the name of the file gets assigned to the randomly generated file name 
                filename  = random_name(file.filename)

                edited_filename = filename

                print('edited_filename--->', edited_filename)
              
                uploads_path = os.path.join(current_app.root_path, 'static/post_IM', filename)

                print('uploaded file----->', uploads_path)

                #the next four lines just resizes the image to the given dimensions e.g 125 by 125
                output_size = (500,500)
                i = Image.open(file)
                i.thumbnail(output_size)
                i.save(uploads_path)

                #save the newly generated filename to the post database along with other form data

                formated_date = date[0:10] + " " + date[11:] 

                formated_date_as_datetime_object = datetime.strptime(formated_date, '%Y-%m-%d %H:%M')

                # print("formated date -->", formated_date)

                # print(" datetime version-->", datetime.strptime(formated_date, '%Y-%m-%d %H:%M'))


                new_reference = random_reference_code()

                post = Post(
                    
                        image_file = edited_filename,
                        title =  event_indicator,
                        venue =  venue,
                        content =  content,
                        date =  formated_date_as_datetime_object, 
                        is_event =  True,
                        author = current_user,
                        reference_code = new_reference

                        )


                db.session.add(post)
                db.session.commit()

                posts = Post.query.filter_by(author = current_user, image_file = edited_filename, reference_code = new_reference).limit(20)
                posts = list(posts) #its important to put it in a list
                print('specific post in list--->', posts )


                # --------------------------------------
                # --------------------------------------
                # EXTRACTING HASHTAGS FROM POSTS--------
                # --------------------------------------
                # --------------------------------------

                for hashtag in extract_hashtags(normal_post_indicator):
                    new_hashtag = Hashtag(
                        hashtag_name =  hashtag, 
                        author = current_user,
                        reference_code = new_reference
                        )
                    db.session.add(new_hashtag)
                    db.session.commit()


                    hashtag_exists = Hashtag_counter.query.filter_by(hashtag_name = hashtag).first()

                    if hashtag_exists == None:

                        new_hashtag_count = Hashtag_counter(
                            hashtag_name =  hashtag, 
                            author = current_user,
                            hashtag_mention_count = 1
                            )


                        db.session.add(new_hashtag)
                        db.session.commit()

                    elif hashtag_exists != None:
                        hashtag_exists.hashtag_mention_count += 1
                        db.session.commit()




                post_html = render_template("reusable/others/post-section.html", posts = posts)

                trending_hashtags = Hashtag_counter.query.order_by(Hashtag_counter.hashtag_mention_count.desc()).limit(10)

                hashtag_html = render_template("reusable/others/hashtag_html.html", trending_hashtags = trending_hashtags)

                emit('new_text_post', {'data': post_html, 'hashtag_html': hashtag_html, 'post_author': current_user.id},  namespace='/',broadcast=True)




                # flash(' EVENT CREATED ', 'success')
                return render_template("reusable/others/post-section.html", posts = posts)



        if lost_item_indicator :

            print("lost form")           

            # if the user doesnt add an image to the file uploaded

            if not file:

                print('no file')

                file = "ic_error_48px.svg"

                formated_date = date_range_start[0:10] + " " + date_range_start[11:] 

                formated_date2 = date_range_stop[0:10] + " " + date_range_stop[11:] 

                formated_date_as_datetime_object_start = datetime.strptime(formated_date, '%Y-%m-%d %H:%M')

                formated_date_as_datetime_object_stop = datetime.strptime(formated_date2, '%Y-%m-%d %H:%M')


                post = Post(
                        image_file = file,
                        content =  lost_item_indicator, 
                        is_Lost_and_searching =  True,
                        venue =  venue,
                        date =  formated_date_as_datetime_object_start,
                        date2 =  formated_date_as_datetime_object_stop,
                        author = current_user

                        )


                print(file,'\n', lost_item_indicator,'\n',venue,'\n',formated_date_as_datetime_object_start,'\n',formated_date_as_datetime_object_stop,'\n')

                db.session.add(post)
                db.session.commit()

                posts = Post.query.filter_by(author = current_user, image_file = filename).first()
                print('specific post--->', posts)

                # flash('WE HAVE PUBLISHED YOUR LOST ITEM', 'success')

                return render_template("reusable/others/post-section.html", posts = posts)



            if file and allowed_file(file.filename) and file.filename != '' and date_range_start  and date_range_stop  and venue :
                print("entered last block")
                split_file_name = os.path.splitext(file.filename)
                name_list = list(split_file_name)
                ex = str(file_ext(file.filename))
                secure = secure_filename(file.filename)

                #funtion to generate random name
                def random_name(filename):
                    random_hex = str(secrets.token_hex(8))
                #the return statement below returns a random name for each file with different parameters separated by underscores 
                    return   current_user.first_name + '_' + current_user.last_name + '_' + name_list[0] + '__' + random_hex + '__' + current_time() + '.' + ex


                #the name of the file gets assigned to the randomly generated file name 
                filename  = random_name(file.filename)
              
                uploads_path = os.path.join(current_app.root_path, 'static/post_IM', filename)

                print('uploaded file----->', uploads_path)

                #the next four lines just resizes the image to the given dimensions e.g 125 by 125
                output_size = (500,500)
                i = Image.open(file)
                i.thumbnail(output_size)
                i.save(uploads_path)

                #save the newly generated filename to the post database along with other form data
                

                formated_date = date_range_start[0:10] + " " + date_range_start[11:] 

                formated_date2 = date_range_stop[0:10] + " " + date_range_stop[11:] 

                formated_date_as_datetime_object_start = datetime.strptime(formated_date, '%Y-%m-%d %H:%M')

                formated_date_as_datetime_object_stop = datetime.strptime(formated_date2, '%Y-%m-%d %H:%M')


                post = Post(
                        image_file = filename,
                        content =  lost_item_indicator, 
                        is_Lost_and_searching =  True,
                        venue =  venue,
                        date =  formated_date_as_datetime_object_start,
                        date2 =  formated_date_as_datetime_object_stop,
                        author = current_user

                        )


                print(file,'\n', lost_item_indicator,'\n',venue,'\n',formated_date_as_datetime_object_start,'\n',formated_date_as_datetime_object_stop,'\n')

                db.session.add(post)
                db.session.commit()



                posts = Post.query.filter_by(author = current_user, image_file = filename).first()
                print('specific post--->', posts)


                # flash('WE HAVE PUBLISHED YOUR LOST ITEM', 'success')

                return render_template("reusable/others/post-section.html", posts = posts)



        if found_item_indicator :
            
            print("found form")

            if file and allowed_file(file.filename) and file.filename != '' and date and possession and venue :
                print("entered last block")
                split_file_name = os.path.splitext(file.filename)
                name_list = list(split_file_name)
                ex = str(file_ext(file.filename))
                secure = secure_filename(file.filename)

                #funtion to generate random name
                def random_name(filename):
                    random_hex = str(secrets.token_hex(8))
                #the return statement below returns a random name for each file with different parameters separated by underscores 
                    return   current_user.first_name + '_' + current_user.last_name + '_' + name_list[0] + '__' + random_hex + '__' + current_time() + '.' + ex


                #the name of the file gets assigned to the randomly generated file name 
                filename  = random_name(file.filename)
              
                uploads_path = os.path.join(current_app.root_path, 'static/post_IM', filename)

                print('uploaded file----->', uploads_path)

                #the next four lines just resizes the image to the given dimensions e.g 125 by 125
                output_size = (500,500)
                i = Image.open(file)
                i.thumbnail(output_size)
                i.save(uploads_path)

                #save the newly generated filename to the post database along with other form data
                

                formated_date = date[0:10] + " " + date[11:] 

                formated_date_as_datetime_object = datetime.strptime(formated_date, '%Y-%m-%d %H:%M')

                if possession == "Yes" :
                    possession = True

                elif possession == "No" :
                    possession = False

                post = Post(
                        image_file = filename,
                        content =  found_item_indicator, 
                        is_Lost_and_found =  True,
                        venue =  venue,
                        possession = possession,
                        date =  formated_date_as_datetime_object,
                        author = current_user

                        )


                print(filename,'\n',found_item_indicator,'\n',venue,'\n',date,'\n', "possession----",possession,"\n")

                db.session.add(post)
                db.session.commit()



                posts = Post.query.filter_by(author = current_user, image_file = filename).first()
                print('specific post--->', posts)


                # flash('THANKS FOR BEING A GOOD PERSON ! ', 'success')

                return render_template("reusable/others/post-section.html", posts = posts)



        if add_account_indicator :

            print("bank account form")

            if  bank and title :

                print (title,'\n',

                bank,'\n',

                add_account_indicator)


                if user_bank_accounts["account_numbers"][0]['bank_name'] == ' ':

                    print(user_bank_accounts["account_numbers"][0])
                    user_bank_accounts["account_numbers"][0]['bank_name'] = bank
                    user_bank_accounts["account_numbers"][0]['account_name'] = add_account_indicator
                    user_bank_accounts["account_numbers"][0]['account_number'] = title                


                print(user_bank_accounts["account_numbers"][0])


                current_user.account_numbers = json.dumps(user_bank_accounts)

                db.session.commit()
                

                return render_template("reusable/others/post-section.html", posts = posts)



        #print('after======\n',user_bank_accounts)
                



        if normal_post_indicator :

            # if the user just wants to post a text
            if not file:

                print('no file')

                file = "null"
                new_reference = random_reference_code()

                post = Post(
                        image_file = file,
                        content =  normal_post_indicator, 
                        is_event =  False,
                        author = current_user,
                        reference_code = new_reference
                        )

                db.session.add(post)
                db.session.commit()


                posts = Post.query.filter_by(author = current_user, image_file = file, reference_code = new_reference).limit(20)
                posts = list(posts) #its important to put it in a list
                print('specific post in list--->', posts )

                # --------------------------------------
                # --------------------------------------
                # EXTRACTING HASHTAGS FROM POSTS--------
                # --------------------------------------
                # --------------------------------------

                for hashtag in extract_hashtags(normal_post_indicator):
                    new_hashtag = Hashtag(
                        hashtag_name =  hashtag, 
                        author = current_user,
                        reference_code = new_reference
                        )
                    db.session.add(new_hashtag)
                    db.session.commit()


                    hashtag_exists = Hashtag_counter.query.filter_by(hashtag_name = hashtag).first()

                    if hashtag_exists == None:

                        new_hashtag_count = Hashtag_counter(
                            hashtag_name =  hashtag, 
                            author = current_user,
                            hashtag_mention_count = 1
                            )


                        db.session.add(new_hashtag)
                        db.session.commit()

                    elif hashtag_exists != None:
                        hashtag_exists.hashtag_mention_count += 1
                        db.session.commit()




                post_html = render_template("reusable/others/post-section.html", posts = posts)

                trending_hashtags = Hashtag_counter.query.order_by(Hashtag_counter.hashtag_mention_count.desc()).limit(10)

                hashtag_html = render_template("reusable/others/hashtag_html.html", trending_hashtags = trending_hashtags)

                emit('new_text_post', {'data': post_html, 'hashtag_html': hashtag_html, 'post_author': current_user.id},  namespace='/',broadcast=True)


                return render_template("reusable/others/post-section.html", posts = posts)





            # if the user wants to post a text and the image is not corect in format

            # check if the post request has the file part
            if not  allowed_file(file.filename):
                flash('Please use only png, jpg or gif images ', 'error')
                return render_template("reusable/others/post-section.html", posts = posts)


            # if the user wants to post a text and the image is valid
            # the following if block performs all the required processing on the file
            #and its name after validating its name


            if file and file.filename.rsplit('.', 1)[1].lower() == "gif" :

                split_file_name = os.path.splitext(file.filename)
                name_list = list(split_file_name)
                ex = str(file_ext(file.filename))
                secure = secure_filename(file.filename)

                #funtion to generate random name
                def random_name(filename):
                    random_hex = str(secrets.token_hex(8))
                #the return statement below returns a random name for each file with different parameters separated by underscores 
                    return   current_user.first_name + '_' + current_user.last_name + '_' + name_list[0] + '__' + random_hex + '__' + current_time() + '.' + ex


                #the name of the file gets assigned to the randomly generated file name 
                filename  = random_name(file.filename)
              
                uploads_path = os.path.join(current_app.root_path, 'static/post_IM', filename)

                print('uploaded gif file----->', uploads_path)

                file.save(uploads_path)

                #save the newly generated filename to the post database along with other form data
                

                post = Post(
                        image_file = filename,
                        content =  normal_post_indicator, 
                        is_event =  False,
                        author = current_user)


                db.session.add(post)
                db.session.commit()


                posts = Post.query.filter_by(author = current_user, image_file = file, reference_code = new_reference).limit(20)
                posts = list(posts) #its important to put it in a list
                print('specific post in list--->', posts )

                file = filename
                new_reference = random_reference_code()

                # --------------------------------------
                # --------------------------------------
                # EXTRACTING HASHTAGS FROM POSTS--------
                # --------------------------------------
                # --------------------------------------

                for hashtag in extract_hashtags(normal_post_indicator):
                    new_hashtag = Hashtag(
                        hashtag_name =  hashtag, 
                        author = current_user,
                        reference_code = new_reference
                        )
                    db.session.add(new_hashtag)
                    db.session.commit()


                    hashtag_exists = Hashtag_counter.query.filter_by(hashtag_name = hashtag).first()

                    if hashtag_exists == None:

                        new_hashtag_count = Hashtag_counter(
                            hashtag_name =  hashtag, 
                            author = current_user,
                            hashtag_mention_count = 1
                            )


                        db.session.add(new_hashtag)
                        db.session.commit()

                    elif hashtag_exists != None:
                        hashtag_exists.hashtag_mention_count += 1
                        db.session.commit()




                post_html = render_template("reusable/others/post-section.html", posts = posts)

                trending_hashtags = Hashtag_counter.query.order_by(Hashtag_counter.hashtag_mention_count.desc()).limit(10)

                hashtag_html = render_template("reusable/others/hashtag_html.html", trending_hashtags = trending_hashtags)

                emit('new_text_post', {'data': post_html, 'hashtag_html': hashtag_html, 'post_author': current_user.id},  namespace='/',broadcast=True)


                return render_template("reusable/others/post-section.html", posts = posts)





            if file and allowed_file(file.filename) and file.filename != '' :
                split_file_name = os.path.splitext(file.filename)
                name_list = list(split_file_name)
                ex = str(file_ext(file.filename))
                secure = secure_filename(file.filename)

                #funtion to generate random name
                def random_name(filename):
                    random_hex = str(secrets.token_hex(8))
                #the return statement below returns a random name for each file with different parameters separated by underscores 
                    return   current_user.first_name + '_' + current_user.last_name + '_' + name_list[0] + '__' + random_hex + '__' + current_time() + '.' + ex


                #the name of the file gets assigned to the randomly generated file name 
                filename  = random_name(file.filename)
              
                uploads_path = os.path.join(current_app.root_path, 'static/post_IM', filename)

                print('uploaded file----->', uploads_path)

                #the next four lines just resizes the image to the given dimensions e.g 125 by 125
                output_size = (500,500)
                i = Image.open(file)
                i.thumbnail(output_size)
                i.save(uploads_path)

                #save the newly generated filename to the post database along with other form data
                
                new_reference = random_reference_code()

                post = Post(
                        image_file = filename,
                        content =  normal_post_indicator, 
                        is_event =  False,
                        author = current_user,
                        reference_code = new_reference
                        )


                db.session.add(post)
                db.session.commit()



                posts = Post.query.filter_by(author = current_user, image_file = filename, reference_code = new_reference).first()
                print('specific post with image--->', posts)

                p = []

                p.append(posts)

                posts = p #its important to put it in a list

                print('p--->', posts)


                file = filename
                new_reference = random_reference_code()

                # --------------------------------------
                # --------------------------------------
                # EXTRACTING HASHTAGS FROM POSTS--------
                # --------------------------------------
                # --------------------------------------

                for hashtag in extract_hashtags(normal_post_indicator):
                    new_hashtag = Hashtag(
                        hashtag_name =  hashtag, 
                        author = current_user,
                        reference_code = new_reference
                        )
                    db.session.add(new_hashtag)
                    db.session.commit()


                    hashtag_exists = Hashtag_counter.query.filter_by(hashtag_name = hashtag).first()

                    if hashtag_exists == None:

                        new_hashtag_count = Hashtag_counter(
                            hashtag_name =  hashtag, 
                            author = current_user,
                            hashtag_mention_count = 1
                            )


                        db.session.add(new_hashtag)
                        db.session.commit()

                    elif hashtag_exists != None:
                        hashtag_exists.hashtag_mention_count += 1
                        db.session.commit()




                post_html = render_template("reusable/others/post-section.html", posts = posts)

                trending_hashtags = Hashtag_counter.query.order_by(Hashtag_counter.hashtag_mention_count.desc()).limit(10)

                hashtag_html = render_template("reusable/others/hashtag_html.html", trending_hashtags = trending_hashtags)

                emit('new_text_post', {'data': post_html, 'hashtag_html': hashtag_html, 'post_author': current_user.id},  namespace='/',broadcast=True)


                return render_template("reusable/others/post-section.html", posts = posts)




        elif normal_post_indicator == " " :
            flash(' you have to write something yo', 'error')
            return render_template("reusable/others/post-section.html", posts = posts)



    return render_template("reusable/others/post-section.html", posts = posts)



    
























    






@index_blueprint.route('/vip',methods=['GET'])  
def vip():
    return render_template("home/vip.html")



@index_blueprint.route('/what_more',methods=['GET'])  
def what_more():
    return render_template("home/what_more.html")





@index_blueprint.route('/accept_terms/<email>/<string:answer>',methods=['POST']) 
@login_required 
def terms(email,answer):
    user = User.query.filter_by(email = email).first_or_404()
    user.has_aceepted_terms_and_conditions = bool(answer)
    db.session.commit()
    
    return redirect(url_for('home.general'))






@index_blueprint.route('/feed',methods=['GET'])  
def feed():
    return render_template("home/feed-section.html")





@index_blueprint.route('/sections',methods=['POST'])  
def sections():
    query = request.get_json() or {}

    try:
        action_type = query['action_type']

        print('\n', json.dumps(query) )
        
    except KeyError:
        pass

    # if request.method == 'POST' and post_type == 'Lost Items' :

    return render_template("home/feed-section.html")




@index_blueprint.route('/phone_visibility',methods=['POST']) 
@login_required 
def phone_visibility():

    query = request.get_json() or {}

    # print('\n', json.dumps(query) )

    try:
        user_id = query['user_id']

        phone_visibility = query['phone_visibility']

        # print('\n', json.dumps(query) )

        # print('\n', phone_visibility )
        
    except KeyError:
        pass

    info = 'nothing'

    user = User.query.get_or_404(user_id)


    if phone_visibility and phone_visibility == 'True':
        user.allows_phone_number_to_be_seen = True
        db.session.commit()
        info = ' Your number is now visible to everyone '

    elif phone_visibility and phone_visibility == 'False':
       
        info = ' Only you can see your number from now on'
        user.allows_phone_number_to_be_seen = False
        db.session.commit()

        
    return render_template("home/information.html",info = info )







@index_blueprint.route('edit-profile/email_visibility',methods=['POST']) 
@login_required 
def email_visibility():

    query = request.get_json() or {}

    # print('\n', json.dumps(query) )

    try:
        user_id = int(query['user_id'])

        email_visibility = query['email_visibility']

        # print('\n', json.dumps(query) )

        # print('\n', email )
        
    except KeyError:
        pass

    user = User.query.get_or_404(user_id)

    if email_visibility == 'visible':
        user.allows_email_to_be_seen = True
        db.session.commit()

    elif email_visibility == 'invisible':
        # print('second block entered')
        user.allows_email_to_be_seen = False
        db.session.commit()
        
    return render_template("home/visibility.html")











@index_blueprint.route('/settings',methods=['GET','POST'])
@login_required
def settings():

    return render_template("home/settings.html")
    




@index_blueprint.route('/_settings',methods=['GET','POST'])
@login_required
def _settings():

    return render_template("home/_settings.html")
    






@index_blueprint.route('/transactions',methods=['GET','POST'])
@login_required
def transactions():

    return render_template("home/transactions.html")
    



@index_blueprint.route('/_transactions',methods=['GET','POST'])
@login_required
def _transactions():

    return render_template("home/_transactions.html")
    










@index_blueprint.route('/premium',methods=['GET','POST'])
@login_required
def premium():

    views_count = current_user.payment_intro_viewed_count 

    if views_count == None:
        current_user.payment_intro_viewed_count = 1
        db.session.commit()

        print('past comit', views_count)

    if views_count != 0:
        current_user.payment_intro_viewed_count += 1
        db.session.commit()

        print('past comit', views_count)


    return render_template("home/premium.html")
    













@index_blueprint.route('/list_stuff/<stuff>',methods=['GET','POST'])
@login_required
def list_stuff(stuff):

    saved_posts = []
    saved_roomies = []
    items = []
    title = ' '
    sort = ' '


    if stuff == 'followers':
        sort = 'followers'
        items = current_user.followers.all()
        title = 'Followers'

    if stuff == 'roomates':
        sort = 'roomates'
        items = current_user.followers.all()
        title = 'Roomates'


    if stuff == 'saved':
        
        sort = 'saved'

        items = current_user.saved_items.all()

        #print(items)

        saved_posts = current_user.saved_items.filter_by(description = "saving a post" ).limit(5)

        #print('posts--->', saved_posts.all())

        saved_roomies = current_user.saved_items.filter_by(description = "saving a roomie" ).limit(5)
        
        #print('roomies--->',  saved_roomies)

        title = 'Saved'

        #print(current_user)


    return render_template("home/list_stuff.html",saved_posts = saved_posts,  saved_roomies = saved_roomies,  items = items , title = title, sort = sort )
    








#################################
#### USER AND PROFILE ROUTES ####
#################################


@index_blueprint.route('/user/<email>',methods=['GET'])
def user(email):
    user = User.query.filter_by(email = email).first_or_404()
    p = user.image_file
    img = url_for('static', filename = 'profile_pics/uploads/{}'.format(p))
    return render_template("home/user-template.html", user = user, img = img)













@index_blueprint.route('/profile/<id>',methods=['GET','POST'])
@login_required
def profile(id):

    user = User.query.get_or_404(id)

    p = user.image_file

    img = url_for('static', filename = 'profile_pics/uploads/{}'.format(p))
    
    form = ProfileForm(CombinedMultiDict((request.files, request.form)))



    return render_template("home/profile.html", 

        user=user, 
        img = img, form = form,
        genders = genders, 
        banks = banks, 
        star_signs = star_signs, 
        price_range = price_range, 
        relationships = relationships, 
        levels = levels, 
        departments = departments,
        locations = locations,
        religions = religions

      )
    






@index_blueprint.route('/_profile',methods=['POST'])
@login_required
def _profile():

    query = request.get_json() or {}

    print('\n', json.dumps(query) )

    try:

        _id = int(query['user'])

    except KeyError:
        pass

    user = User.query.get_or_404(_id)

    p = user.image_file

    img = url_for('static', filename = 'profile_pics/uploads/{}'.format(p))
    
    form = ProfileForm(CombinedMultiDict((request.files, request.form)))



    return render_template("home/_profile.html", 

        user=user, 
        img = img, form = form,
        genders = genders, 
        banks = banks, 
        star_signs = star_signs, 
        price_range = price_range, 
        relationships = relationships, 
        levels = levels, 
        departments = departments,
        locations = locations,
        religions = religions

      )
    













@index_blueprint.route('edit_user_profile',methods=['POST']) 
@login_required 
def edit_user_profile():

 
    query = request.get_json() or {}

    print('\n', json.dumps(query) )

    try:

        data = query['data'].strip()

        command = query['command'].strip()

        user = int(query['user'])

    except KeyError:
        pass

    user = User.query.get_or_404(user)


    if user != current_user :

        return jsonify(response = 'you are only allowed to edit your own account')



    if command == 'submit_more_about' :

        user.more_about = str(data)

        db.session.commit()



    if command == 'submit_gender' :

        user.gender = str(data)

        db.session.commit()


    if command == 'submit_religion' :

        user.religion = str(data)
        
        db.session.commit()



    if command == 'submit_address' :

        user.address = str(data)
        
        db.session.commit()


    if command == 'submit_budget' :

        user.budget = str(data)
        
        db.session.commit()


    if command == 'submit_likes' :

        user.likes = str(data)
        
        db.session.commit()


    if command == 'submit_dislikes' :

        user.dislikes = str(data)
        
        db.session.commit()



    if command == 'submit_birthday' :

        formated_date_as_datetime_object = date.fromisoformat(data)

        print(formated_date_as_datetime_object)

        user.birth_day = formated_date_as_datetime_object

        user.has_updated_age_first_time == True

        db.session.commit()

        # ARIES (mar 21 - april 19)
        if formated_date_as_datetime_object.month == 3 and formated_date_as_datetime_object.day in range(21, 32):
            user.star_sign = '♈ aries'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 4 and formated_date_as_datetime_object.day in range(1, 20):
            user.star_sign = '♈ aries'
            db.session.commit()



        # TAURUS (apr 20 - may 20)
        if formated_date_as_datetime_object.month == 4 and formated_date_as_datetime_object.day in range(20, 31):
            user.star_sign = ' ♉ taurus'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 5 and formated_date_as_datetime_object.day in range(1, 21):
            user.star_sign = ' ♉ taurus'
            db.session.commit()



        # gemini (may 21 - jun 21)
        if formated_date_as_datetime_object.month == 5 and formated_date_as_datetime_object.day in range(21, 32):
            user.star_sign = ' ♊ gemini'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 6 and formated_date_as_datetime_object.day in range(1, 22):
            user.star_sign = ' ♊ gemini'
            db.session.commit()



        # cancer (june 22 - july 22)
        if formated_date_as_datetime_object.month == 6 and formated_date_as_datetime_object.day in range(22, 31):
            user.star_sign = ' ♋ cancer'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 7 and formated_date_as_datetime_object.day in range(1, 23):
            user.star_sign = ' ♋ cancer'
            db.session.commit()



        # leo (jul 23 - aug 22)
        if formated_date_as_datetime_object.month == 7 and formated_date_as_datetime_object.day in range(23, 32):
            user.star_sign = ' ♌ leo'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 8 and formated_date_as_datetime_object.day in range(1, 23):
            user.star_sign = ' ♌ leo'
            db.session.commit()



        # virgo (aug 23 - sep 22 )
        if formated_date_as_datetime_object.month == 8 and formated_date_as_datetime_object.day in range(23, 32):
            user.star_sign = ' ♍ virgo'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 9 and formated_date_as_datetime_object.day in range(1, 23):
            user.star_sign = ' ♍ virgo'
            db.session.commit()




        # libra (sep 23 - october 23 )
        if formated_date_as_datetime_object.month == 9 and formated_date_as_datetime_object.day in range(23, 31):
            user.star_sign = ' ♎ libra'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 10 and formated_date_as_datetime_object.day in range(1, 24):
            user.star_sign = ' ♎ libra'
            db.session.commit()



        # SCORPIO(oct 24 - nov 21)
        if formated_date_as_datetime_object.month == 10 and formated_date_as_datetime_object.day in range(24, 32):
            user.star_sign = ' ♏ scorpio'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 11 and formated_date_as_datetime_object.day in range(1, 22):
            user.star_sign = ' ♏ scorpio'
            db.session.commit()




        # sagittarius (nov 22 - dec 21)
        if formated_date_as_datetime_object.month == 11 and formated_date_as_datetime_object.day in range(22, 31):
            user.star_sign = ' ♐ sagittarius'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 12 and formated_date_as_datetime_object.day in range(1, 22):
            user.star_sign = ' ♐ sagittarius'
            db.session.commit()



        # capricorn (dec 22 - jan 19)
        if formated_date_as_datetime_object.month == 12 and formated_date_as_datetime_object.day in range(22, 31):
            user.star_sign = ' ♑ capricorn'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 1 and formated_date_as_datetime_object.day in range(1, 20):
            user.star_sign = ' ♑ capricorn'
            db.session.commit()



        # AQUARIUS (jan 20 - feb 18)
        if formated_date_as_datetime_object.month == 1 and formated_date_as_datetime_object.day in range(20, 32):
            user.star_sign = ' ♒ aquarius'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 2 and formated_date_as_datetime_object.day in range(0, 19):
            user.star_sign = ' ♒ aquarius'
            db.session.commit()



        # PISCES  (feb 19 - mar 20)
        if formated_date_as_datetime_object.month == 2 and formated_date_as_datetime_object.day in range(19, 30):
            user.star_sign = ' ♓ pisces'
            db.session.commit()

        elif formated_date_as_datetime_object.month == 3 and formated_date_as_datetime_object.day in range(0, 21):
            user.star_sign = ' ♓ pisces'
            db.session.commit()

        data = formated_date_as_datetime_object


        birth_day = render_template("home/practise.html", data = user.birth_day.strftime("%b %d"))

        star_sign = render_template("home/practise.html", data = user.star_sign)

        if user.has_updated_age_first_time == True:
            abort(403)

        else:

            return jsonify(

                birth_day = birth_day,
                star_sign = star_sign

                )



    if command == 'submit_department' :

        user.department = str(data)
        
        db.session.commit()



    if command == 'submit_level' :

        user.level = str(data)
        
        db.session.commit()



    if command == 'submit_relationship' :

        user.relationship_status = str(data)
        
        db.session.commit()



        
    return render_template("home/practise.html", data = data)


























@index_blueprint.route('/update_profile_pic/<int:id>',methods=['GET','POST'])
@login_required
def update_profile_pic(id):
    count = request.args.get('count')


    user = User.query.get_or_404(id)

    if user != current_user:
        abort(403)


    photoForm = PhotoForm(CombinedMultiDict((request.files, request.form)))

    # logic for pic upload fields
    if  request.method == 'POST' and photoForm.validate() :
    # logic for uploading profile pic only
    #the request.files object intance using flaskform
        file = photoForm.photo.data
     
        #generate random string 8 digits long
        random_hex = secrets.token_hex(5)


        # check if the post request has the file part
        if not file:
            flash('NO PHOTO CHOSEN', 'error')
            return redirect(request.url)

        # check if the post request has the file part
        elif not  allowed_file(file.filename):
            flash('THE SELECTED FILE TYPE IS NOT ALLOWED, USE png OR jpg FILES ONLY', 'error')
            return redirect(request.url)

     
        # the following if block performs all the required processing on the file
        #and its name after validating its name

        if file and allowed_file(file.filename) and file.filename != '':
            split_file_name = os.path.splitext(file.filename)
            name_list = list(split_file_name)
            ex = str(file_ext(file.filename))
            secure = secure_filename(file.filename)

            #funtion to generate random name
            def random_name(filename):
                random_hex = str(secrets.token_hex(8))
            #the return statement below returns a random name for each file with different parameters separated by underscores 
                return   current_user.first_name + '_' + current_user.last_name + '_' + name_list[0] + '__' + random_hex + '__' + current_time() + '.' + ex


            #the name of the file gets assigned to the randomly generated file name 
            filename  = random_name(file.filename)
          
            uploads_path = os.path.join(current_app.root_path, 'static/profile_pics/uploads', filename)

            #the next four lines just resizes the image to the given dimensions e.g 125 by 125
            output_size = (250,250)
            i = Image.open(file)
            i.thumbnail(output_size)
            i.save(uploads_path)

            #save the newly generated filename to the user database along with other form data
            

            user.image_file = filename
            db.session.commit()

            return redirect(request.url)

    elif request.method == 'GET':
        photoForm.photo.data = user.image_file



    p = user.image_file
    img = url_for('static', filename = 'profile_pics/uploads/{}'.format(p))



    # return redirect(

    #     status='success',
    #     image_url = img

    #     )



    return redirect(url_for('home.profile', id = user.id))












@index_blueprint.route('/update_profile_picture',methods=['GET','POST'])
@login_required
def update_profile_picture( ):


    form = PostForm(CombinedMultiDict((request.files, request.form)))


    # logic for pic upload fields
    if  request.method == 'POST' :
    # logic for uploading profile pic only
    #the request.files object intance using flaskform
        file = form.photo.data

        # file = request.files['photo']
     
        #generate random string 8 digits long
        random_hex = secrets.token_hex(5)

        # check if the post request has the file part
        if not file:
            flash('NO PHOTO CHOSEN', 'error')
            return redirect(request.url)

        # check if the post request has the file part
        elif not  allowed_file(file.filename):
            flash('THE SELECTED FILE TYPE IS NOT ALLOWED, USE png OR jpg FILES ONLY', 'error')
            return redirect(request.url)
     
        # the following if block performs all the required processing on the file
        #and its name after validating its name
        if file and allowed_file(file.filename) and file.filename != '':
            split_file_name = os.path.splitext(file.filename)
            name_list = list(split_file_name)
            ex = str(file_ext(file.filename))
            secure = secure_filename(file.filename)

            #funtion to generate random name
            def random_name(filename):
                random_hex = str(secrets.token_hex(8))
            #the return statement below returns a random name for each file with different parameters separated by underscores 
                return   current_user.first_name + '_' + current_user.last_name + '_' + name_list[0] + '__' + random_hex + '__' + current_time() + '.' + ex


            #the name of the file gets assigned to the randomly generated file name 
            filename  = random_name(file.filename)
          
            uploads_path = os.path.join(current_app.root_path, 'static/profile_pics/uploads', filename)

            #the next four lines just resizes the image to the given dimensions e.g 125 by 125
            output_size = (250,250)
            i = Image.open(file)
            i.thumbnail(output_size)
            i.save(uploads_path)

            #save the newly generated filename to the user database along with other form data
            

            current_user.image_file = filename
            db.session.commit()

            return redirect(request.url)







    return jsonify({'result_image_location': url_for('static', filename = 'profile_pics/uploads/{}'.format(current_user.image_file)) })







































@index_blueprint.route('/edit-profile/<id>', methods=['POST','GET'])
@login_required
def edit_profile(id):
 

    form = ProfileForm(CombinedMultiDict((request.files, request.form)))

    user = User.query.get_or_404(id)


    if user != current_user:
        abort(403)

    if  request.method == 'POST' and form.validate() :

        file = form.photo.data
        venue =  form.venue.data.lower().lstrip()
        title =  form.title.data.lower().lstrip()
        content =  form.content.data.lower().lstrip()
        price =  form.price.data
        budget =  form.budget.data

        roomie_info_indicator =  form.roomie_info_indicator.data.lower().lstrip()
        update_basic_info_indicator =  form.update_basic_info_indicator.data.lower().lstrip()
        gender = form.gender.data
        religion = form.religion.data

        department = form.department.data
        level = form.level.data
        relationship_status = form.relationship_status.data
        needs_roomate = form.needs_roomate.data

        date = request.form.get('datepicker')

        update_other_info_form = request.form.get('update_other_info_form')

        date_range_start = request.form.get('datepicker_start')

        date_range_stop = request.form.get('datepicker_end')
     

        #generate random string 8 digits long
        random_hex = secrets.token_hex(5)

       # print(date, venue, title, content)


        if update_basic_info_indicator :

            print("basic info form")

            print(update_basic_info_indicator,'\n\n', gender,'\n\n', religion,'\n\n', title,'\n\n', title)

            user.more_about = update_basic_info_indicator
            db.session.commit()

            if gender:
                user.gender = gender
                db.session.commit()

            if religion:
                user.religion = religion
                db.session.commit()

            if title:
                user.address = title
                db.session.commit()

            if needs_roomate:
                if needs_roomate == "YES":
                    user.seeks_roomate = True

                elif needs_roomate == "NO":
                    user.seeks_roomate = False

                db.session.commit()


            flash('CHANGES SAVED', 'success')

            return redirect(request.url)





        if roomie_info_indicator :

            print("roomie info form")

            print(roomie_info_indicator,'\n\n', content,'\n\n', budget,'\n\n')

            user.likes = roomie_info_indicator
            db.session.commit()


            if content:
                user.dislikes = content
                db.session.commit()

            if budget:
                user.budget = budget
                db.session.commit()


            flash('CHANGES SAVED', 'success')

            return redirect(request.url)




        if update_other_info_form :

            print("other info form")

            print(update_other_info_form,'\n\n', department,'\n\n', level,'\n\n', relationship_status,'\n\n', relationship_status)

            formated_date = update_other_info_form[0:10] 

            formated_date_as_datetime_object = datetime.strptime(formated_date, '%Y-%m-%d')

            print("formated date -->", formated_date)

            print(" datetime version-->", datetime.strptime(formated_date, '%Y-%m-%d'))



            user.birth_day = formated_date_as_datetime_object
            db.session.commit()


            if formated_date_as_datetime_object :

                print('date gotten' )



                # ARIES (mar 21 - april 19)
                if formated_date_as_datetime_object.month == 3 and formated_date_as_datetime_object.day in range(21, 32):
                    user.star_sign = '♈ aries'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 4 and formated_date_as_datetime_object.day in range(1, 20):
                    user.star_sign = '♈ aries'
                    db.session.commit()



                # TAURUS (apr 20 - may 20)
                if formated_date_as_datetime_object.month == 4 and formated_date_as_datetime_object.day in range(20, 31):
                    user.star_sign = ' ♉ taurus'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 5 and formated_date_as_datetime_object.day in range(1, 21):
                    user.star_sign = ' ♉ taurus'
                    db.session.commit()



                # gemini (may 21 - jun 21)
                if formated_date_as_datetime_object.month == 5 and formated_date_as_datetime_object.day in range(21, 32):
                    user.star_sign = ' ♊ gemini'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 6 and formated_date_as_datetime_object.day in range(1, 22):
                    user.star_sign = ' ♊ gemini'
                    db.session.commit()



                # cancer (june 22 - july 22)
                if formated_date_as_datetime_object.month == 6 and formated_date_as_datetime_object.day in range(22, 31):
                    user.star_sign = ' ♋ cancer'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 7 and formated_date_as_datetime_object.day in range(1, 23):
                    user.star_sign = ' ♋ cancer'
                    db.session.commit()



                # leo (jul 23 - aug 22)
                if formated_date_as_datetime_object.month == 7 and formated_date_as_datetime_object.day in range(23, 32):
                    user.star_sign = ' ♌ leo'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 8 and formated_date_as_datetime_object.day in range(1, 23):
                    user.star_sign = ' ♌ leo'
                    db.session.commit()



                # virgo (aug 23 - sep 22 )
                if formated_date_as_datetime_object.month == 8 and formated_date_as_datetime_object.day in range(23, 32):
                    user.star_sign = ' ♍ virgo'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 9 and formated_date_as_datetime_object.day in range(1, 23):
                    user.star_sign = ' ♍ virgo'
                    db.session.commit()




                # libra (sep 23 - october 23 )
                if formated_date_as_datetime_object.month == 9 and formated_date_as_datetime_object.day in range(23, 31):
                    user.star_sign = ' ♎ libra'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 10 and formated_date_as_datetime_object.day in range(1, 24):
                    user.star_sign = ' ♎ libra'
                    db.session.commit()



                # SCORPIO(oct 24 - nov 21)
                if formated_date_as_datetime_object.month == 10 and formated_date_as_datetime_object.day in range(24, 32):
                    user.star_sign = ' ♏ scorpio'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 11 and formated_date_as_datetime_object.day in range(1, 22):
                    user.star_sign = ' ♏ scorpio'
                    db.session.commit()




                # sagittarius (nov 22 - dec 21)
                if formated_date_as_datetime_object.month == 11 and formated_date_as_datetime_object.day in range(22, 31):
                    user.star_sign = ' ♐ sagittarius'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 12 and formated_date_as_datetime_object.day in range(1, 22):
                    user.star_sign = ' ♐ sagittarius'
                    db.session.commit()



                # capricorn (dec 22 - jan 19)
                if formated_date_as_datetime_object.month == 12 and formated_date_as_datetime_object.day in range(22, 31):
                    user.star_sign = ' ♑ capricorn'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 1 and formated_date_as_datetime_object.day in range(1, 20):
                    user.star_sign = ' ♑ capricorn'
                    db.session.commit()



                # AQUARIUS (jan 20 - feb 18)
                if formated_date_as_datetime_object.month == 1 and formated_date_as_datetime_object.day in range(20, 32):
                    user.star_sign = ' ♒ aquarius'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 2 and formated_date_as_datetime_object.day in range(0, 19):
                    user.star_sign = ' ♒ aquarius'
                    db.session.commit()



                # PISCES  (feb 19 - mar 20)
                if formated_date_as_datetime_object.month == 2 and formated_date_as_datetime_object.day in range(19, 30):
                    user.star_sign = ' ♓ pisces'
                    db.session.commit()

                elif formated_date_as_datetime_object.month == 3 and formated_date_as_datetime_object.day in range(0, 21):
                    user.star_sign = ' ♓ pisces'
                    db.session.commit()





            if user.birth_day:
                print(user.birth_day.month, user.birth_day.day )


            if department:
                user.department = department
                db.session.commit()

            if level:
                user.level = level
                db.session.commit()

            if relationship_status:
                user.relationship_status = relationship_status
                db.session.commit()


            flash('CHANGES SAVED', 'success')

            return redirect(request.url)




    # print("returning")
    return redirect(url_for('home.profile', id=user.id))















@index_blueprint.route('/get_forms', methods=[ 'POST'])
@login_required  
def get_forms():

    beginning_of_year = str(datetime.utcnow().year) + "-" +  "01" + "-" + "01"

    beginning_of_next_year = str(datetime.utcnow().year + 1) + "-" +  "01" + "-" + "01"

    ten_years_back = str(datetime.utcnow().year - 10) + "-" +  "01" + "-" + "01"



    query = request.get_json() or {}

    print("recieved json data",  query)

    try:

        command = query['command']

        user = query['user']

    except KeyError:
        pass


    form = ProfileForm(CombinedMultiDict((request.files, request.form)))

    
    user_bank_accounts = json.loads(current_user.account_numbers)

    if command == "other":

        return render_template("home/other-info-form.html", form = form, user = user, beginning_of_next_year = beginning_of_next_year, beginning_of_year = beginning_of_year, ten_years_back = ten_years_back)


    if command == "roomie":

        return render_template("home/roomie-form.html", form = form, user = user  )


    if command == "normal":

        return render_template("home/basic-form.html", form = form, user = user )


    if command == "lost":

        return render_template("home/lost-item-form.html", form = form )


    if command == "found":

        return render_template("home/found-item-form.html", form = form )








@index_blueprint.route('/view-profile-pic/<int:id>',methods=['GET','POST'])
@login_required
def view_profile(id):
    count = request.args.get('count')

    # print(count)

    p = current_user.image_file
    img = url_for('static', filename = 'profile_pics/uploads/{}'.format(p))
    user = User.query.get_or_404(id)


    if user != current_user:
        abort(403)


    photoForm = PhotoForm(CombinedMultiDict((request.files, request.form)))

    # logic for pic upload fields
    if  request.method == 'POST' and photoForm.validate() :
    # logic for uploading profile pic only
    #the request.files object intance using flaskform
        file = photoForm.photo.data
     
        #generate random string 8 digits long
        random_hex = secrets.token_hex(5)


        # check if the post request has the file part
        if not file:
            flash('NO PHOTO CHOSEN', 'error')
            return redirect(request.url)

        # check if the post request has the file part
        elif not  allowed_file(file.filename):
            flash('THE SELECTED FILE TYPE IS NOT ALLOWED, USE png OR jpg FILES ONLY', 'error')
            return redirect(request.url)

     
        # the following if block performs all the required processing on the file
        #and its name after validating its name

        if file and allowed_file(file.filename) and file.filename != '':
            split_file_name = os.path.splitext(file.filename)
            name_list = list(split_file_name)
            ex = str(file_ext(file.filename))
            secure = secure_filename(file.filename)

            #funtion to generate random name
            def random_name(filename):
                random_hex = str(secrets.token_hex(8))
            #the return statement below returns a random name for each file with different parameters separated by underscores 
                return   current_user.first_name + '_' + current_user.last_name + '_' + name_list[0] + '__' + random_hex + '__' + current_time() + '.' + ex


            #the name of the file gets assigned to the randomly generated file name 
            filename  = random_name(file.filename)
          
            uploads_path = os.path.join(current_app.root_path, 'static/profile_pics/uploads', filename)

            #the next four lines just resizes the image to the given dimensions e.g 125 by 125
            output_size = (250,250)
            i = Image.open(file)
            i.thumbnail(output_size)
            i.save(uploads_path)

            #save the newly generated filename to the user database along with other form data
            

            user.image_file = filename
            db.session.commit()


            flash('POST PHOTO UPDATED', 'success')
            return redirect(request.url)

    elif request.method == 'GET':
        photoForm.photo.data = user.image_file




    pic_list = []
    for i in range(2, 11):
        pic_list.append(str(i))




    
    return render_template("home/view-profile.html", user=user, img = img, photoForm = photoForm, pic_list = pic_list, count = count )
















@index_blueprint.route('/view-profile-pic/load_more_avatars',methods=['GET','POST'])
@login_required
def load_more_avatars():

    query = request.get_json() or {}

    try:
        count = int(query['count'])

        # print('\n', json.dumps(query) )
        
    except KeyError:
        pass


    pic_list = []

    for i in range(2, int(count + 10) ):
        pic_list.append(str(i))




# when its at 40 display only the remaining two
    if count == 40:

        pic_list = []

        for i in range(2, int(count + 2) ):
            pic_list.append(str(i))

        count = int(count) + 2




    else:
        count = int(count) + 10

    
    return render_template("home/view-profile-avatar-section.html", pic_list = pic_list, count = count )









# @index_blueprint.route('/edit-profile/<id>', methods=['GET', 'POST'])
# @login_required
# def edit_profile(id):
#     Caption = CaptionForm(request.form)
#     moreAbout = MoreAboutForm(request.form)
#     birthDay = BirthDayForm(request.form)
#     likesform = LikesForm(request.form)
#     dislikesform = DislikesForm(request.form)
#     phoneform = PhoneForm(request.form)


#     user = User.query.filter_by(id = id).first_or_404()

# # logic for caption field only
#     if request.method == 'POST' and Caption.validate() :
#         user.caption = Caption.caption.data.lower()
#         db.session.commit()
#         flash('SUCESSFULLY UPDATED  YOUR CAPTION', 'success')
#         return redirect(request.url)

# # logic for moreAbout field only
#     if request.method == 'POST' and moreAbout.validate() :
#         user.more_about = moreAbout.more_about.data.lower()
#         db.session.commit()
#         flash('SUCESSFULLY UPDATED MORE ABOUT SECTION', 'success')
#         return redirect(request.url)

# # logic for birthDay field only
#     if request.method == 'POST' and birthDay.validate() :
#         day = str(birthDay.day.data)
#         month = str(birthDay.month.data)
#         year =  str(birthDay.year.data)

#         user.birth_day = day + ' ' + month + ' ' + year


#         db.session.commit()
#         flash('SUCESSFULLY UPDATED YOUR BIRTHDAY ', 'success')
#         return redirect(url_for('home.edit_profile', email = current_user.email))


# # logic for likes field only        
#     if request.method == 'POST' and likesform.validate() :
#         user = User.query.filter_by(email = email).first_or_404()
#         user.likes = likesform.likes.data.lower()
#         db.session.commit()
#         flash('SUCESSFULLY UPDATED YOUR LIKES ', 'success')
#         return redirect(url_for('home.edit_profile', email = current_user.email))

# # logic for dislikes field only
#     if request.method == 'POST' and dislikesform.validate() :
#         user = User.query.filter_by(email = email).first_or_404()
#         user.dislikes = dislikesform.dislikes.data.lower()
#         db.session.commit()
#         flash('SUCESSFULLY UPDATED YOUR DISLIKES', 'success')
#         return redirect(url_for('home.edit_profile', email = current_user.email))


# # logic for phonenumber field only
#     if request.method == 'POST' and phoneform.validate() :
#         user = User.query.filter_by(email = email).first_or_404()
#         user.phone = phoneform.phone.data
#         db.session.commit()
#         flash('SUCESSFULLY UPDATED YOUR PHONENUMBER', 'success')
#         return redirect(url_for('home.edit_profile', email = current_user.email))


        
#     return render_template('home/edit_profile.html', moreAbout = moreAbout, birthDay = birthDay, likesform = likesform, dislikesform = dislikesform, Caption = Caption, phoneform = phoneform )










@index_blueprint.route('/set-avatar/<id>/<img>', methods=['GET', 'POST'])
@login_required
def set_avatar(id,img):
    user = User.query.get_or_404(id)
    user.image_file = img
    db.session.commit()
    flash('AVATAR UPDATED SUCESSFULLY', 'success')   
    return redirect(url_for('home.profile', id = current_user.id))



#############
#############
#### END ####
#############
#############
















@index_blueprint.route('/light-IM',methods=['GET'])
@login_required  
def light():
    return render_template("home/light-IM.html")



                 


@index_blueprint.route('/buy-IM',methods=['GET'])
@login_required  
def buy():
    return render_template("home/buy-IM.html")





@index_blueprint.route('/recharge-and-bills',methods=['GET'])
@login_required  
def recharge():
    return render_template("home/recharge-and-bills.html")
 




@index_blueprint.route('/rent-IM',methods=['GET'])
@login_required  
def rent():
    return render_template("home/rent-IM.html")























###########################
#### POST IM ROUTES ####
###########################


@index_blueprint.route('/post-IM',methods=['GET'])
@login_required  
def post_IM():
    return render_template("home/post-IM.html")





#############
#############
#### END ####
#############
#############






















#############################
#### ROOMIE IM ROUTES ####
#############################


@index_blueprint.route('/roomie-IM',methods=['GET'])
@login_required  
def roomie():
    return render_template("home/roomie-IM.html")





#############
#############
#### END ####
#############
#############






