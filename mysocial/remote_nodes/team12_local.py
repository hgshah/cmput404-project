import json
import urllib.parse

import requests
from rest_framework import status
from rest_framework.response import Response

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from common.base_util import BaseUtil
from common.pagination_helper import PaginationHelper
from follow.models import Follow
from follow.serializers.follow_serializer import FollowRequestSerializer
from mysocial.settings import base
from post.serializer import PostSerializer
from remote_nodes.local_default import LocalDefault


class Team12Local(LocalDefault):
    domain = '127.0.0.1:8012'
    username = 'team12_local'
    team_metadata_tag = 'team12'

    """Mapping: remote <-> local"""
    remote_author_fields = {
        'id': 'official_id',
        'username': 'display_name',
        'github': 'github',
        'profile_image': 'profile_image'
    }

    post_remote_fields = {
        'id': 'official_id',
        'url': 'url',
        "title": "title",
        "source": "source",
        "origin": "origin",
        "description": "description",
        "contentType": "contentType",
        "image_url": "content",
        "author": "author",
        "categories": "categories",
        "published": "published",
        "visibility": "visibility",
        "unlisted": "unlisted"
    }

    def __init__(self):

        """
        To use headers:
            response = requests.get('url',
                                    headers=self.headers,
                                    auth=(self.username, self.password))
        """
        self.bearer_token = None

        super().__init__()

    @classmethod
    def create_node_credentials(cls):
        """This is for local testing"""
        return {
            cls.domain: {
                'username': cls.username,
                'password': 'team12_local',
                'remote_username': 'local_default@mail.com',
                'remote_password': 'local_default',
            }
        }

    def get_headers(self):
        """
        Use like:
            response = requests.get(url, headers=self.headers)
        """
        if self.bearer_token is None:
            try:
                payload = json.dumps({
                    "email": self.username,
                    "password": self.password
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.post(
                    f'{self.get_base_url()}/api/auth/token/obtain/',
                    data=payload,
                    headers=headers)
                if response.status_code == 200:
                    response_json: dict = json.loads(response.text)
                    self.bearer_token = response_json.get('access')

            except ConnectionError as err:
                print(f'{self}: headers: connection error: the other server at {self.get_base_url()} may not be up or '
                      f'too slow to respond')
            except Exception as e:
                print(f'{self}: headers: unknown error: {e}')

        if self.bearer_token is None:
            print(f'{self}: headers: bearer token still empty')

        return {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }

    def get_all_followers(self, author: Author, params=None):
        if params is None:
            # python has a weird property that if the argument is mutable, like a dictionary
            # if you pass the reference around, you can actually change the default values,
            # like params here. doing this to prevent evil things
            params = {}

        url = f'{author.get_url()}/followers/'
        if len(params) > 0:
            query_param = urllib.parse.urlencode(params)
            url += '?' + query_param
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            response_json = json.loads(response.text)
            # team12 oddities
            if 'posts' in response_json:
                print('Team12 local returns weird for followers. If this appears in prod: uh-oh!')
                return []

            # clean up process
            for author_data in response_json:
                _, host, path, _, _, _ = urllib.parse.urlparse(author_data['host'])
                node_config = base.REMOTE_CONFIG.get(host)
                if node_config is None:
                    data_host = author_data['host']
                    print(f"AuthorSerializer: Host not found: {host} for {data_host}")
                    continue

                # todo
                remote_fields: dict = node_config.remote_author_fields

                # sender id
                # host
                pass

            return AuthorSerializer.deserializer_author_list(response.content.decode('utf-8'))
        return None

    def get_all_author_jsons(self, params: dict):
        """Returns a list of authors as json"""
        url = f'{self.get_base_url()}/authors/'
        if len(params) > 0:
            query_param = urllib.parse.urlencode(params)
            url += '?' + query_param

        try:
            response = requests.get(url, headers=self.get_headers())
        except ConnectionError:
            print(f'Connection error: {self}')
            return None
        except Exception as e:
            print(f"NodeConfigBase: Unknown err: {str(e)}")
            return None

        if response.status_code == 200:
            return AuthorSerializer.deserializer_author_list(response.content.decode('utf-8'))
        return None

    def get_author_via_url(self, author_url: str) -> Author:
        author_url = author_url.rstrip('/')
        author_url = f'{author_url}/'
        response = requests.get(author_url, headers=self.get_headers())

        if response.status_code == 200:
            author_json = json.loads(response.content.decode('utf-8'))
            author_json['url'] = author_url  # since we don't trust their url; this works
            serializer = AuthorSerializer(data=author_json)

            if serializer.is_valid():
                return serializer.validated_data  # <- GOOD RESULT HERE!!!

            print(f'{self} GetAuthorViaUrl: AuthorSerializer: ', serializer.errors)

        return None
    
    def get_authors_posts(self, request, author_posts_path):
        url = f'{self.get_base_url()}{author_posts_path}'

        try:
            response = requests.get(url, headers=self.get_headers())
            if response.status_code < 200 or response.status_code > 300:
                return Response("Failed to get author's  post from remote server",
                                status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response(f"Failed to get author's post from remote server, error: {e}",
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = []
        post_data = json.loads(response.content.decode('utf-8'))
        
        for post in post_data:
            data.append(self.convert_team12_post(url, post))

        data, err = PaginationHelper.paginate_serialized_data(request, data)

        if err is not None:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'type': 'posts', 'items': data}, status=status.HTTP_200_OK)
    
    def get_post_by_post_id(self, post_url):
        url = f'{self.get_base_url()}{post_url}'

        try:
            response = requests.get(url, headers=self.get_headers())

            if response.status_code < 200 or response.status_code > 300:
                return Response("Failed to get post from remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response(f"Failed to get author's post from remote server, error: {e}",
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        post_data = json.loads(response.content.decode('utf-8'))

        post = self.convert_team12_post(url, post_data)
        return Response(post, status=status.HTTP_200_OK)
    
    def convert_team12_post(self, url, post):
        post["url"] = url

        serializer = PostSerializer(data=post)
        if serializer.is_valid():
            return serializer.data
        else:
            return serializer.errors