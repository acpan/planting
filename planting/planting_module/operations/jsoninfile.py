#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
from planting.planting_module import ModuleBase
from functools import reduce
import json


class Jsoninfile(ModuleBase):

    def __init__(self):
        super(Jsoninfile, self).__init__()

    def build_tasks(self, path, keys, val):
        def str_splice(str_a, str_b):
            if isinstance(str_b, int):
                return str_a + ',' + str(str_b)
            else:
                return str_a + ',\"' + str_b + '\"'
        keys[0] = '\"' + keys[0] + '\"'
        key_series = reduce(str_splice, keys)
        key_series = '[' + key_series + ']'
        dir_path = os.path.dirname(path)
        if isinstance(val, dict) or isinstance(val, list):
            val = json.dumps(val)
            shell_jq = "cat {0} | jq \'setpath({1}; {2})\' > {3}/new | " \
                "mv {3}/new {0}".format(path, key_series,
                                        val, dir_path)
        else:
            if isinstance(val, str):
                shell_jq = "cat {0} | jq \'setpath({1}; \"{2}\")\' > {3}/new" \
                    " | mv {3}/new {0}".format(path, key_series,
                                               val, dir_path)
            else:
                shell_jq = "cat {0} | jq \'setpath({1}; {2})\' > {3}/new | " \
                    "mv {3}/new {0}".format(path, key_series,
                                            val, dir_path)

        print(shell_jq)
        self._tasks = [dict(action=dict(
            module='shell',
            args=shell_jq)
            )]

    def output_field(self):
        self._output = 'changed'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.jsoninfile = self

    def __call__(self, path: str, keys: list, val):
        self.build_tasks(path, keys, val)
        return self.play()
