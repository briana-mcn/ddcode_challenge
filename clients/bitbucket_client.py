import requests

from clients.base import BaseClient


class BitBucketClient(BaseClient):
    def __init__(self, resource, reource_type='teams'):
        super(BitBucketClient, self).__init__()
        self.base_url = 'https://api.bitbucket.org/2.0/'
        self.resource = resource
        self.resource_type = reource_type

    def get_repository_data(self, page_size=100, timeout=20):
        """Retrieves all repository data for a provided team or user.
        """
        params = {'pagelen': page_size}
        endpoint = 'repositories/{resource}'.format(resource=self.resource)
        return self.retrieve_all_paged_objects(endpoint, timeout, params)

    def get_repo_commits(self, repos, page_size=100, timeout=20):
        total_commits = 0
        for repo in repos:
            endpoint = 'repositories/{resource}/{repo_name}/commits'.format(
                resource=self.resource,
                repo_name=repo
            )
            total_commits += self.retrieve_page_object_count(endpoint, timeout, params={'pagelen': page_size})

        return total_commits

    def get_repo_issues(self, repos):
        total_issues = 0
        for repo in repos:
            endpoint = 'repositories/{resource}/{repo_name}/issues'.format(
                resource=self.resource,
                repo_name=repo
            )
            total_issues += self.get_mulitple_repo_record_count(endpoint)
        return total_issues

    def get_repo_watchers(self, repos, page_size=100):
        total_watchers = 0
        for repo in repos:
            endpoint = 'repositories/{resource}/{repo_name}/watchers'.format(
                resource=self.resource,
                repo_name=repo,
                page_size=page_size
            )
            total_watchers += self.get_mulitple_repo_record_count(endpoint)
        return total_watchers

    def get_followers(self):
        endpoint = '{resource_type}/{resource}/followers'.format(
            resource_type=self.resource_type,
            resource=self.resource
        )
        resp = requests.get(url=self.base_url+endpoint)
        # todo implement non-200 response error handling
        if resp.json() != 200:
            # todo raise error
            pass
        if not resp.json().get('size'):
            #todo raise
            pass
        return resp.json().get('size')

    def get_followings(self):
        endpoint = '{resource_type}/{resource}/following'.format(
            resource_type=self.resource_type,
            resource=self.resource
        )
        resp = requests.get(url=self.base_url + endpoint)
        # todo implement non-200 response error handling
        if resp.json() != 200:
            # todo raise error
            pass
        if not resp.json().get('size'):
            # todo raise
            pass
        return resp.json().get('size')

    def retrieve_all_paged_objects(self, endpoint, timeout, params):
        """Retrieves the JSON content of all paginated pages of a resource.

        The Bitbucket API provides a 'next' key if more records are available after the current page.
        The 'next' key is utilized to retrieve the next paginated URL-
        all JSON responses are appended to a list and returned after all pages are retrieved.

        :return: all JSON content of each paginated page
        :rtype: list of JSON objects
        """
        all_objects = []
        futures = self.session.get(
            url=self.base_url+endpoint,
            params=params,
            timeout=timeout
        )
        resp = futures.result()
        if resp.status_code != 200:
            # todo raise error
            pass
        all_objects.extend(resp.json()['values'])
        while 'next' in resp.json().keys():
            futures = self.session.get(url=resp.json()['next'])
            resp = futures.result()
            if resp.status_code != 200:
                # todo raise err
                pass
            all_objects.extend(resp.json())
        return all_objects

    def get_mulitple_repo_record_count(self, endpoint):
        resp = requests.get(self.base_url + endpoint)
        if resp.status_code != 200:
            # todo raise
            pass
        data_dict = resp.json()
        # something not right with response
        if not data_dict.get('size'):
            # todo raise
            pass
        return (data_dict['size'])

    def retrieve_page_object_count(self, endpoint, timeout, params):
        """Parses through all paged urls of an endpoints' repsponse, returning the count of all records for the repo.

        .. note:: Implemented specifically for the /commits endpoint, as it does not include
            a 'size' key indicating the record count.

        :param endpoint: endpoint for the request
        :type endpoint: str
        :param timeout: seconds to allows for the requests library to send a request
        :type timeout: int
        :param params: items to be passed in the request as query paramaters
        :type params: dict
        :return: count of all commits in a single repository
        :rtype: int
        :raise: HTTPError
        """
        resp = requests.get(url=self.base_url+endpoint, params=params, timeout=timeout)
        if resp.status_code != 200:
            # todo raise
            pass
        page_count = 0
        while 'next' in resp.json().keys():
            url = resp.json()['next']
            resp = requests.get(url=url)
            page_count += 1

        final_page_records = resp.json().get('values')
        if not final_page_records:
            final_page_record_count = 0
        else:
            final_page_record_count = len(final_page_records)
        return (page_count * 100) + final_page_record_count
