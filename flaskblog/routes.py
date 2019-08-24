from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
							PostForm, CampaignForm, BannerForm)
from flaskblog.models import User, Post, Campaign, Banner
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from datetime import datetime
from datetime import date
from yattag import Doc
import shutil

# @app.route("/")
@app.route("/home")
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)

	return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')		
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
	''' 
	 данная функция сохраняет аватарку пользователя в файловую систему
	 в random_hex записываем случайное значение, которое будем использовать
	 в качестве имени файла
	 с помощью os.path.splitext получаем название загружаемого файла и 
	 его расширение
	 в picture_fn пишем название файла, который будем сохранять
	 в picture_path  пишем путь по которому будем сохранять файл с новым названием
	 app.root_path- полный пусть до package directory
	'''
	random_hex = secrets.token_hex(8) 
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

	# минимизируем аватарку и сохраняем
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():	
	form = UpdateAccountForm()
	if form.validate_on_submit():
		# если загрузили файл для аватарки,то сохраняем его в файловую систему
		# и затем показываем на странице с информацией о аккаунте, вместо default.jpg
		if form.picture.data: 
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('account'))
		# если это GET-запрос, то  в полях формы 
		#указываем значения из БД, чтобы не было пустых полей
	elif request.method == 'GET': 	
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', 
							image_file=image_file, form=form)

