from flask import Flask, render_template, url_for, request
from models import *

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./chroniclingamerica.sqlite' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    # db.drop_all()
    db.create_all()

@app.route('/')
def index():
    # return "Hello! This is a test that the app runs correctly."
    count = Paper.query.count()
    list_page = url_for('papers')
    return """
    <h1>Matt's Library of Congress Chronicling America Newspaper Directory</h1>
    <p>Welcome! This is a directory of newspaper metadata for all of the newspapers contained
    in the Library of Congress's Chronicling America newspaper archive, a total of {} newspapers. Please review my README file
    on <a href="https://github.com/mwhanger/si507_final">github</a> for a list of routes, or click
    <a href="{}">here</a> for a full directory of all papers in the directory, in order from oldest to newest.
    """.format(count,list_page)

#https://stackoverflow.com/questions/14032066/can-flask-have-optional-url-parameters
@app.route('/papers')
@app.route('/papers/<int:page_num>')
@app.route('/papers/<state_name>/<int:page_num>')
def papers(page_num=1,state_name=None):
    # if not page_num:
    #     page_num = 1
    #https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination
    if state_name:
        chose_state = State.query.filter_by(name=state_name).first()
        #print(chose_state.papers)
        papers = chose_state.papers.filter(Paper.start_year.notin_([9999,0,1000])).order_by(Paper.start_year.asc()).paginate(page=page_num, per_page=25)
    else:
        papers = Paper.query.filter(Paper.start_year.notin_([9999,0,1000])).order_by(Paper.start_year.asc()).paginate(page=page_num, per_page=25)
    next_url = url_for('papers', state_name=state_name, page_num=papers.next_num) if papers.has_next else None
    prev_url = url_for('papers', state_name=state_name, page_num=papers.prev_num) if papers.has_prev else None
    return render_template("papers_list.html", papers=papers.items, next_url=next_url, prev_url=prev_url, state_name=state_name)

#https://stackoverflow.com/questions/7782046/how-do-i-use-url-for-if-my-method-has-multiple-route-annotations
@app.route('/ended/<int:year>', endpoint="ended")
@app.route('/started/<int:year>', endpoint="started")
@app.route('/ended/<state_name>/<int:year>', endpoint="ended")
@app.route('/started/<state_name>/<int:year>', endpoint="started")
def year_papers(year, state_name=None):
    #https://stackoverflow.com/questions/21498694/flask-get-current-route
    if "ended" in request.url_rule.rule:
        filt = 'end_year'
        cond = "Ended"
    elif "started" in request.url_rule.rule:
        filt = 'start_year'
        cond = "Started"
    page = request.args.get('page', 1, type=int)
    if state_name:
        chose_state = State.query.filter_by(name=state_name).first()
        #https://stackoverflow.com/questions/10251724/how-to-give-column-name-dynamically-from-string-variable-in-sql-alchemy-filter
        papers = chose_state.papers.filter(getattr(Paper, filt)==year).order_by(Paper.title.asc()).paginate(page=page, per_page=25)
    else:
        papers = Paper.query.filter(getattr(Paper, filt)==year).order_by(Paper.title.asc()).paginate(page=page, per_page=25)
    next_url = url_for(cond.lower(), state_name=state_name, page=papers.next_num, year=year) if papers.has_next else None
    prev_url = url_for(cond.lower(), state_name=state_name, page=papers.prev_num, year=year) if papers.has_prev else None
    return  render_template("pub_years.html", papers=papers.items, cond=cond, state_name=state_name, year=year, next_url=next_url, prev_url=prev_url)

if __name__ == "__main__":
    app.run()
