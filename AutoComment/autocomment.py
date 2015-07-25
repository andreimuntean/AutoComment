#!/usr/bin/python3

"""autocomment.py: Replies to all timeline posts between two dates."""

__author__ = 'Alex Cristian, Andrei Muntean'
__license__ = 'MIT License'

import json
from datetime import datetime
from replymanager import filter_posts
from replymanager import generate_comment
from sys import path

# Extends the path to load additional dependencies.
path.insert(0, 'dependencies')

from facepy import GraphAPI


def ascii_print(value):
    """Prevents the program from crashing when trying to print non-ASCII characters.
    A workaround for one of the many dubious Python design decisions."""
    
    print(str(value.encode('ascii', 'ignore')))


def to_datetime(datetime_string):
    """Parses a Facebook time string into a Python datetime."""

    return datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S+0000')


def get_posts(graph, user_id, since, until, limit):
    """Gets all (user timeline) posts from a specified period."""

    query = '{0}/feed?since={1}&until={2}&limit={3}'.format(user_id, since, until, limit)
    query += '&fields=id,from,to,message,created_time,type'
    posts = graph.get(query)['data']

    # Parses the posts into a more functional format.
    posts = list(map(lambda post: {
        'id': post['id'],
        'receiver_id': post['to']['data'][0]['id'] if 'to' in post else '',
        'author': post['from']['name'],
        'message': post['message'] if 'message' in post else '',
        'has_photo': post['type'] == 'photo',
        'created_time': to_datetime(post['created_time'])
        }, posts))

    # Filters the posts and returns them.
    return filter_posts(user_id, posts)


def reply_to_posts(posts, also_print_to_stdout = False):
    """Generates comments and replies to each individual post."""

    for post in posts:
        # Generates a comment based on this post.
        comment = generate_comment(post['author'], post['message'], post['has_photo'], post['created_time'])

        # Replies to this post.
        # graph.post(
        #     path = post_id + '/comments',
        #     message = comment
        # )

        if also_print_to_stdout:
            ascii_print('Replied to {0} with "{1}".'.format(post['author'], comment))


def run():
    # Reads the user access token.
    # You can get one from https://developers.facebook.com/tools/explorer.
    access_token = open('access-token.txt').read()
    
    # Connects to Facebook.
    graph = GraphAPI(access_token)

    # Gets the user id.
    user_id = graph.get('me')['id']

    # Determines the period from which to get the posts.
    since = input('Start Date (e.g. 15february2015): ')
    until = input('End Date (e.g. 4march2015): ')
    limit = input('Post Limit (e.g. 80): ')

    # Gets the posts from the specified period.
    posts = get_posts(graph, user_id, since, until, limit)

    # Replies to every post and prints the results.
    reply_to_posts(posts, True)


if __name__ == '__main__':
    run()