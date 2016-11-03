from flask import Blueprint, render_template, current_app, flash, request, redirect, url_for
from lightmdb.forms import ContactForm
from lightmdb.models import ContactMessage

contactus = Blueprint('contactus', __name__)


@contactus.route("/", methods=["GET", "POST"])
def contact():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        message = ContactMessage(
            title=form.title.data,
            content=form.content.data,
            email=form.email.data,
            phone=form.phone.data
        )
        message.save()
        return render_template('contact/thanks.html')
    return render_template('contact/contact.html', form=form)


@contactus.route("/admin/", methods=["GET", "POST"])
def contact_admin():
    desired_types = ['new']
    if request.method == 'POST':
        flash(request.form)
        if 'update' in request.form and 'status' in request.form:
            message=ContactMessage(request.form['update'])
            message.change_status(request.form['status'])
        elif 'delete' in request.form:
            message = ContactMessage(request.form['delete'])
            message.delete_message()
        elif 'show' in request.form:
            desired_types=[]
            all_types=['new','replied','waiting','spam','closed']
            for one_type in all_types:
                if one_type in request.form:
                    desired_types.append(one_type)
    messages=ContactMessage.get_messages(desired_types)
    return render_template(
        'contact/contactadmin.html',
        table=messages,
        thead=[
            'Update Status', 'Title', 'Content', 'Email',
            'Phone', 'Status', 'Sent Time', 'Delete'
        ]
    )
