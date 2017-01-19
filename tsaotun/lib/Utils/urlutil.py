"""This module provides urlutils"""

import re

valid_prefixes = {
    'url': ['http://', 'https://'],
    'git': ['git://', 'github.com/', 'git@'],
    'transport': ['tcp://', 'tcp+tls://', 'udp://', 'unix://', 'unixgram://']
}

url_path_with_fragment_suffix = re.compile('.git(?:#.+)?$')


def is_url(url):
    """Check if the given url is valid"""
    return check_url(url, 'url')


def is_git_url(url):
    """Check if the given url is git url"""
    if is_url(url) and url_path_with_fragment_suffix.search(url):
        return True
    else:
        return check_url(url, 'git')

def is_git_transport(url):
    """Check if the given url is a git transport protocol"""
    return is_url(url) or url.startswith('git://') or url.startswith('git:@')

def is_transport_url(url):
    """Check if the given url is a valid transport protocol"""
    return check_url(url, 'transport')

def check_url(url, kind):
    """Main function to check if a url is a valid one within its kind"""
    for prefix in valid_prefixes[kind]:
        if url.startswith(prefix):
            return True
    return False
