# -*- coding: utf-8 -*-

import requests, requests_cache
import json
import time

#Importing main flask app file to use its context and database connection
import SI507_final as fp

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
            pubname = item['publisher'] or 'Unknown'
            pub = get_or_create_record(fp.Publisher,name=pubname)
            pubfreq = item['frequency'] or 'Unknown'
            freq = get_or_create_record(fp.Frequency,frequency=pubfreq)
            paper = fp.Paper(
                title=item['title'],
                place_of_publication = item['place_of_publication'] ,
                start_year = item['start_year'],
                end_year = item['end_year'],
                notes = '\n'.join(item['note']),
                alt_titles = '\n'.join(item['alt_title']),
                lccn = item['lccn'],
                publisher_id = pub.id,
                frequency_id = freq.id)
            if not fp.Paper.query.filter_by(lccn=paper.lccn).first():
                session.add(paper)
            #Many-to-one relationships
            #Many-to-Many relationships - verifying integrity due to duplicates in data, then appending
            for state in item['state']:
                s = get_or_create_record(fp.State,name=state)
                if s not in session.query(fp.State).with_parent(paper):
                    s.papers.append(paper)
            for place in item['place']:
                p = get_or_create_record(fp.Place,place=place)
                if p not in session.query(fp.Place).with_parent(paper):
                    p.papers.append(paper)
            for language in item['language']:
                l = get_or_create_record(fp.Language,language=language)
                if l not in session.query(fp.Language).with_parent(paper):
                    l.papers.append(paper)
            for subject in item['subject']:
                subj = get_or_create_record(fp.Subject,subject=subject)
                if subj not in session.query(fp.Subject).with_parent(paper):
                    subj.papers.append(paper)
        session.commit()
        end_rec = result['endIndex']
        tot = result["totalItems"]
        #for testing - 1 page
        # tot = 100
        if end_rec >= tot: break
        params["page"] += 1
        #Sleeping between requests
        #Commenting out because integrity checks take long enough to count as a 'sleep'
        # time.sleep(5)

end_time = time.time()

print("Process time:\n",time.strftime("%H:%M:%S", time.gmtime(end_time - start_time)))
# with open('test_string.txt',"w",encoding="utf8",newline="") as testfile:
#     testfile.write(first_result.text)
#
# print(len(first_result.json()['items']))
