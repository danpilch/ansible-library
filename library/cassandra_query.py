#!/usr/bin/python

try:
    import json
    from cassandra.cluster import Cluster
    from cassandra import ConsistencyLevel
    from cassandra import util
    from cassandra.auth import PlainTextAuthProvider
    from cassandra.query import SimpleStatement
    HAS_LIB = True
except:
    HAS_LIB = False

DOCUMENTATION = '''
module: cassandra_query
short_description: Performs a query against a Cassandra cluster.
description:
  - Performs a query against a Cassandra database and returns an iterative dataset based on key-value pairs (column-value).
version_added: "2.0"
options:



'''

class cassandra_query(object):

    """ Initialise """
    def __init__(self, module):
        self.module = module
        self.login_hosts = module.params['login_hosts'].split(',')
        self.consistency = module.params['consistency']
        self.login_port = module.params['login_port']
        self.login_user = module.params['login_user']
        self.login_password = module.params['login_password']
        self.query = module.params['query']

        self.consistency_level = ConsistencyLevel.ONE
        self.session = None

    """ Connect to Cassandra """
    def connection(self):
        try:
            cluster = Cluster(self.login_hosts, auth_provider=PlainTextAuthProvider(username=self.login_user, password=self.login_password), port=self.login_port)
            self.session = cluster.connect()
        except Exception as e:
            self.module.fail_json(msg="Failed to create Cassandra connection: {0}".format(e))        
   
    """ Close connection to Cassandra """
    def close(self):
        self.session.cluster.shutdown()
        self.session.shutdown()

    """ Query Cassandra """
    def query_ks(self):
        try: 
            self.consistency_level = getattr(ConsistencyLevel, self.consistency)
        except Exception as e:
            self.module.fail_json(msg="Failed to set consistency level: {0}".format(e))
        try: 
            query = SimpleStatement(self.query, consistency_level=self.consistency_level)
            self.resultset = self.session.execute(query)
        except Exception as e:
            self.close()
            self.module.fail_json(msg="Failed to execute query: {0}".format(e))

    """ Parse Cassandra resultset to json """
    def parse(self):
        try:
            parsed_results = [ dict(line) for line in [[(field, getattr(row, field, None)) for field in row._fields] for row in self.resultset] ]
            self.close()
            return parsed_results
        except Exception as e:
           self.close()
           self.module.fail_json(msg="Failed to parse resultset: {0}".format(e))

class SetEncoder(json.JSONEncoder):
   def default(self, obj):
      if isinstance(obj, util.sortedset):
         return list(obj)
      if isinstance(obj, util.OrderedMapSerializedKey):
         return list(obj)
      return json.JSONEncoder.default(self, obj)

def main():

    if not HAS_LIB:
        module.fail_json(msg="Could not import python cassandra-driver package.")

    module = AnsibleModule(
        argument_spec = dict(
            login_user = dict(required=True),
            login_password = dict(required=True),
            login_hosts = dict(default=['localhost']),
            login_port = dict(default=9042),
            consistency = dict(default='ONE'),
            query = dict(required=True),
            fact_name = dict(default='cassandra_query_resultset'),
            ),
        )

    run = cassandra_query(module)
    run.connection()
    run.query_ks()
    run.close()
    resultset = run.parse()
    print json.dumps({ "ansible_facts": { module.params['fact_name']: resultset } }, cls=SetEncoder)

from ansible.module_utils.basic import *

main()
