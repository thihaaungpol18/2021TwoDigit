from flask import Blueprint, render_template,redirect,url_for,flash
from twodapp import db
from twodapp.models import Agent, Bet, ThreeDigit, TwoDigit
from sqlalchemy import desc
from twodapp.bets.forms import BetForm
from datetime import datetime
from flask_login import login_required

bets =  Blueprint('bets', __name__)

#Responsible For Bettins CRD

@bets.route('/bets/<int:bet_id>')
@bets.route('/bets/<int:bet_id>/')
@login_required
def deleteBet(bet_id):
    #Deleting a bet and payback amount if the bet is deleted if nesscessry!
    bet = Bet.query.get(bet_id)
    agent = bet.agent_rs
        
    if bet.state=="win" or bet.state=="lose" or bet.state=="notnow" or bet.state=="unavailable" or bet.state=="initial":
        agent.balance = str(int(agent.balance)+int(bet.amount))
        agent.total_amount=str(int(agent.total_amount)-int(bet.amount))
        db.session.delete(bet)
        db.session.commit()
        flash("Successfully Delete",'error')
    else:
        db.session.delete(bet)
        db.session.commit()
        flash("Successfully Delete",'error')
    return redirect(url_for('bets.getBets'))

@bets.route('/bets/del/<int:bet_id>')
@bets.route('/bets/del/<int:bet_id>/')
@login_required
def deleteBetFromAgentProfile(bet_id):
    #Deleting a bet and payback amount if the bet is deleted if nesscessry!
    bet = Bet.query.get(bet_id)
    agent = bet.agent_rs
        
    if bet.state=="win" or bet.state=="lose" or bet.state=="notnow" or bet.state=="unavailable" or bet.state=="initial":
        agent.balance = str(int(agent.balance)+int(bet.amount))
        agent.total_amount=str(int(agent.total_amount)-int(bet.amount))
        db.session.delete(bet)
        db.session.commit()
    else:
        db.session.delete(bet)
        db.session.commit()
    return redirect(url_for('agents.agentProfile',agent_id=agent.id))

@bets.route('/',methods=["GET", "POST"])
@bets.route('/bets',methods=["GET", "POST"])
@bets.route('/bets/',methods=["GET", "POST"])
@login_required
def getBets():
#states={"initial","notnow","win","lose","unavailable","paid"}
    all_bets = Bet.query.order_by(desc(Bet.date)).all()
    for bet in all_bets:
        if bet.state=="initial" or bet.state=="notnow" or bet.state=="unavailable":
            day=datetime.strptime(bet.date,'%Y-%m-%d').day
            month = datetime.strptime(bet.date,'%Y-%m-%d').month
            year = datetime.strptime(bet.date,'%Y-%m-%d').year

            today = datetime.utcnow()
            if datetime.strptime(bet.date,'%Y-%m-%d')>today:
                bet.state="notnow"
            else:
                if len(bet.value)==3:
                    ##THREE D
                    print("3 Digit : {}".format(bet.value))
                    real_threedigit_numbers = ThreeDigit.query.order_by(desc(ThreeDigit.date)).all()
                    for number in real_threedigit_numbers:
                        
                        number_day=datetime.strptime(number.date,'%Y-%m-%d').day
                        number_month=datetime.strptime(number.date,'%Y-%m-%d').month
                        number_year=datetime.strptime(number.date,'%Y-%m-%d').year

                        if number_year==year and number_month==month and number_day==day and str(bet.value)==str(number.value):
                            bet.state="win"
                            bet.amount_to_pay = str(int(bet.amount)*bet.product)
                            break
                        elif number_year==year and number_month==month and number_day==day and str(bet.value)!=str(number.value):
                            bet.state="lose"
                            break
                        else:
                            bet.state="unavailable"
                else:
                    ##TWO D
                    real_twodigit_numbers = TwoDigit.query.order_by(desc(TwoDigit.date)).all()
                    for number in real_twodigit_numbers:

                        number_day=datetime.strptime(number.date,'%Y-%m-%d').day
                        number_month=datetime.strptime(number.date,'%Y-%m-%d').month
                        number_year=datetime.strptime(number.date,'%Y-%m-%d').year

                        if number_year==year and number_month==month and number_day==day and number.time == bet.time and str(bet.value)==str(number.value):
                            bet.state="win"
                            bet.amount_to_pay = str(int(bet.amount)*bet.product)
                            break
                        elif number_year==year and number_month==month and number_day==day and number.time == bet.time and str(bet.value)!=str(number.value):
                            bet.state="lose"
                            break
                        else:
                            bet.state="unavailable"
    db.session.commit()
    bets = Bet.query.order_by(desc(Bet.date)).all()

    ###################################################################
    # Adding New Bet

    form = BetForm()
    a = Agent.query.order_by(desc(Agent.id)).all()
    agents = [(agent.id,agent.name)for agent in a]
    form.agents.choices = agents
    if form.validate_on_submit():
        bet = Bet(date=str(form.date.data),
            product = int(form.product.data),
            value=str(form.value.data),
            amount=str(form.amount.data),
            time=str(form.time.data),
            agent_id=form.agents.data)
        db.session.add(bet)
        db.session.commit()
        for b in Bet.query.all():
            if b==bet:
                agent = Agent.query.get(b.agent_id)
                agent.balance=str(int(agent.total_amount)-int(b.amount))
                agent.total_amount=str(int(agent.total_amount)+int(bet.amount))
                db.session.commit()
                break
        return redirect(url_for('bets.getBets'))
    ###################################################################

    return render_template("bets/list_table.html",bets=bets,form=form)

@bets.route('/bets/<int:id>/repay')
@login_required
def payToAgent(id):
    bet = Bet.query.get(id)
    if bet.state=="win":
        agent = bet.agent_rs
        agent.balance = str(int(agent.balance)+int(bet.amount_to_pay))
        bet.state = "paid"
        db.session.commit()
        return redirect(url_for('bets.getBets'))
    elif bet.state=="lose":
        bet.state = "paid"
        db.session.commit()
        return redirect(url_for('bets.getBets'))

@bets.route('/bets/<int:id>/repay/agent')
@login_required
def payToAgentFromAgentProfile(id):
    bet = Bet.query.get(id)
    if bet.state=="win":
        agent = bet.agent_rs
        agent.balance = str(int(agent.balance)+int(bet.amount_to_pay))
        bet.state = "paid"
        db.session.commit()
        return redirect(url_for('agents.agentProfile',agent_id=bet.agent_rs.id))
    elif bet.state=="lose":
        bet.state = "paid"
        db.session.commit()
        return redirect(url_for('agents.agentProfile',agent_id=bet.agent_rs.id))

