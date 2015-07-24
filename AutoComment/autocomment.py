#!/usr/bin/python3

"""autocomment.py: Replies to all timeline posts between two dates."""

__author__ = 'Alex Cristian, Andrei Muntean'

import json
from sys import path
path.insert(0, "dependencies")
from facepy import GraphAPI

def initialize(access_token_path):
    global graph

    # Reads the user access token.
    # You can get one from https://developers.facebook.com/tools/explorer.
    access_token = open(access_token_path).read()
    
    # Connects to Facebook.
    graph = GraphAPI(access_token)

def to_ascii_string(value):
    """A workaround for one of the many dubious Python design decisions."""
    
    return str(value.encode('ascii', 'ignore'))

def get_posts(user_id, since, until, limit):
    """Gets all (user timeline) posts from a specified period."""

    query = '{0}/feed?since={1}&until={2}&limit={3}&fields=id,from,to,message,created_time,type'.format(user_id, since, until, limit)
    posts = graph.get(query)['data']

    # Returns the posts which were directed to this user.
    return [post for post in posts if 'to' in post and post['to']['data'][0]['id'] == user_id]

def generate_message(post_message, post_author_name, post_has_picture, post_created_time):
    # TODO.
    pass

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
        post_id = post['id']
        post_author_name = to_ascii_string(post['from']['name'])
        post_has_picture = post['type'] == 'photo'
        post_message = to_ascii_string(post['message']) if 'message' in post else ''
        post_created_time = post['created_time']

        # Generates a message based on this post.
        message = generate_message(post_message, post_author_name, post_has_picture, post_created_time)

        # Replies to this post.
        # graph.post(
        #     path = post_id + '/comments',
        #     message = message
        # )

        print('Replied to {0}.'.format(post_author_name))

if __name__ == '__main__':
    run()