from clients.base import BaseClient
from exc import HTTPError


class BitBucketClient(BaseClient):
    """Client used to interface with multiple BitBucket APIs.

    Considers the resource type when instantiating the client to allow for
    accurate fetching of the desired category of resources.
    """
    def __init__(self, resource, resource_type='teams'):
        super(BitBucketClient, self).__init__()
        self.base_url = 'https://api.bitbucket.org/2.0/'
        self.resource = resource
        self.resource_type = resource_type

    def get_repository_data(self, page_size=100, timeout=20):
        """Retrieves all repository data for a provided team or user.

        :return: all repositories and associate metadata
        :rtype: list of dicts
        """
        params = {'pagelen': page_size}
        endpoint = 'repositories/{resource}'.format(resource=self.resource)
        return self.retrieve_all_paged_objects(endpoint, timeout, params)

    def get_repo_commits(self, repos, page_size=100, timeout=20):
        """Retrieves the commit count for all provided repositories.

        :param repos: desired repositories to retrieve commit count from
        :type repos: list of strs
        :return: commit count of input repositories
        :rtype: int
        """
        params = {'pagelen': page_size}
        total_commits = 0
        for repo in repos:
            endpoint = 'repositories/{resource}/{repo_name}/commits'.format(
                resource=self.resource,
                repo_name=repo
            )
            total_commits += self.retrieve_page_object_count(
                endpoint,
                timeout=timeout,
                params=params,
                page_size=page_size
            )
        return total_commits

    def get_repo_issues(self, repos, page_size=100, timeout=20):
        """Calculates the total issue count from each input repository.

        :param repos: repos to parse to get issue count
        :type repos: list of strs
        :return: total issues count of all repositories
        :rtype: int
        """
        params = {'pagelen': page_size}
        total_issues = 0
        for repo in repos:
            endpoint = 'repositories/{resource}/{repo_name}/issues'.format(
                resource=self.resource,
                repo_name=repo
            )
            total_issues += self.get_multiple_repo_record_count(endpoint, timeout=timeout, params=params)
        return total_issues

    def get_repo_watchers(self, repos, page_size=100, timeout=20):
        """Retrieves the number of watchers for all of the users (or teams) associated repositories.

        :param repos: all of the repos to retrieve the total watcher count from
        :type repos: list of strs
        :return: all of the users repository watchers
        :rtype: int
        """
        params = {'pagelen': page_size}
        total_watchers = 0
        for repo in repos:
            endpoint = 'repositories/{resource}/{repo_name}/watchers'.format(
                resource=self.resource,
                repo_name=repo,
            )
            total_watchers += self.get_multiple_repo_record_count(endpoint, timeout=timeout, params=params)
        return total_watchers

    def get_followers(self, page_size=100, timeout=20):
        """Retrieves all of the users or teams followers

        :return: the number of followers on all of the users repositories
        :rtype: int
        """
        params = {'pagelen': page_size}
        endpoint = '{resource_type}/{resource}/followers'.format(
            resource_type=self.resource_type,
            resource=self.resource
        )
        futures = self.session.get(url=self.base_url+endpoint, timeout=timeout, params=params)
        resp = futures.result()
        if resp.status_code != 200:
            raise HTTPError(
                'Unexpected response of client {}: {}, HTTP status: {}'.format(
                    self.__class__.__name__,
                    resp.json(),
                    resp.status_code
                )
            )
        # if size key exists, but is 0, we don't want the error to be raised
        if resp.json().get('size', 'no size') == 'no size':
            raise HTTPError("Expected 'size' key not returned in the response: {}".format(resp.json()))
        return resp.json()

    def get_followings(self, page_size=100, timeout=20):
        """Retrieves the count of active repositories a user or team is following.

        :return: number of followings a users has
        :rtype: int
        """
        params = {'pagelen': page_size}
        endpoint = '{resource_type}/{resource}/following'.format(
            resource_type=self.resource_type,
            resource=self.resource
        )
        futures = self.session.get(url=self.base_url+endpoint, timeout=timeout, params=params)
        resp = futures.result()
        if resp.status_code != 200:
            raise HTTPError(
                'Unexpected response of client {}: {}, HTTP status: {}'.format(
                    self.__class__.__name__,
                    resp.json(),
                    resp.status_code
                )
            )
        # no error raised if size key is 0
        if resp.json().get('size', 'no size') == 'no size':
            raise HTTPError("Expected 'size' key not returned in the response: {}".format(resp.json()))
        return resp.json()

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
            raise HTTPError(
                'Unexpected response of client {}: {}, HTTP status: {}'.format(
                    self.__class__.__name__,
                    resp.json(),
                    resp.status_code
                )
            )
        all_objects.extend(resp.json()['values'])
        while 'next' in resp.json().keys():
            futures = self.session.get(url=resp.json()['next'])
            resp = futures.result()
            if resp.status_code != 200:
                raise HTTPError(
                    'Unexpected response of client {}: {}, HTTP status: {}'.format(
                        self.__class__.__name__,
                        resp.json(),
                        resp.status_code
                    )
                )
            all_objects.extend(resp.json())
        return all_objects

    def get_multiple_repo_record_count(self, endpoint, timeout, params):
        """Retrieves the number of records returned from an endpoint.

        Introspects the response for the 'size' key that represents the total record count.

        :return: the count of all records
        :rtype: int
        """
        futures = self.session.get(url=self.base_url+endpoint, timeout=timeout, params=params)
        resp = futures.result()
        data_dict = resp.json()
        # an issue tracker may not exist for a repository, try out the key and catch if that's the error,
        # otherwise raise the unknown issue
        if resp.status_code == 200:
            return data_dict['size']
        # not great implementation, but the only way I could figure out how to differentiate between
        # a request error or issue tracking not implemented error
        elif resp.status_code == 404:
            # probably would be good to log this 404
            # " 'size' key does not exist: {}".format(resp.status_code)
            if data_dict['error']['message'] != 'Repository has no issue tracker.':
                # not an issue tracking issue
                raise HTTPError(
                    'Unexpected response of client {}: {}, HTTP status: {}'.format(
                        self.__class__.__name__,
                        resp.json(),
                        resp.status_code
                    )
                )
            return 0
        else:
            raise HTTPError(
                'Unexpected response of client {}: {}, HTTP status: {}'.format(
                    self.__class__.__name__,
                    resp.json(),
                    resp.status_code
                )
            )

    def retrieve_page_object_count(self, endpoint, timeout, params, page_size):
        """Parses through all paged urls of an endpoints' response, returning the count of all records for the repo.

        Leverages the desired number of records to return on each response and the presence of a 'next'
        key denoting whether or not all pages have been served. A count of the pages multiplied by the
        page size plus a count of the last paged records are returned.

        .. note:: Implemented specifically for the /commits endpoint, as it does not include
            a 'size' key indicating the record count.

        :param endpoint: endpoint for the request
        :type endpoint: str
        :param timeout: seconds to allows for the requests_futures library to send a request
        :type timeout: int
        :param params: items to be passed in the request as query parameters
        :type params: dict
        :param page_size: page length to return for the paginated responses
        :type page_size: int
        :return: count of all commits in a single repository
        :rtype: int
        """
        futures = self.session.get(url=self.base_url+endpoint, params=params, timeout=timeout)
        resp = futures.result()
        if resp.status_code != 200:
            raise HTTPError(
                'Unexpected response of client {}: {}, HTTP status: {}'.format(
                    self.__class__.__name__,
                    resp.json(),
                    resp.status_code
                )
            )
        page_count = 0
        while 'next' in resp.json().keys():
            url = resp.json()['next']
            futures = self.session.get(url=url)
            resp = futures.result()
            if resp.status_code != 200:
                raise HTTPError(
                    'Unexpected response of client {}: {}, HTTP status: {}'.format(
                        self.__class__.__name__,
                        resp.json(),
                        resp.status_code
                    )
                )
            page_count += 1

        final_page_records = resp.json().get('values')
        if not final_page_records:
            final_page_record_count = 0
        else:
            final_page_record_count = len(final_page_records)
        return (page_count * page_size) + final_page_record_count
