#!/usr/bin/python3

"""replymanager.py: A flexible script for filtering posts and generating replies."""

__author__ = 'Alex Cristian, Andrei Muntean'
__license__ = 'MIT License'


def filter_posts(user_id, posts):
    """Filters a list of posts.

    Arguments:
        user_id: string. The id of the user from whose timeline the posts were taken.
        posts: list of posts. Each post is a dictionary of the form:
              'id': string. The Facebook post id.
              'receiver_id': string. The id of the user on whose timeline this post appears.
                  Empty string if no receiver (e.g. it is a status update).
              'author': string. The name of the post author.
              'message': string. The post message. Empty string if no message.
              'has_photo': boolean. Determines whether the post has a photo attachment.
              'created_time': datetime. The time at which the post was created.
              'comment_count': integer. The number of comments on the post.
              'like_count': integer. The number of people that like the post.

    Returns a list of posts.
    """

    return posts


def generate_comment(post):
    """Generates a comment for the specified post.

    Arguments:
        post: a dictionary of the form:
            'id': string. The Facebook post id.
            'receiver_id': string. The id of the user on whose timeline this post appears.
                Empty string if no receiver (e.g. it is a status update).
            'author': string. The name of the post author.
            'message': string. The post message. Empty string if no message.
            'has_photo': boolean. Determines whether the post has a photo attachment.
            'created_time': datetime. The time at which the post was created.
            'comment_count': integer. The number of comments on the post.
            'like_count': integer. The number of people that like the post.

    Returns a string.
    """

    return ''