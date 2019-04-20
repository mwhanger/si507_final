# -*- coding: utf-8 -*-

import requests, requests_cache
import json
import time

#Importing main flask app file to use its context and database connection
# import SI507_final as fp
# from flask_sqlalchemy import SQLAlchemy
from models import Paper, Publisher, State, Place, Language, Frequency, Subject
from SI507_final import db, app

def get_or_create_record(model, **kwargs):
    new_rec = model.query.filter_by(**kwargs).first()
    if new_rec:
        return new_rec
    else:
        # params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        # params.update(defaults or {})
        new_rec = model(**kwargs)
        session.add(new_rec)
        session.commit()
        return new_rec


#setting up a process timer
start_time = time.time()

#Using main app context to load db through SQLAlchemy ORM
#https://stackoverflow.com/questions/31444036/runtimeerror-working-outside-of-application-context
with app.app_context():
    session = db.session

# session = db.session

#https://chroniclingamerica.loc.gov/search/titles/results/?terms=michigan&format=json&page=5

    requests_cache.install_cache('loc_cache')

    baseurl = "https://chroniclingamerica.loc.gov/search/titles/results/"

    params={"format":"json","page":1,"rows":100}

    try:
        params['page'] = session.query(db.func.max(Paper.page)).scalar() or 1
    except:
        pass

    while True:
        req = requests.get(baseurl,params)
        result = req.json()
        cur_page = params['page']
        tot_page = -(-result['totalItems'] // params['rows'])
        print("Now retrieving page {} of {} pages {}".format(cur_page,tot_page, "(From Cache)" if req.from_cache == True else "            "), end="", flush=True)
        print("\r",end="", flush=True)
        for item in result['items']:
            # paper_mapper(item)
            pubname = item['publisher'] or 'Unknown'
            pub = get_or_create_record(Publisher,name=pubname)
            pubfreq = item['frequency'] or 'Unknown'
            freq = get_or_create_record(Frequency,frequency=pubfreq)
            if not Paper.query.filter_by(lccn=item['lccn']).first():
                paper = Paper(
                    title=item['title'],
                    place_of_publication = item['place_of_publication'] ,
                    start_year = item['start_year'],
                    end_year = item['end_year'],
                    notes = '\n'.join(item['note']),
                    alt_titles = '\n'.join(item['alt_title']),
                    lccn = item['lccn'],
                    page = cur_page,
                    publisher_id = pub.id,
                    frequency_id = freq.id)
                session.add(paper)
            else:
                paper = Paper.query.filter_by(lccn=item['lccn']).first()
            #Many-to-one relationships
            #Many-to-Many relationships - verifying integrity due to duplicates in data, then appending
            for state in item['state']:
                s = get_or_create_record(State,name=state)
                if s not in paper.states.all():
                    s.papers.append(paper)
            for place in item['place']:
                p = get_or_create_record(Place,place=place)
                if p not in paper.places.all():
                    p.papers.append(paper)
            for language in item['language']:
                l = get_or_create_record(Language,language=language)
                if l not in paper.languages.all():
                    l.papers.append(paper)
            for subject in item['subject']:
                subj = get_or_create_record(Subject,subject=subject)
                if subj not in paper.subjects.all():
                    subj.papers.append(paper)
        session.commit()
        end_rec = result['endIndex']
        tot = result["totalItems"]
        #for testing - 1 page
        # tot = 2000
        if end_rec >= tot: break
        params["page"] += 1
        #Sleeping between requests
        #Commenting out because integrity checks take long enough to count as a 'sleep'
        # time.sleep(5)

end_time = time.time()

print("\nProcess time:\n",time.strftime("%H:%M:%S", time.gmtime(end_time - start_time)))
# with open('test_string.txt',"w",encoding="utf8",newline="") as testfile:
#     testfile.write(first_result.text)
#
# print(len(first_result.json()['items']))
