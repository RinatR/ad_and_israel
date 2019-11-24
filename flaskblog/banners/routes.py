from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, login_required
from flaskblog import db
import secrets
from flaskblog.models import Banner, Ssp, Campaign, Region, Os
from flaskblog.banners.forms import BannerForm
from flaskblog.banners.utils import save_banner_picture, write_html_to_file, generate_html

banners = Blueprint('banners', __name__)

@banners.route("/banner/new", methods=['GET', 'POST'])
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
        chosen_ssp_ids = [] 
        for cx in form.ssp_checkboxes:
            ssp = Ssp.query.filter_by(name=cx.data).first()            
            if cx.checked == True:
                chosen_ssp_ids.append(ssp) 

        if form.image.data:
            campaign = Campaign.query.get_or_404(campaign_id)            
            banner_image = save_banner_picture(form.image.data, campaign.campaign_hash)            
            trafkey = secrets.token_hex(8) # здесь генерируем трафкей
            banner_html = generate_html(banner_image, trafkey, campaign.campaign_hash)    
            write_html_to_file(banner_html,campaign.campaign_hash, trafkey)     
            banner = Banner(title=form.title.data, image_file=banner_image, width=form.width.data, 
                            height=form.height.data, click_link=form.click_link.data, audit_link=form.audit_link.data,
                            campaign_id=campaign_id, content=banner_html, trafkey=trafkey)

            #  добавляем выбранные ссп к баннеру
            for x in chosen_ssp_ids:
                banner.ssps.append(x)

            #  добавляем выбранные регионы к баннеру
            for region in form.region_list.data:
                reg = Region.query.filter_by(id=region).first()            
                banner.regions.append(reg)

             #  добавляем выбранные операционные системы к баннеру
            for os in form.os_list.data:
                oper_sys = Os.query.filter_by(id=os).first()            
                banner.operating_systems.append(oper_sys)
            
            db.session.add(banner)
            db.session.commit()                 
            flash('Your banner has been created', 'success')
            return redirect(url_for('campaigns.campaign',campaign_id=campaign_id))
    return render_template('create_banner.html', form=form, legend='New Banner', title='New Banner')



# https://log.rinads.com/?src=bw&s_act=c&s_trk=CghWgOBZk3yCtxDazeWmCxjFq7XMBQ**

# https://log.rinads.com/?src=bw&s_act=s&s_trk=CghWgOBZk3yCtxDazeWmCxjFq7XMBQ**

# https://log.rinads.com/?src=bw&s_act=n&s_trk=CghWgOBZk3yCtxDazeWmCxjFq7XMBQ**

