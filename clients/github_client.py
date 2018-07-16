import os
import re

from clients.base import BaseClient


class GitHubClient(BaseClient):
    """
    Required to interface with three of GitHubs APIs:
    - Users API (users profile data)
    - Activity API (users starred repos)
    - Repositories API (data on repos)
    """
    def __init__(self, user):
        super(GitHubClient, self).__init__()
        self.base_url = 'https://api.github.com/'
        self.user = user
        self.params = {'access_token': os.environ['GH_ACCESS_TOKEN']}
        self.headers = {'Accept': 'application/vnd.github.v3+json'}

    def get_user_profile_data(self, timeout=20):
        endpoint = 'users/{user}'.format(user=self.user)
        futures = self.session.get(
            url=self.base_url+endpoint,
            params=self.params,
            headers=self.headers,
            timeout=timeout
        )
        resp = futures.result()
        if resp.status_code == 200:
            return resp.json()
        else:
            # something went bad with the request
            # todo raise something here
            pass

    def get_user_starred_repository(self, page_size=100, timeout=20):
        endpoint = 'users/{user}/starred'.format(user=self.user)
        params = {'page_size': page_size}
        params.update(self.params)
        futures = self.session.get(
            url=self.base_url+endpoint,
            params=params,
            headers=self.headers,
            timeout=timeout
        )
        resp = futures.result()
        if resp.status_code != 200:
            # todo raise
            pass
        if 'next' in resp.links.keys():
            records = self._get_total_record_count(resp.links)
            return records
        else:
            return len(resp.json())

    def get_user_repo_data(self, page_size=100, timeout=20):
        endpoint = 'users/{user}/repos'.format(user=self.user)
        params = {'page_size': page_size}
        params.update(self.params)
        return self._retrieve_all_paged_objects(
            endpoint,
            timeout=timeout,
            params=params,
            headers=self.headers
        )

    def get_user_commits(self, repos, page_size=100, timeout=20):
        params = {'page_size': page_size}
        params.update(self.params)
        total_commits = 0
        for repo in repos:
            endpoint = 'repos/{user}/{repo_name}/commits'.format(user=self.user, repo_name=repo)
            futures = self.session.get(
                url=self.base_url+endpoint,
                headers=self.headers,
                timeout=timeout,
                params=params
            )
            resp = futures.result()
            if resp.status_code != 200:
                # todo raise error
                pass
            if 'next' in resp.links.keys():
                repo_commits = self._get_total_record_count(resp.links)
                total_commits += repo_commits
            else:
                total_commits += len(resp.json())
        return total_commits

    def get_repo_topics(self, repos, page_size=100, timeout=20):
        headers = {'Accept': 'application/vnd.github.mercy-preview+json'}
        params = {'page_size': page_size}
        params.update(self.params)
        topics = set()
        for repo in repos:
            endpoint = 'repos/{user}/{repo_name}/topics'.format(user=self.user, repo_name=repo)
            futures = self.session.get(
                url=self.base_url+endpoint,
                headers=headers,
                params=params,
                timeout=timeout
            )
            resp = futures.result()
            if resp.status_code != 200:
                # todo raise error
                pass
            if resp.json().get('names'):
                topics.update(resp.json()['names'])
        return topics

    def _retrieve_all_paged_objects(self, endpoint, timeout, params, headers):
        """Returns all paginated results
        """
        all_objects = []
        futures = self.session.get(
            url=self.base_url+endpoint,
            timeout=timeout,
            params=params,
            headers=headers
        )
        resp = futures.result()
        if resp.status_code != 200:
            # todo raise error
            pass
        all_objects.extend(resp.json())
        while 'next' in resp.links.keys():
            futures = self.session.get(url=resp.links['next']['url'], headers=headers, params=params)
            resp = futures.result()
            if resp.status_code != 200:
                #todo raise err
                pass
            all_objects.extend(resp.json())
        return all_objects

    def _get_total_record_count(self, link_data):
        """Using the Link header data to find the last paginated response
        """
        last_url = link_data['last']['url']
        futures = self.session.get(url=last_url, params=self.params, timeout=20, headers=self.headers)
        resp = futures.result()
        if resp.status_code != 200:
            # todo
            pass
        last_count = len(resp.json())
        last_page_num = re.search(r'\d+', re.search(r'\bpage=\d+', last_url).group(0)).group(0)
        return ((int(last_page_num) - 1) * 100) + last_count
