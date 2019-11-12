from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required
from flaskblog import db
from flaskblog.models import Ssp
from flaskblog.ssps.forms import SspForm


sources = Blueprint('sources', __name__)

@sources.route("/ssp/new", methods=['GET', 'POST'])
@login_required
def new_ssp():
    form = SspForm()

    if form.validate_on_submit():
        ssp = Ssp(name=form.name.data, type=form.type.data, endpoint_url=form.endpoint_url.data)
        db.session.add(ssp)
        db.session.commit()
        flash('The new SSP has been created', 'success')

        return redirect(url_for('ssps.ssps'))
    return render_template('create_ssp.html', form=form, legend='New SSP')

@sources.route("/ssps")
@login_required
def ssps():    
    ssps = Ssp.query.all()
    return render_template('ssps.html', ssps=ssps)

@sources.route("/ssp/<int:ssp_id>")
@login_required
def ssp(ssp_id):
    ssp = SSP.query.get_or_404(ssp_id)
    return render_template('ssp.html', ssp=ssp)

@sources.route("/ssp/<int:ssp_id>/update",  methods=['GET', 'POST'])
@login_required
def update_ssp(ssp_id):    
    ssp = Ssp.query.get_or_404(ssp_id)
    form = SspForm()   
    if form.validate_on_submit():        
        ssp.name = form.name.data
        ssp.type = form.type.data
        ssp.endpoint_url = form.endpoint_url.data
        db.session.commit()
        flash('The SSP has been updated', 'success')
        return redirect(url_for('ssps.ssps'))
    elif request.method == 'GET':
        form.name.data = ssp.name
        form.type.data = ssp.type
        form.endpoint_url.data = ssp.endpoint_url
    return render_template('create_ssp.html', title='Update SSP',
                            form=form, legend='Update SSP')

@sources.route("/ssp/<int:ssp_id>/delete", methods=['POST'])
@login_required
def delete_ssp(ssp_id):    
    ssp = Ssp.query.get_or_404(ssp_id)    
    db.session.delete(ssp)
    db.session.commit()
    flash('The SSP has been deleted', 'success')
    return redirect(url_for('ssps.ssps'))