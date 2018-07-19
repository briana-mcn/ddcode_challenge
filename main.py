import json

from flask import Flask, request

from exc import RequestError, VCSManagerError
from profiles.base_user_profile import UserProfile
from profiles.bitbucket import BitBucketProfile
from profiles.github import GitHubProfile


app = Flask(__name__)


@app.route('/user-profile')
def main():
    github_user = request.args.get('github_user')
    bitbucket_user = request.args.get('bitbucket_user')
    bitbucket_user_type = request.args.get('bitbucket_user_type')
    # GET
    # /user-profile?bitbucket_user=1&bitbucket_user_type=teams&github_user=1

    # if the query params exists, initiate build
    if bitbucket_user and bitbucket_user_type and github_user:
        github_profile = GitHubProfile(github_user)
        github_profile.build_github_profile()
        if bitbucket_user_type not in ['teams', 'users']:
            raise RequestError(
                "Only 'teams' or 'users' resource types available for BitBuckets API: {}".format(bitbucket_user_type)
            )
        bitbucket_profile = BitBucketProfile(resource=bitbucket_user, resource_type=bitbucket_user_type)
        bitbucket_profile.build_bitbucket_profile()

        # jsonify the retreieved data dictionary from both accounts
        # note: I think this is a really hacky, near un-viable solution for a production environment.
        # Aside from building a small database, I think I would need to re-implement
        # an aggregator to take two dictionaries and merge all values, that way you could still access the individual
        # dict values of any `Profile` object
        confirm_dict_equality(bitbucket_profile.retrieved_data, github_profile.retrieved_data)
        aggregate_profiles = bitbucket_profile
        aggregate_profiles.calculate_languages()
        request.status_code = 200
        return json.dumps(aggregate_profiles.retrieved_data)
    else:
        raise RequestError('Missing query parameters: {}'.format(list(request.args.keys())))


def confirm_dict_equality(dict1, dict2):
    """Confirms equality of two dictionaries
    """
    if dict1 == dict2:
        pass
    else:
        # log this
        request.status_code = 500
        raise VCSManagerError('The built dictionaries are not identical. Yikes.')


if __name__ == "__main__":
    app.run(debug=True)
