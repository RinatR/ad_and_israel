from flask import (render_template, url_for, flash, redirect, request, Blueprint)
from flask_login import login_user, current_user, login_required
from flaskblog import db
from flaskblog.models import Campaign, Banner
from flaskblog.campaigns.forms import CampaignForm
from flaskblog.campaigns.utils import create_folder, delete_campaign_folder


camps = Blueprint('campaigns', __name__)

@camps.route("/campaign/new", methods=['GET','POST'])
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
        return redirect(url_for('campaigns.campaigns'))
    return render_template('create_campaign.html', title='New Campaign', form=form, 
                            legend='New Campaign')

@camps.route("/")
@camps.route("/campaigns")
@login_required
def campaigns():
    page = request.args.get('page', 1, type=int)
    campaigns = Campaign.query.order_by(Campaign.finish_date.desc())
    return render_template('campaigns.html', campaigns=campaigns)

@camps.route("/campaign/<int:campaign_id>")
@login_required
def campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    banners = Banner.query.filter_by(campaign_id=campaign_id).all()  
    
    return render_template('campaign.html', title=campaign.title, 
        campaign=campaign, banners=banners)

@camps.route("/campaign/<int:campaign_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('campaigns.campaigns'))
    elif request.method == 'GET':
        form.title.data = campaign.title
        form.start_date.data = campaign.start_date  
        form.finish_date.data = campaign.finish_date
        return render_template('create_campaign.html', title='Update Campaign',
                            form=form, legend='Update Campaign')


@camps.route("/campaign/<int:campaign_id>/delete",  methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.author != current_user:
        abort(403)
    db.session.delete(campaign)
    db.session.commit()
    delete_campaign_folder(campaign.campaign_hash)
    flash('Your campaign has been deleted', 'success')
    return redirect(url_for('campaigns.campaigns'))

@camps.route("/campaign/<int:campaign_id>/start", methods=['POST'])
@login_required
def start_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.status = True
    db.session.commit()

    return redirect(url_for('campaigns.campaign', campaign_id=campaign.id))

@camps.route("/campaign/<int:campaign_id>/stop", methods=['POST'])
@login_required
def stop_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.status = False
    db.session.commit()

    return redirect(url_for('campaigns.campaign', campaign_id=campaign.id))