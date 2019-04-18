# -*- coding: utf-8 -*-

import requests, requests_cache
import json
import time

#Importing main flask app file to use its context and database connection
import si507_final as fp

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

def paper_mapper(paper):
    session.add(
        fp.Paper(
            title=item['title'],
            place_of_publication = item['place_of_publication'] ,
            start_year = item['start_year'],
            end_year = item['end_year'],
            notes = '\n'.join(item['note']),
            alt_titles = '\n'.join(item['alt_title']),
            lccn = item['lccn'],
            # states = get_or_create_record(fp.State,name=item['state']),
            # place = get_or_create_record(fp.Place,place=item['place']),
            # publisher = get_or_create_record(fp.Publisher,name=item['publisher']),
            # frequency = get_or_create_record(fp.Frequency,frequency=item['frequency']),
            # language = get_or_create_record(fp.Language,language=item['language']),
            # subject = get_or_create_record(fp.Subject,subject=item['subject'])
        )
    )
#
#     )

#Using main app context to load db through SQLAlchemy ORM
#https://stackoverflow.com/questions/31444036/runtimeerror-working-outside-of-application-context
with fp.app.app_context():
    session = fp.db.session

#https://chroniclingamerica.loc.gov/search/titles/results/?terms=michigan&format=json&page=5

    requests_cache.install_cache('loc_cache')

    baseurl = "https://chroniclingamerica.loc.gov/search/titles/results/"

    params={"format":"json","page":1,"rows":100}

    while True:
        result = requests.get(baseurl,params).json()
        for item in result['items']:
            # paper_mapper(item)
            paper = fp.Paper(
                title=item['title'],
                place_of_publication = item['place_of_publication'] ,
                start_year = item['start_year'],
                end_year = item['end_year'],
                notes = '\n'.join(item['note']),
                alt_titles = '\n'.join(item['alt_title']),
                lccn = item['lccn'])
            session.add(paper)
            for state in item['state']:
                s = get_or_create_record(fp.State,name=state)
                # if not session.query(fp.State,fp.Paper).join('papers').filter_by(state_id=s.id,paper_id=paper.id):
                if s not in session.query(fp.State).with_parent(paper):
                    s.papers.append(paper)
                    # print(session.query(fp.State. fp.Paper).filter(fp.states.state_id == fp.State.id))
        # if s in session.query(fp.State).with_parent(paper):
        #     print('yes')
        session.commit()
        end_rec = result['endIndex']
        tot = result["totalItems"]
        #for testing - 1 page
        tot = 100
        if end_rec >= tot: break
        params["page"] += 1
        time.sleep(5)


# with open('test_string.txt',"w",encoding="utf8",newline="") as testfile:
#     testfile.write(first_result.text)
#
# print(len(first_result.json()['items']))
