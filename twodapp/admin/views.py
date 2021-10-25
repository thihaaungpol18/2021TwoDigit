from flask import Blueprint, render_template,redirect, abort,url_for,request
from flask.helpers import flash
from twodapp import db
from twodapp.admin.forms import LoginForm,RegisterForm
from twodapp.models import Admin
from flask_login import login_user, current_user, logout_user, login_required

admin = Blueprint("admin",__name__)
#Responsible For Admin Accounts Create , Read , And Login Logout
@admin.route('/admin/login',methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if  admin is None:
            flash("Wrong email or password")
        elif admin.check_username(form.username.data) and admin.check_password(form.password.data) and admin is not None:
            login_user(admin)
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('bets.getBets')
            return redirect(next)
        else:
            flash("Wrong email or password")
    return render_template('admin/login.html',form=form)

@admin.route('/admin/register',methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        admin = Admin(username=form.username.data,
                        password_hash=form.password.data)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('admin.login'))
    return render_template('admin/register.html',form=form)
    
@admin.route('/admin/logout',methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))