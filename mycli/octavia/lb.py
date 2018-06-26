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


class Info(command.Command):
    auth_required = True

    def get_parser(self, prog_name):
        parser = super(Info, self).get_parser(prog_name)

        parser.add_argument(
            '--loadbalancer',
            metavar='<loadbalancer>',
            help="Filter by load balancer ID.",
        )

        return parser

    def take_action(self, parsed_args):
        octavia = self.app.client_manager.load_balancer

        if parsed_args.loadbalancer:
            lbs = [octavia.load_balancer_show(lb_id=parsed_args.loadbalancer)]
        else:
            lbs = octavia.load_balancer_list()['loadbalancers']

        for lb in lbs:
            print(
                "- LoadBalancer: %s, name: %s, status: %s" %
                (lb['id'], lb['name'], lb['provisioning_status']))
            listener_ids = lb['listeners']
            # Can only get pools by loadbalancer id.
            pools = octavia.pool_list(loadbalancer_id=lb['id'])['pools']

            for listener in listener_ids:
                print("\t- Listener: %s" % listener['id'])

                for p in pools:
                    pool_listener_ids = [l['id'] for l in p['listeners']]
                    if listener['id'] in pool_listener_ids:
                        print("\t\t- Pool: %s" % p['id'])

                        member_ids = p['members']
                        for m in member_ids:
                            print("\t\t\t- Member: %s" % m['id'])

            for p in pools:
                if not p['listeners']:
                    print("\t- Shared Pool: %s" % p['id'])

                    member_ids = p['members']
                    for m in member_ids:
                        print("\t\t- Member: %s" % m['id'])
