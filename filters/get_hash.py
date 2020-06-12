import re

def get_commit_hash(filename):
    """ Grab the commit hash from the end of a filename """
    commit_hash = re.search('.*-(.*).tbz', filename).group(1)

    return commit_hash


class FilterModule(object):

    def filters(self):
        return { 'get_commit_hash': get_commit_hash, }
