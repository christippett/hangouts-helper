from pkg_resources import get_distribution, DistributionNotFound


try:
    __version__ = get_distribution('hangouts-chat-util').version
except DistributionNotFound:
    __version__ = 'unknown'  # package not installed
