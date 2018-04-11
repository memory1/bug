#!/usr/bin/python
# -*- coding: UTF-8 -*-

class bugInfo:
    """A simple example class"""
    def __init__(self,bug_id, create_time,reporter, assignee, cf_regression,priority,bug_severity):
        self.bug_id = bug_id
        self.create_time = create_time
        self.priority = priority
        self.bug_severity = bug_severity
        self.cf_regression = cf_regression
        self.assignee = assignee
        self.reporter = reporter

