from twodapp.agents.form import AgentForm
from twodapp.bets.forms import BetForm
from twodapp.models import Agent, Bet, ThreeDigit, TwoDigit
from flask import Blueprint,render_template,flash,redirect,url_for,request
from twodapp import db
from sqlalchemy import desc
from datetime import datetime
from flask_login import login_required

agents = Blueprint("agents",__name__)

#Responsible For Agents Create,Read,Delete,Update

@agents.route('/agents/',methods=["GET","POST"])
@agents.route('/agents',methods=["GET","POST"])
@login_required
def getAgents():
    #Form modal For Creating a new agent And Showing Data In Table
    form = AgentForm()
    if form.validate_on_submit():
        agent = Agent(name=form.name.data)
        db.session.add(agent)
        db.session.commit()
        flash("Success! You Just Created An Agent!")
        return redirect(url_for('agents.getAgents'))
    agents = Agent.query.order_by(desc(Agent.id)).all()
    return render_template('agents/agent_list.html',agents=agents,form=form)

@agents.route('/agents/<int:agent_id>/',methods=["GET","POST"])
@agents.route('/agents/<int:agent_id>',methods=["GET","POST"])
@login_required
def agentProfile(agent_id):
    #Showing Specific Agent's Details with card and also with table
    #Form For adding a bet
    item = Agent.query.get(agent_id)
    all_bets = Bet.query.filter(Bet.agent_id == agent_id).order_by(desc(Bet.date))

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
    bets = Bet.query.filter(Bet.agent_id == agent_id).order_by(desc(Bet.date)).all()


    #############################################################################
    #ADDING NEW BET FROM AGENT_PROFILE
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
                agent.total_amount=str(int(agent.total_amount)+int(b.amount))
                agent.balance = str(int(agent.balance)-int(b.amount))
                db.session.commit()
                break
        return redirect(url_for('agents.agentProfile',agent_id=bet.agent_id))
        #############################################################################
    return render_template('agents/agent_profile.html',agent=item,bets=bets,agent_id=agent_id,form=form)

@agents.route('/agents/delete/<int:id>',methods=["GET","POST"])
@login_required
def deleteAgent(id):
    # Clearly , For Deleting An Agent
    item = Agent.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('agents.getAgents'))

@agents.route('/agents/update/<int:id>',methods=["GET","POST"])
@login_required
def updateAgent(id):
    # Also Updating Name of an agent 
    form = AgentForm()
    item = Agent.query.get(id)
    if form.validate_on_submit():
        item.name = form.name.data
        print(form.name.data)
        db.session.commit()
        return redirect(url_for('agents.getAgents'))