@banners.route("/banner/<int:banner_id>", methods=['GET', 'POST'])
@login_required
def banner(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    # for b in banner.ssps:
    #     print(b.name)
    print(banner.operating_systems)
    return render_template('banner.html', title=banner.title, banner=banner)

@banners.route("/banner/<int:banner_id>/update", methods=['GET', 'POST'])
@login_required
def update_banner(banner_id):
    banner = Banner.query.get_or_404(banner_id) 

    if banner.parent_campaign.author != current_user:
        abort(403)
    form = BannerForm()    
    if form.validate_on_submit():        

        if form.image.data:           
            banner_image = save_banner_picture(form.image.data, 
                            banner.parent_campaign.campaign_hash)
            banner_html = generate_html(form.click_link.data, banner_image)
            banner.content = banner_html          
        banner.title = form.title.data
        banner.width = form.width.data
        banner.height = form.height.data
        banner.click_link = form.click_link.data
        banner.audit_link = form.audit_link.data


        selected_ssp_ids = [] 
        unselected_ssp_ids = []
        for cx in form.ssp_checkboxes:
            ssp = Ssp.query.filter_by(name=cx.data).first()            
            if cx.checked == True:
                selected_ssp_ids.append(ssp) 
            else:
                unselected_ssp_ids.append(ssp)
        
        # добавляем выбранные ссп к конкретному баннеру
        for x in selected_ssp_ids:
            banner.ssps.append(x)  

        # проверяем, назначены ли уже в текущем баннере ссп, которые сейчас не выбраны в чекбоксах и удаляем их из БД, если таковые имеются.
        for x in unselected_ssp_ids:
            if x in banner.ssps:
                banner.ssps.remove(x)

        #  определяем выбранные и невыбранные регионы из выпадающего списка и пишем их в соответствующий список
        selected_regions = []
        unselected_regions = []
        for region in form.region_list.choices:
            if region[0] in form.region_list.data:
                reg = Region.query.filter_by(id=region[0]).first()
                selected_regions.append(reg)
            else:
                reg = Region.query.filter_by(id=region[0]).first()
                unselected_regions.append(reg)

        # добавляем выбранные регионы к конкретному баннеру
        for region in selected_regions:
            banner.regions.append(region)

        # проверяем, назначены ли уже в текущем баннере регионы, которые сейчас не выбраны в выпадающем списке с регионами и удаляем их из БД, если таковые имеются.
        for x in unselected_regions:
            if x in banner.regions:
                banner.regions.remove(x) 


        #  определяем выбранные и невыбранные операционные системы из выпадающего списка и пишем их в соответствующий список
        selected_os = []
        unselected_os = []
        for os in form.os_list.choices:
            if os[0] in form.os_list.data:
                oper_sys = Os.query.filter_by(id=os[0]).first()
                selected_os.append(oper_sys)
            else:
                oper_sys = Os.query.filter_by(id=os[0]).first()
                unselected_os.append(oper_sys)

        # добавляем выбранные операционные системы к конкретному баннеру
        for os in selected_os:
            banner.operating_systems.append(os)

        # проверяем, назначены ли уже в текущем баннере операционные системы, которые сейчас не выбраны в выпадающем списке с ОС и удаляем их из БД, если таковые имеются.
        for x in unselected_os:
            if x in banner.operating_systems:
                banner.operating_systems.remove(x)
        
        db.session.add(banner)         
        db.session.commit()
        flash('Your banner has been updated', 'success')        
    
        return redirect(url_for('campaigns.campaign', campaign_id=banner.parent_campaign.id))

    if request.method == 'GET':
        form.title.data = banner.title
        form.width.data = banner.width
        form.height.data = banner.height    
        form.click_link.data = banner.click_link
        form.audit_link.data = banner.audit_link        
                
    return render_template('create_banner.html', title='Update Banner',
                            form=form, legend='Update Banner')

@banners.route("/banner/<int:banner_id>/delete", methods=['POST'])
@login_required
def delete_banner(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    if banner.parent_campaign.author != current_user:
        abort(403)
    db.session.delete(banner)
    db.session.commit()
    flash('Your banner has been deleted', 'success')
    return redirect(url_for('campaigns.campaign', campaign_id=banner.parent_campaign.id))


# @app.route("/regions", methods=['GET'])

# def search_regions():    
#     regions = Region.query.all()            
#     region_dict = {}
#     region_list = []
#     for region in regions:
#         region_dict[region.id] = region.name   

#     region_list.append(region_dict)
#     response = jsonify(region_list)
    
#     return response
    
# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web', 
#         'done': False
#     }
# ]

# @app.route('/rinatads/api/v1.0/banners', methods=['GET'])
# def get_banners():
#     banners = Banner.query.all()    
#     banners_list = []
    
#     for banner in banners:
#         banners_dict = {}
#         banners_dict['id'] = banner.id
#         banners_dict['title'] = banner.title
#         banners_dict['width'] = banner.width
#         banners_dict['height'] = banner.height        
#         banners_list.append(banners_dict)
    
#     response = jsonify(banners_list)
    
#     return response


# @app.route('/rinatads/api/v1.0/banners/<int:banner_id>', methods=['GET'])
# def get_banner(banner_id):
#     banner = Banner.query.filter_by(id=banner_id).first()   
    
#     banner_dict = {}
#     banner_dict['id'] = banner.id
#     banner_dict['title'] = banner.title
#     banner_dict['width'] = banner.width
#     banner_dict['height'] = banner.height 
    
#     return jsonify(banner_dict)


# @app.route('/rinatads/api/v1.0/banners', methods=['POST'])
# def create_banner():    
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': task}), 201

# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
# def update_task(task_id):
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if 'title' in request.json and type(request.json['title']) != unicode:
#         abort(400)
#     if 'description' in request.json and type(request.json['description']) is not unicode:
#         abort(400)
#     if 'done' in request.json and type(request.json['done']) is not bool:
#         abort(400)
#     task[0]['title'] = request.json.get('title', task[0]['title'])
#     task[0]['description'] = request.json.get('description', task[0]['description'])
#     task[0]['done'] = request.json.get('done', task[0]['done'])
#     return jsonify({'task': task[0]})

# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
# def delete_task(task_id):
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#     tasks.remove(task[0])
#     return jsonify({'result': True})