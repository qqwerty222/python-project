import pymysql

from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="db",
            user="website",
            password="website_pass",
            database="company",
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

def db_execute(query):
    db = get_db().cursor()
    db.execute(query)

    return db.fetchall()
    
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

        
def db_data_workers():
    table = db_execute("SELECT * FROM workers")

    # .../api/workers/
    workers_ = {}
    # { 
    #   1: {
    #       name: frank
    #       team: orange
    #       tasks_received: 30
    #       tasks_in_progress: 10
    #       tasks_finished: 20
    #       tasks_coverage(%): 77.0
    #       }
    #   }   
    # }
    for worker in table:
        workers_[f"{worker['id']}"] = { 
            'name':                 f"{worker['name']}", 
            'team':                 f"{worker['team']}",
            'tasks_received':       int(f"{worker['tasks_received']}"),
            'tasks_in_progress':    int(f"{worker['tasks_in_progress']}"),
            'tasks_finished':       int(f"{worker['tasks_finished']}"),

            # count tasks coverage:  finished / ( received / 100 ) = coverage%
            'tasks_coverage(%)':       worker['tasks_finished'] // (worker['tasks_received'] / 100)
        }
    
    return workers_

def db_data_teams():
    table = db_execute("SELECT * FROM workers")
    
    #.../api/teams
    teams_ = {}
    # {
    #   lemon: {
    #       name: lemon
    #       size: 3
    #       workers: [
    #           "frank",
    #           "john",
    #           "bill",
    #       ]
    #       tasks: {
    #           received: 100
    #           in_progress: 30
    #           finished: 70
    #           coverage: 70%
    #       }
    # }

    teams_list = []

    for worker in table:

        if worker['team'] not in teams_list: 
            teams_list.append(f"{worker['team']}")

            # {'lemon': {}}
            teams_[f"{worker['team']}"] = {}
            # {'lemon': { workers: ['frank']}}
            teams_[f"{worker['team']}"]['workers'] = [f"{worker['name']}"]
            # {'lemon': { ..., size: 1}}
            teams_[f"{worker['team']}"]['size'] = 1
       
            # {'lemon': { ..., tasks: {received: 30, ..., coverage: 50%}}}
            teams_[f"{worker['team']}"]['tasks'] = { 
                'received':     worker['tasks_received'],
                'in_progress':  worker['tasks_in_progress'],
                'finished':     worker['tasks_finished'],
                }

            # {'lemon': { name: 'lemon'}} # workaround for jinja template parsing
            teams_[f"{worker['team']}"]['name'] = f"{worker['team']}"

        else:
            teams_[f"{worker['team']}"]['workers'].append(f"{worker['name']}")
            teams_[f"{worker['team']}"]['size'] += 1
            teams_[f"{worker['team']}"]['tasks']['received']    += worker['tasks_received']
            teams_[f"{worker['team']}"]['tasks']['in_progress'] += worker['tasks_in_progress']
            teams_[f"{worker['team']}"]['tasks']['finished']    += worker['tasks_finished']

    # for loop to count task coverage for each team 
    for team in teams_.values():
        team['tasks']['coverage(%)'] = team['tasks']['finished'] // (team['tasks']['received'] / 100)

    return teams_

def db_data_company():
    table = db_execute("SELECT * FROM workers")

    # .../api/common
    company_ = {}
    # {
    #   teams: 3
    #   workers:15
    #   tasks: {
    #       tasks_received: 150
    #       tasks_in_progress: 30
    #       tasks_finished: 120
    #       tasks_covered(%): 80
    #   }
    # }

    company_['size']    = len(db_data_teams())
    company_['workers'] = 0 
    company_['tasks'] = { 
        'received': 0,
        'in_progress': 0,
        'finished': 0,
        'coverage(%)': 0
    }
    
    for team in db_data_teams().values():
        company_['workers'] += len(team['workers']) 
        company_['tasks']['received'] += team['tasks']['received']
        company_['tasks']['in_progress'] += team['tasks']['in_progress']
        company_['tasks']['finished'] += team['tasks']['finished']
    
    company_['tasks']['coverage(%)'] = company_['tasks']['finished'] // (company_['tasks']['received'] / 100)

    return company_