def save_post_picture(form_image):
	random_hex = secrets.token_hex(8) 
	f_name, f_ext = os.path.splitext(form_image.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/posts_pics', picture_fn)
	form_image.save(picture_path)

	return picture_fn

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():	
	form = PostForm()
	if form.validate_on_submit():
		if form.image.data:
			picture_file = save_post_picture(form.image.data)
			post = Post(title=form.title.data, content=form.content.data, 
					author=current_user, image_file=picture_file)
			db.session.add(post)
			db.session.commit()
			flash('Your post has been created!', 'success')
			return redirect(url_for('home'))
		else:
			post = Post(title=form.title.data, content=form.content.data, 
					author=current_user)
			db.session.add(post)
			db.session.commit()
			flash('Your post has been created!', 'success')
			return redirect(url_for('home'))
	
	return render_template('create_post.html', title='New Post', form=form, 
							legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update",  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()	
	if form.validate_on_submit():
		if form.image.data:
			picture_file = save_post_picture(form.image.data)
		post.title = form.title.data
		post.content = form.content.data
		post.image_file = picture_file
		db.session.commit()
		flash('Your post has been updated', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post',
							form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete",  methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted', 'success')
	return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).\
						order_by(Post.date_posted.desc())\
						.paginate(per_page=5, page=page)

	return render_template('user_posts.html', posts=posts, user=user)

#создаем директорию для хранения креативов баннеров конкретной кампании
# campaign_hash - название папки
def create_folder(campaign_hash):	
	path = os.path.join(app.root_path, 'static/campaigns',campaign_hash)
	if not os.path.exists(path):
		os.makedirs(path)	


@app.route("/campaign/new", methods=['GET','POST'])
@login_required
def new_campaign():
	form = CampaignForm()
	if form.validate_on_submit():
		
		campaign_hash = secrets.token_hex(8)
		campaign = Campaign(title=form.title.data, author=current_user, 
							start_date=form.start_date.data, 
							finish_date=form.finish_date.data, 
							campaign_hash=campaign_hash)
		db.session.add(campaign)
		db.session.commit()
		flash('Your campaign has been created', 'success')		
		create_folder(campaign_hash)
		return redirect(url_for('campaigns'))
	return render_template('create_campaign.html', title='New Campaign', form=form, 
							legend='New Campaign')
@app.route("/")
@app.route("/campaigns")
def campaigns():
	page = request.args.get('page', 1, type=int)
	campaigns = Campaign.query.order_by(Campaign.finish_date.desc())
	return render_template('campaigns.html', campaigns=campaigns)

@app.route("/campaign/<int:campaign_id>")
def campaign(campaign_id):
	campaign = Campaign.query.get_or_404(campaign_id)
	banners = Banner.query.filter_by(campaign_id=campaign_id).all()
	
	return render_template('campaign.html', title=campaign.title, 
		campaign=campaign, banners=banners)

@app.route("/campaign/<int:campaign_id>/update", methods=['GET', 'POST'])
@login_required
def update_campaign(campaign_id): 
	campaign = Campaign.query.get_or_404(campaign_id)
	if campaign.author != current_user:
		abort(403)
	form = CampaignForm()
	if form.validate_on_submit():
		campaign.title = form.title.data
		campaign.start_date = form.start_date.data
		campaign.finish_date = form.finish_date.data
		db.session.commit()
		flash('Your campaign has been updated', 'success')
		return redirect(url_for('campaigns'))
	elif request.method == 'GET':
		form.title.data = campaign.title
		form.start_date.data = campaign.start_date	
		form.finish_date.data = campaign.finish_date
		return render_template('create_campaign.html', title='Update Campaign',
							form=form, legend='Update Campaign')

def delete_campaign_folder(campaign_hash):
	path = os.path.join(app.root_path, 'static/campaigns',campaign_hash)
	shutil.rmtree(path, ignore_errors=False)

@app.route("/campaign/<int:campaign_id>/delete",  methods=['POST'])
@login_required
def delete_campaign(campaign_id):
	campaign = Campaign.query.get_or_404(campaign_id)
	if campaign.author != current_user:
		abort(403)
	db.session.delete(campaign)
	db.session.commit()
	delete_campaign_folder(campaign.campaign_hash)
	flash('Your campaign has been deleted', 'success')
	return redirect(url_for('campaigns'))

# сохраняем картинку баннера в папку кампании
def save_banner_picture(form_image, campaign_hash):
	random_hex = secrets.token_hex(8) 
	f_name, f_ext = os.path.splitext(form_image.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/campaigns',
								campaign_hash, picture_fn)
	form_image.save(picture_path)

	return picture_path

# def write_html_to_file(content, campaign_hash):
# 	path = os.path.join(app.root_path, 'static/campaigns/', campaign_hash)
# 	print(path)

# 	filename = path + "/index.html"
# 	with open (filename, 'w') as f_obj:
# 		f_obj.write(content)

def generate_html(click_link, banner_image):    
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('meta', charset="utf-8"):
                with tag('meta', name="viewport", 
                	content="width=device-width, initial-scale=1, shrink-to-fit=no"):
                    with tag('body'):
                        with tag('a', href=click_link):
                            doc.stag('img',src=banner_image, klass="banner")
    return doc.getvalue()

    # write_html_to_file(doc.getvalue(), campaign_hash)

@app.route("/banner/new", methods=['GET', 'POST'])
@login_required
def new_banner():
	'''
	функция создания баннера-картинки в кампании
	1. получаем из БД нужную кампанию по ее id
	2. сохраняем картинку баннера в файловой системе внутри папки с кампанией
	3. генерируем html-файл с баннером и сохраняем его  в БД
	'''
	campaign_id = request.args.get('campaign_id',type=int)	
	form = BannerForm()
	if form.validate_on_submit():
		if form.image.data:
			campaign = Campaign.query.get_or_404(campaign_id)
			banner_image = save_banner_picture(form.image.data, campaign.campaign_hash)
			print(banner_image)
			banner_html = generate_html(form.click_link.data, banner_image)
			banner = Banner(title=form.title.data, image_file=banner_image, 
							click_link=form.click_link.data, 
							campaign_id=campaign_id, content=banner_html)
			db.session.add(banner)
			db.session.commit()		
			flash('Your banner has been created', 'success')
			return redirect(url_for('campaign',campaign_id=campaign_id))
	return render_template('create_banner.html', form=form, legend='New Banner',
		title='New Banner')

@app.route("/banner/<int:banner_id>", methods=['GET', 'POST'])
@login_required
def banner(banner_id):
	banner = Banner.query.get_or_404(banner_id)
	return render_template('banner.html', title=banner.title, banner=banner)

@app.route("/banner/<int:banner_id>/update", methods=['GET', 'POST'])
@login_required
def update_banner(banner_id):
	banner = Banner.query.get_or_404(banner_id)
	
	if banner.parent_campaign.author != current_user:
		abort(403)

	form = BannerForm()
	if form.validate_on_submit():
		if form.image.data:		
			# print(banner.parent_campaign.campaign_hash)
			banner_image = save_banner_picture(form.image.data, 
							banner.parent_campaign.campaign_hash)
			banner_html = generate_html(form.click_link.data, banner_image)
			banner.content=banner_html			
		banner.title = form.title.data
		banner.click_link = form.click_link.data			
		db.session.commit()
		flash('Your banner has been updated', 'success')
		return redirect(url_for('campaign', campaign_id=banner.parent_campaign.id))

	if request.method == 'GET':
		form.title.data = banner.title
		form.click_link.data = banner.click_link
	return render_template('create_banner.html', title='Update Banner',
							form=form, legend='Update Banner')

@app.route("/banner/<int:banner_id>/delete", methods=['POST'])
@login_required
def delete_banner(banner_id):
	banner = Banner.query.get_or_404(banner_id)
	if banner.parent_campaign.author != current_user:
		abort(403)
	db.session.delete(banner)
	db.session.commit()
	flash('Your banner has been deleted', 'success')
	return redirect(url_for('campaign', campaign_id=banner.parent_campaign.id))


@app.route("/campaign/<int:campaign_id>/start", methods=['POST'])
@login_required
def start_campaign(campaign_id):
	campaign = Campaign.query.get_or_404(campaign_id)
	campaign.status = True
	db.session.commit()

	return redirect(url_for('campaign', campaign_id=campaign.id))

@app.route("/campaign/<int:campaign_id>/stop", methods=['POST'])
@login_required
def stop_campaign(campaign_id):
	campaign = Campaign.query.get_or_404(campaign_id)
	campaign.status = False
	db.session.commit()

	return redirect(url_for('campaign', campaign_id=campaign.id))




