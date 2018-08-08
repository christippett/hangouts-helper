from pkg_resources import get_distribution, DistributionNotFound


try:
    __version__ = get_distribution('hangouts-helper').version
except DistributionNotFound:
    __version__ = 'unknown'  # package not installed
