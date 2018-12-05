#!/usr/bin/env python
# -*- coding: utf8 -*-
from planting.planting_module import ModuleBase


class Fetch(ModuleBase):
    """

    copy files from remote machine to local machine

    Args:
        src(str): remote path
        dest(str): local path
    """
    def __init__(self):
        super(Fetch, self).__init__()

    def build_tasks(self, src, dest):
        self._tasks = [dict(action=dict(
            module='fetch',
            args=dict(src=src, dest=dest)))]

    def output_field(self):
        self._output = 'changed'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.fetch = self

    def __call__(self, src, dest):
        self.build_tasks(src, dest)
        return self.play()
