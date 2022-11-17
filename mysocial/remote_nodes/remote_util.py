import json
import os

from drf_spectacular.utils import OpenApiParameter
from rest_framework.request import Request

from authors.models.author import Author, AuthorType
from common.pagination_helper import PaginationHelper
from common.test_helper import TestHelper
from mysocial.settings import base
from remote_nodes.macewan import MacEwan
from remote_nodes.potato_oomfie import PotatoOomfie
from remote_nodes.team14_local import Team14Local
from remote_nodes.team14_main import Team14Main
from remote_nodes.turnip_oomfie import TurnipOomfie
from remote_nodes.ualberta import UAlberta
from remote_nodes.local_default import LocalDefault
from remote_nodes.local_mirror import LocalMirror


class RemoteUtil:
    """
    Remote node configs

    This is where both test and production configurations of each configs are accessible. It's
    a key-value pair of the domain and the corresponding logic of how to call the server and map
    the values into something our internal code can understand.
    """

    NODE_TARGET_QUERY_PARAM = 'node-target'
    REMOTE_IMPLEMENTED_TAG = 'remote implemented'
    REMOTE_WIP_TAG = 'remote wip'

    REMOTE_NODE_SINGLE_PARAMS = [
        OpenApiParameter(name=NODE_TARGET_QUERY_PARAM, location=OpenApiParameter.QUERY,
                         description='The domain name for the remote node we want to target. For example: '
                                     '`?node-target=app.herokuapp.com`. We currently support the following nodes:\n'
                                     '- Main endpoints\n'
                                     '    - Our stable endpoint: [WIP]\n '
                                     '- Other connected endpoints\n'
                                     '    - [WIP]\n '
                                     '- Staging endpoints (unstable)\n'
                                     '    - potato-oomfie.herokuapp.com\n '
                                     '    - turnip-oomfie-1.herokuapp.com\n',
                         required=False, type=str),
    ]

    REMOTE_NODE_MULTIL_PARAMS = REMOTE_NODE_SINGLE_PARAMS + PaginationHelper.OPEN_API_PARAMETERS

    @staticmethod
    def setup():
        """
        Setup all remote node configs and logic
        """
        connected_nodes = ()
        if '127.0.0.1' in base.CURRENT_DOMAIN:
            connected_nodes = (LocalDefault, LocalMirror, Team14Local)
        else:
            connected_nodes = (TurnipOomfie, PotatoOomfie, UAlberta, MacEwan, Team14Main)

        # special remote node configs if you're running locally
        # you may add (or even override) your node here or via the REMOTE_NODE_CREDENTIALS config (see docs/server.md)
        if '127.0.0.1' in base.CURRENT_DOMAIN:
            # tricky technique to make the user's config var override ours; useful for other teams!
            local_credentials: dict = {}
            for node in connected_nodes:
                local_credentials.update(node.create_node_credentials())
            # then set it back to our app's remote credentials
            base.REMOTE_NODE_CREDENTIALS = local_credentials

        # setup remote config node type authors
        for host, credentials in base.REMOTE_NODE_CREDENTIALS.items():
            node: Author = TestHelper.overwrite_node(credentials['username'], credentials['password'],
                                                     credentials['remote_username'], credentials['remote_password'],
                                                     host)
            is_active = credentials.get('is_active')
            if is_active is None and not isinstance(is_active, bool):
                continue
            elif is_active:
                node.author_type = AuthorType.ACTIVE_REMOTE_NODE
            else:
                node.author_type = AuthorType.INACTIVE_REMOTE_NODE

        # todo: setup superuser???
        if 'PREFILLED_USERS' in os.environ:
            prefilled_users = json.loads(os.environ['PREFILLED_USERS'])
            # prefilled_users: dict = {
            #     'items': [{'username': 'super', 'password': 'super', 'is_staff': True, 'email': "super@gmail.com"}]}
            for user in prefilled_users['items']:
                username = user['username']
                other_args: dict = user
                other_args.pop('username')
                TestHelper.overwrite_author(username, other_args)

        # This is where the endpoints and configs are added!
        # When it's local (contains 127.0.0.1), we add 127.0.0.1:8000 and 127.0.0.1:8080
        # Then, we add the endpoints, like turnip-oomfie-1.herokuapp.com (TurnipOomfie)
        for config in connected_nodes:
            base.REMOTE_CONFIG.update(config.create_dictionary_entry())

    @staticmethod
    def extract_node_target(request: Request):
        """
        :param request:
        :return: Either (None, None) if the param does not exist
        or a (string, dict) if it does. Dict here is the request query parameters without the added node
        """
        if RemoteUtil.NODE_TARGET_QUERY_PARAM not in request.query_params:
            return None, None
        node_param = request.query_params[RemoteUtil.NODE_TARGET_QUERY_PARAM]
        new_dict = request.query_params.copy()
        new_dict.pop(RemoteUtil.NODE_TARGET_QUERY_PARAM)
        return node_param, new_dict

    @staticmethod
    def get_node_config(node_param: str):
        if node_param not in base.REMOTE_CONFIG:
            return None
        return base.REMOTE_CONFIG[node_param]