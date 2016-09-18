# encoding: utf-8

"""Utilities."""

from __future__ import print_function, unicode_literals
import os
import re
import sys


# Paths & Files

def workflows_dirpaths():
    """List of paths of all installed Alfred workflows."""
    prefs = os.environ['alfred_preferences']  # Set by Alfred
    workflows = os.path.join(prefs, 'workflows')
    return _subdirpaths(workflows)


def iconpath(wf_obj, wf, dirpath=''):
    """The path to the icon for the workflow object `wf_obj` in `dirpath`.

    If the path doesn't exist, falls back to the icon of the parent workflow
    `wf` or the default workflow icon.

    """
    def p(x):
        return os.path.join(dirpath, x)

    paths = [p(wf_obj.icon), p(wf.icon), workflow_default_iconpath()]
    for p in paths:
        if os.path.isfile(p):
            return p
    return None


def workflow_default_iconpath(alfred_path='/Applications/Alfred 3.app'):
    """The path to Alfred's default workflow icon.

    Can't bundle cuz copyright.

    Since this is hard-coded, this is most likely not valid if:
        - Alfred 4 comes out
        - User installed Alfred in a custom location
        - Alfred changes the icon's location

    """
    icon = ('Contents/Frameworks/Alfred Framework.framework/Versions/A/'
            'Resources/workflow_default.png')
    return os.path.join(alfred_path, icon)


# Variables

def substitute(string, vars):
    """Return a copy of `string` where Alfred's variable placeholders
    `{var:<key>}` in `replacements` are replaced by their values.

    """
    if not vars:
        return string

    var = '{{var:{}}}'
    vars = _map_keys(lambda k: var.format(k), vars)
    return _replace(string, vars)


# Util^2

def _subdirpaths(dirpath):
    """List of paths for `dirpath`'s subdirectories."""
    for _, dirnames, _ in os.walk(dirpath):
        # Return immediately
        return [os.path.join(dirpath, d) for d in dirnames]
    return []


def _replace(string, replacements):
    """Return a copy of `string` where all occurrences of keys in
    `replacements` are replaced by their values.

    With help from: http://stackoverflow.com/a/15175239/4994382

    """
    def sub(match):
        m = match.string[match.start(): match.end()]
        return replacements[m]

    if not replacements:
        return string

    # Regex disjunction
    disj = map(re.escape, replacements.keys())
    disj = '|'.join(disj)
    disj = '({})'.format(disj)

    regex = re.compile(disj)
    return regex.sub(sub, string)


def _map_keys(function, d):
    """Return a dictionary where keys from `d` are mapped using `function`."""
    return {function(k): v for k, v in d.iteritems()}
