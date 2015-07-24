#!/usr/bin/python3

"""autocomment.py: Replies to all timeline posts between two dates."""

__author__ = 'Alex Cristian, Andrei Muntean'

import json
from sys import path
path.insert(0, "dependencies")

# Custom dependencies.
from facepy import GraphAPI

def to_ascii_string(value):
    """A workaround for one of the many dubious Python design decisions."""
    return str(value.encode('ascii', 'ignore'))

def get_posts(user_id, since, until, limit):
    """Gets all (user timeline) posts from a specified period."""

    query = '{0}/feed?since={1}&until={2}&limit={3}'.format(user_id, since, until, limit)
    
    return graph.get(query)['data']

def initialize(access_token_path):
    global graph

    # Reads the user access token.
    # You can get one from https://developers.facebook.com/tools/explorer.
    access_token = open(access_token_path).read()
    
    # Connects to Facebook.
    graph = GraphAPI(access_token)

def run():
    initialize('access-token.txt')

    # Gets the user id.
    user_id = graph.get('me?fields=id')['id']

    # Determines the period from which to get the posts.
    since = input('Start Date (e.g. 15february2015): ')
    until = input('End Date (e.g. 4march2015): ')
    limit = input('Post Limit (e.g. 80): ')

    # Gets the posts from the specified period.
    posts = get_posts(user_id, since, until, limit)

    for post in posts:
        # TODO.
        post_id = post['id']
        message = to_ascii_string(post['message']) if 'message' in post else ''
        created_time = post['created_time']

if __name__ == '__main__':
    run()