# encoding: utf-8

"""Creates Alfred feedback items from workflows."""

from __future__ import print_function, unicode_literals
import util


def items(workflow, dirpath, title_pref='keyword'):
    """List of feedback item dicts for a workflow.

    If `title_pref` is `keyword`, keywords and hotkeys will be displayed as
    titles in Alfred. Otherwise the titles of the objects themselves will be
    used.

    `dirpath` is the directory the workflow was read from.

    """
    def item(obj):
        """Feedback item dict for a single workflow object."""
        title, subtitle = titles(obj)
        icon = iconpath(obj)
        valid = (obj.keyword is not None) and (not workflow.disabled)
        arg_whitespace = ' ' if obj.withspace else ''
        arg = (obj.keyword + arg_whitespace) if obj.keyword else ''

        # Replace `{var:<name>}` placeholders
        title = sub(title)
        subtitle = sub(subtitle)
        arg = sub(arg)

        return {
            'title': title,
            'subtitle': subtitle,
            'icon': icon,
            'valid': valid,
            'arg': arg,
            'autocomplete': title,
            'copytext': title,
            'largetext': title
        }

    def iconpath(obj):
        return util.iconpath(obj, workflow, dirpath=dirpath)

    def sub(s):
        return util.substitute(s, workflow.variables)

    def titles(obj):
        keyword = obj.keyword or obj.full_hotkey
        if title_pref == 'keyword':
            titles = (keyword, obj.maintext, obj.subtext)
        else:
            titles = (obj.maintext, keyword, obj.subtext)
        title = titles[0] or workflow.name or ''
        if titles[1] and titles[2]:
            subtitle = '{}   |   {}'.format(titles[1], titles[2])
        else:
            subtitle = titles[1] or titles[2] or workflow.name or ''
        return title, subtitle

    # Interested only in keywords and hotkeys
    objects = [obj for obj in workflow.objects if obj.keyword or obj.hotstring]
    return map(item, objects)        
