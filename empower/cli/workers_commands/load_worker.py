#!/usr/bin/env python3
#
# Copyright (c) 2019 Roberto Riggio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

"""Load a worker. """

import argparse

import empower_core.command as command


def pa_cmd(args, cmd):
    """Load a worker parser method. """

    usage = "%s <options>" % command.USAGE.format(cmd)
    desc = command.DESCS[cmd]

    parser = argparse.ArgumentParser(usage=usage, description=desc)

    required = parser.add_argument_group('required named arguments')

    required.add_argument('-n', '--name', help='The app name',
                          required=True, type=str, dest="name")

    (args, leftovers) = parser.parse_known_args(args)

    return args, leftovers


def do_cmd(gargs, args, leftovers):
    """Load a worker. """

    request = {
        "version": "1.0",
        "name": args.name,
        "params": command.get_params(leftovers)
    }

    headers = command.get_headers(gargs)

    url = '/api/v1/workers'
    response, _ = command.connect(gargs, ('POST', url), 201, request,
                                  headers=headers)

    location = response.headers['Location']
    tokens = location.split("/")
    worker_id = tokens[-1]

    url = '/api/v1/workers/%s' % worker_id
    _, data = command.connect(gargs, ('GET', url), 200, headers=headers)

    print(data['service_id'])
