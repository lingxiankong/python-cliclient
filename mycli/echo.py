# Copyright 2018 Catalyst IT Limited
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from osc_lib.command import command


class Echo(command.Command):
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(Echo, self).get_parser(prog_name)
        parser.add_argument(
            '-m', '--message', default='Hello, World!', help='Echo message.'
        )
        return parser

    def take_action(self, parsed_args):
        print(parsed_args.message)
