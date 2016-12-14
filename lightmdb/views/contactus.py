from flask import Blueprint, render_template, current_app, flash, request, redirect, url_for
from lightmdb.forms import ContactForm
from lightmdb.models import ContactMessage,ContactComment

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
    comments=[]
    pk_contact=0
    notpost=0
    if request.method == 'POST':
        flash(request.form)
        if 'update' in request.form and 'status' in request.form:
            message=ContactMessage(request.form['update'])
            message.change_status(request.form['status'])
            if 'sendMail' in request.form:
                send_mail = True
            else:
                send_mail = False
            if 'commentUpdate' in request.form:
                comment=ContactComment(pk=request.form['commentUpdate'])
                comment.update_comment(request.form['comment'],send_mail)
            else:
                comment=ContactComment(pk_contact=message.cid,comment=request.form['comment'],send_mail=send_mail)
                comment.save()
        if 'delete' in request.form:
            message = ContactMessage(request.form['delete'])
            message.delete_message()
            comment=ContactComment(pk_contact=message.cid)
            comment.delete_comments_by_contact_id()
        elif 'deletecomment' in request.form:
            comment = ContactComment(pk=request.form['deletecomment'])
            comment.delete_comments_by_id()
        desired_types=[]
        all_types=['new','replied','waiting','spam','closed']
        for one_type in all_types:
            if one_type in request.form:
                desired_types.append(one_type)
        if 'showComments' in request.form:
            pk_contact=request.form['showComments']
            contact_comment=ContactComment(pk_contact=pk_contact)
            comments=contact_comment.get_comments_by_contact_id()
            if not comments:
                comments=[]
    else:
        notpost=1

    messages=ContactMessage.get_messages(desired_types)
    return render_template(
        'contact/contactadmin.html',
        table=messages,
        comments=comments,
        pk_contact=int(pk_contact),
        post=request.form,
        len=len(comments),
        notpost=notpost,
        thead=[
            'Title', 'Content', 'Email',
            'Phone', 'Status', 'Sent Time','Comment' ,'Delete'
        ]
    )


@contactus.teardown_request
def close_connection(error=None):
    from lightmdb import close_db
    close_db()
