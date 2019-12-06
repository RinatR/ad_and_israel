from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, login_required
from ad_and_israel import db
import secrets
from ad_and_israel.models import Htmlbanner, Ssp, Campaign, Region, Os
from ad_and_israel.html_banners.forms import HtmlbannerForm


html_banner = Blueprint('html_banners', __name__)

@html_banner.route("/html_banner/new", methods=['GET', 'POST'])
@login_required
def new_banner():
    campaign_id = request.args.get('campaign_id',type=int)
    form = HtmlbannerForm() 

    if form.validate_on_submit():
        chosen_ssp_ids = [] 
        for cx in form.ssp_checkboxes:
            ssp = Ssp.query.filter_by(name=cx.data).first()            
            if cx.checked == True:
                chosen_ssp_ids.append(ssp)

        campaign = Campaign.query.get_or_404(campaign_id)
                       
        trafkey = secrets.token_hex(8) # здесь генерируем трафкей              
        banner = Htmlbanner(title=form.title.data, width=form.width.data, 
                            height=form.height.data, content=form.content.data, click_link=form.click_link.data, 
                            audit_link=form.audit_link.data, campaign_id=campaign_id, trafkey=trafkey)

        #  добавляем выбранные ссп к баннеру
        for x in chosen_ssp_ids:
            banner.ssps_htmlbanner.append(x)

        #  добавляем выбранные регионы к баннеру
        for region in form.region_list.data:
            reg = Region.query.filter_by(id=region).first()            
            banner.regions_htmlbanner.append(reg)

         #  добавляем выбранные операционные системы к баннеру
        for os in form.os_list.data:
            oper_sys = Os.query.filter_by(id=os).first()            
            banner.operating_systems_htmlbanner.append(oper_sys)

        db.session.add(banner)
        db.session.commit()                 
        flash('Your banner has been created', 'success')
        return redirect(url_for('campaigns.campaign',campaign_id=campaign_id)) 


    return render_template('create_html_banner.html', form=form, legend='New Banner', 
                            title='New Banner')


@html_banner.route("/html_banner/<int:banner_id>", methods=['GET', 'POST'])
@login_required
def banner(banner_id):
    banner = Htmlbanner.query.get_or_404(banner_id)   
    
    return render_template('html_banner.html', title=banner.title, html_banner=banner)


@html_banner.route("/html_banner/<int:banner_id>/update", methods=['GET', 'POST'])
@login_required
def update_banner(banner_id):
    banner = Htmlbanner.query.get_or_404(banner_id)
    if banner.parent_campaign.author != current_user:
        abort(403)

    form = HtmlbannerForm()

    if form.validate_on_submit():
        banner.title = form.title.data
        banner.width = form.width.data
        banner.height = form.height.data
        banner.content = form.content.data
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
            banner.ssps_htmlbanner.append(x)  

        # проверяем, назначены ли уже в текущем баннере ссп, которые сейчас не выбраны в чекбоксах и удаляем их из БД, если таковые имеются.
        for x in unselected_ssp_ids:
            if x in banner.ssps_htmlbanner:
                banner.ssps_htmlbanner.remove(x)

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
            banner.regions_htmlbanner.append(region)

        # проверяем, назначены ли уже в текущем баннере регионы, которые сейчас не выбраны в выпадающем списке с регионами и удаляем их из БД, если таковые имеются.
        for x in unselected_regions:
            if x in banner.regions_htmlbanner:
                banner.regions_htmlbanner.remove(x) 


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
            banner.operating_systems_htmlbanner.append(os)

        # проверяем, назначены ли уже в текущем баннере операционные системы, которые сейчас не выбраны в выпадающем списке с ОС и удаляем их из БД, если таковые имеются.
        for x in unselected_os:
            if x in banner.operating_systems_htmlbanner:
                banner.operating_systems_htmlbanner.remove(x)

        db.session.add(banner)
        db.session.commit()

        flash('Your banner has been updated', 'success')
        return redirect(url_for('campaigns.campaign', campaign_id=banner.parent_campaign.id))

    if request.method == 'GET': 
        form.title.data = banner.title
        form.width.data = banner.width
        form.height.data = banner.height
        form.content.data = banner.content
        form.click_link.data = banner.click_link
        form.audit_link.data = banner.audit_link

        return render_template('create_html_banner.html', title='Update Banner', form=form, legend='Update Banner')


@html_banner.route("/html_banner/<int:banner_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_banner(banner_id):
    banner = Htmlbanner.query.get_or_404(banner_id)
    if banner.parent_campaign.author != current_user:
        abort(403)
    db.session.delete(banner)
    db.session.commit()
    flash('Your banner has been deleted', 'success')
    return redirect(url_for('campaigns.campaign', campaign_id=banner.parent_campaign.id))