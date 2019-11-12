from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, login_required
from flaskblog import db
import secrets
from flaskblog.models import Banner, Ssp, Campaign, Region
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
    for b in banner.regions:
        print(b.name)
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