#!/usr/bin/python3

"""autocomment.py: Replies to all timeline posts between two dates."""

__author__ = 'Alex Cristian, Andrei Muntean'
__license__ = 'MIT License'

import json
from datetime import datetime
from replymanager import filter_posts
from replymanager import generate_comment
from facepy import GraphAPI


def ascii_print(value):
    """Prevents the program from crashing when trying to print non-ASCII characters.
    A workaround for one of the many dubious Python design decisions."""
    
    print(str(value.encode('ascii', 'ignore')))


def to_datetime(datetime_string):
    """Parses a Facebook time string into a Python datetime."""

    return datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S+0000')


def get_posts(graph, since, until, limit):
    """Gets all (user timeline) posts from a specified period."""

    posts = graph.get('me/feed',
        fields = 'id,from,to,message,created_time,type'
            + ',comments.limit(0).summary(true)'
            + ',likes.limit(0).summary(true)',
        since = since,
        until = until,
        limit = limit)['data']

    # Parses the posts into a more functional format.
    posts = list(map(lambda post: {
        'id': post['id'],
        'receiver_id': post['to']['data'][0]['id'] if 'to' in post else '',
        'author': post['from']['name'],
        'message': post['message'] if 'message' in post else '',
        'has_photo': post['type'] == 'photo',
        'created_time': to_datetime(post['created_time']),
        'comment_count': int(post['comments']['summary']['total_count']),
        'like_count': int(post['likes']['summary']['total_count'])
        }, posts))

    # Filters the posts and returns them.
    return filter_posts(graph.get('me')['id'], posts)


def reply_to_posts(posts, also_print_to_stdout = False):
    """Generates comments and replies to each individual post."""

    for post in posts:
        # Generates a comment based on this post.
        comment = generate_comment(post)

        # Replies to this post.
        # graph.post(
        #     path = post_id + '/comments',
        #     message = comment
        # )

        if also_print_to_stdout:
            ascii_print('{0} said: {1}'.format(post['author'], post['message']))
            ascii_print('You replied: ' + comment)
            print()


def run():
    # Reads the user access token.
    # Permissions required: 'user_posts', 'user_friends', 'publish_actions'.
    # You can get one from https://developers.facebook.com/tools/explorer.
    access_token = open('access-token.txt').read()
    
    # Connects to Facebook.
    graph = GraphAPI(access_token)

    # Determines the period from which to get the posts.
    since = input('Start Date (e.g. 15february2015): ')
    until = input('End Date (e.g. 4march2015): ')

    # Gets the posts from the specified period.
    posts = get_posts(graph, since, until, 80)

    # Replies to every post and prints the results.
    reply_to_posts(posts, True)


if __name__ == '__main__':
    run()