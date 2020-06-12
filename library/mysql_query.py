#!/usr/bin/python

try:
    import MySQLdb
    HAS_LIB = True
except:
    HAS_LIB = False

DOCUMENTATION = '''
module: mysql_query
short_description: Performs a query against a MySQL database.
description:
  - Performs a query against a MySQL database and returns an iterative dataset based on key-value pairs (column-value).
version_added: "2.0"
options:



'''

class mysql_query(object):

    """ initialise """
    def __init__(self, module):
        self.module = module
        self.host = module.params['login_host']
        self.db = module.params['db_name']
        self.port = module.params['login_port']
        self.user = module.params['login_user']
        self.passwd = module.params['login_password']
        self.query = module.params['query']

    """ Connect to MySQLdb """
    def connection(self):
        config = {
            'host': self.host,
            'db': self.db,
            'port': self.port,
            'user': self.user,
            'passwd': self.passwd
        }

        try:
            self.connection = MySQLdb.Connection(**config)
            self.cursor = self.connection.cursor()
        except Exception as e:
            self.module.fail_json(msg="Failed to create MySQL connection: {0}".format(e))        
    
    """ Query MySQLdb """  
    def query_db(self):
        try:
            self.cursor.execute(self.query)
        except Exception as e:
            self.cursor.close()
            self.module.fail_json(msg="Failed to execute query: {0}".format(e))
  
    """ Parse MySQL resultset to json """
    def parse(self):
        try:
            parsed_results = [ dict(line) for line in [zip([ column[0] for column in self.cursor.description], row) for row in self.cursor.fetchall()] ]
            print parsed_results
            self.cursor.close()
            return parsed_results
        except Exception as e:
            self.cursor.close()
            self.module.fail_json(msg="Failed to parse resultset: {0}".format(e))


def main():

    if not HAS_LIB:
        module.fail_json(msg="Could not import MySQLdb package.")

    module = AnsibleModule(
        argument_spec = dict(
            login_user = dict(required=True),
            login_password = dict(required=True),
            login_host = dict(default='localhost'),
            login_port = dict(default=3306),
            db_name = dict(required=True),
            query = dict(required=True),
            fact_name = dict(default='mysql_query_resultset'),
            ),
        )

    run = mysql_query(module)
    run.connection()
    run.query_db()
    resultset = run.parse()
    print json.dumps({ "ansible_facts": { module.params['fact_name']: resultset } })

from ansible.module_utils.basic import *

main()
