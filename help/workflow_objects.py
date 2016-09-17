# encoding: utf-8

"""Wrappers around workflow `info.plist` files."""

from __future__ import print_function, unicode_literals
import os
import plistlib

# PyObjC
from AppKit import NSCommandKeyMask, NSAlternateKeyMask, \
                   NSControlKeyMask, NSShiftKeyMask


class Workflow(object):
    """Thin wrapper around a workflow `info.plist` file..

    Does not support all keys.

    """
    def __init__(self, plist):
        """`plist` is a dictionary as read from a workflow `info.plist` file."""
        self._store = plist

    @classmethod
    def from_dir(cls, dirpath):
        """Read a workflow from a directory, passing on any `plistlib` error."""
        return cls.from_plist(os.path.join(dirpath, 'info.plist'))

    @classmethod
    def from_plist(cls, path):
        """Read a workflow from a plist file, passing on any `plistlib` error."""
        return cls(plistlib.readPlist(path))

    # Keys

    @property
    def name(self):
        return self._store.get('name')

    @property
    def disabled(self):
        return self._store.get('disabled', False)

    @property
    def objects(self):
        objects = self._store.get('objects', [])
        return map(WorkflowObject, objects)

    @property
    def variables(self):
        return self._store.get('variables', {})

    # Computed

    @property
    def icon(self):
        return 'icon.png'

    def __repr__(self):
        pattern = '{}(name=\'{}\', objects=\'{}\')'
        return pattern.format(type(self).__name__,
                              self.name,
                              self.objects)


class WorkflowObject(object):
    """Thin wrapper around a single workflow object as read from a
    `info.plist` file.

    Does not support all keys.

    """
    def __init__(self, plist_obj):
        self._store = plist_obj

    # Top-level keys

    @property
    def uid(self):
        return self._store.get('uid')

    @property
    def type(self):
        return self._store.get('type')

    @property
    def config(self):
        return self._store.get('config', {})

    # Flattened config keys

    @property
    def title(self):
        return self.config.get('title')

    @property
    def text(self):
        return self.config.get('text')

    @property
    def subtext(self):
        return self.config.get('subtext')

    @property
    def keyword(self):
        return self.config.get('keyword')

    @property
    def withspace(self):
        return self.config.get('withspace')

    @property
    def hotstring(self):
        return self.config.get('hotstring')

    @property
    def hotmod(self):
        return self.config.get('hotmod')

    # Computed

    @property
    def maintext(self):
        return self.title or self.text

    @property
    def icon(self):
        return self.uid + '.png'

    @property
    def full_hotkey(self):
        if self.hotstring is None:
            return None

        mods = ''

        # In the order Alfred displays them
        if self._has_keymask(NSControlKeyMask):
            mods += '⌃'
        if self._has_keymask(NSAlternateKeyMask):
            mods += '⌥'
        if self._has_keymask(NSShiftKeyMask):
            mods += '⇧'
        if self._has_keymask(NSCommandKeyMask):
            mods += '⌘'

        return mods + self.hotstring

    def _has_keymask(self, mask):
        return _has_mask(self.hotmod or 0, mask)

    def __repr__(self):
        return '{}(\'{}\')'.format(type(self).__name__,
                                   str(self._store))


# Util

def _has_mask(flags, mask):
    return flags & mask != 0
