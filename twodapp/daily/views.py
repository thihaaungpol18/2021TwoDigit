from datetime import datetime
from flask import request
from twodapp.daily.forms import TwoDigitAddForm, TwoDigitForm
from flask import render_template,Blueprint,redirect,url_for
from twodapp.models import Bet, ThreeDigit, TwoDigit
from datetime import datetime
from twodapp import db
from sqlalchemy import desc
from dateutil import tz

daily = Blueprint("daily",__name__)

@daily.route('/daily/get',methods=["GET","POST"])
@daily.route('/daily/get/',methods=["GET","POST"])
def putDailyToDb():
    # #Need Fix
    # form = TwoDigitForm()
    # if form.validate_on_submit():
    #     to_zone = tz.tzlocal()
    #     now = datetime.utcnow()
    #     time = ''
    #     four = now.replace(hour=9,minute=30)
    #     twelve_thirty = now.replace(hour=12,minute=30)
    #     if now >= four:
    #         time = 'evening'       
    #         source =  requests.get('https://marketdata.set.or.th/mkt/sectorialindices.do?language=en&country=US').text
    #         soup  = bs.BeautifulSoup(source,'lxml')
    #         soups = soup.find_all('td')
    #         set = str(soups[1])
    #         value = str(soups[7])
    #         real_value = str(set.split('.')[1][1])+str(value.split('.')[0][-1])
    #         twodigit = TwoDigit(value=real_value,time=time)
    #         print(time)
    #         db.session.add(twodigit)
    #     elif now<=twelve_thirty  or now <= four :
    #         time = 'morning'       
    #         source =  requests.get('https://marketdata.set.or.th/mkt/sectorialindices.do?language=en&country=US').text
    #         soup  = bs.BeautifulSoup(source,'lxml')
    #         soups = soup.find_all('td')
    #         set = str(soups[1])
    #         value = str(soups[7])
    #         real_value = str(set.split('.')[1][1])+str(value.split('.')[0][-1])
    #         twodigit = TwoDigit(value=real_value,time=time)
    #         print(time)
    #         db.session.add(twodigit)
    #     db.session.commit()
    #     return redirect(url_for('daily.getDailyUpdates'))

    # return render_template('daily/updateDailyDigits.html',form=form)
    return render_template('daily/updateDailyDigits.html')

@daily.route('/daily/add',methods=["GET","POST"])
@daily.route('/daily/add/',methods=["GET","POST"])
def addTwoDigit():
    form = TwoDigitAddForm()
    if len(str(form.value.data))==3:
        item = ThreeDigit(date=str(form.date.data),value=str(form.value.data),time=str(form.time.data))
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('daily.dailyNumbers'))
    else:
        if form.validate_on_submit():
            item = TwoDigit(date=str(form.date.data),value=str(form.value.data),time=str(form.time.data))
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('daily.dailyNumbers'))
    return render_template('daily/add.html',form=form)


@daily.route('/daily',methods=["GET","POST"])
@daily.route('/daily/',methods=["GET","POST"])
def dailyNumbers():
    form = TwoDigitAddForm()
    if len(str(form.value.data))<=2: 
        if form.validate_on_submit():
            item = TwoDigit(date=str(form.date.data),value=str(form.value.data),time=str(form.time.data))
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('daily.dailyNumbers'))

    all_items = TwoDigit.query.order_by(desc(TwoDigit.date))
    return render_template('daily/list_two_d.html',all_items=all_items,form=form)

@daily.route('/daily/threedigit',methods=["GET","POST"])
@daily.route('/daily/threedigit/',methods=["GET","POST"])
def dailyThreeDigitNumbers():
    form = TwoDigitAddForm()
    if len(str(form.value.data))==3: 
        if form.validate_on_submit():
            item = ThreeDigit(date=str(form.date.data),value=str(form.value.data),time=str(form.time.data))
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('daily.dailyThreeDigitNumbers'))
    all_3d_items = ThreeDigit.query.order_by(desc(ThreeDigit.date))
    return render_template('daily/list_three_d.html',all_3d_items=all_3d_items,form=form)


@daily.route('/daily/delete/<int:id>')
@daily.route('/daily/delete/<int:id>/')
def delete(id):
    item = TwoDigit.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('daily.dailyNumbers'))

@daily.route('/daily/delete/threedigit/<int:id>')
@daily.route('/daily/delete/threedigit/<int:id>/')
def deleteThreeDigit(id):
    item = ThreeDigit.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('daily.dailyNumbers'))