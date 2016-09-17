#!/usr/bin/env python
# encoding: utf-8
# https://github.com/arthurhammer/alfred-workflows

"""Main entry point for the Help Alfred Workflow."""

from __future__ import print_function, unicode_literals
import sys

import feedback
import util
from workflow_objects import Workflow

from vendor.workflow import Workflow3 as AlfredWorkflow


def read_workflows():
    workflows = []
    for dirpath in util.workflows_dirpaths():
        try:
            workflow = Workflow.from_dir(dirpath)
        except Exception as e:
            msg = 'Couldn\'t read workflow from directory {}. Reason: {}\nSkipping.\n'
            sys.stderr.write(msg.format(dirpath, e))
            continue
        workflows.append((dirpath, workflow))
    return workflows


def from_cache(alfred):
    return alfred.cached_data('workflows', read_workflows, max_age=60)


def main():
    # Args
    args = sys.argv
    title_pref = args[1] if (len(args) == 2) else None
    if title_pref not in ['keyword', 'title']:
        title_pref = 'keyword'

    include_disabled = False

    # Get workflows
    alfred = AlfredWorkflow()
    workflows = from_cache(alfred)
    workflows.sort(key=lambda p: p[1].name)

    # Massage into feedback
    for dirpath, workflow in workflows:
        if not workflow.disabled or include_disabled:
            items = feedback.items(workflow,
                                   dirpath=dirpath,
                                   title_pref=title_pref)
            for item in items:
                alfred.add_item(**item)

    alfred.send_feedback()


if __name__ == '__main__':
    main()
