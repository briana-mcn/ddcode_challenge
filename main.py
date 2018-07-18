import json

from flask import Flask, request

from profiles.base_user_profile import UserProfile
from profiles.bitbucket import BitBucketProfile
from profiles.github import GitHubProfile


app = Flask(__name__)



@app.route('/user-profile')
def main():
    github_user = request.args.get('github_user')
    bitbucket_user = request.args.get('bitbucket_user')
    bitbucket_user_type = request.args.get('bitbucket_user_type')

    # /user-profile?bitbucket_user=1&bitbucket_user_type=teams&github_user=1

    # if the query params exists, initiate build
    if github_user and bitbucket_user and bitbucket_user_type:
        github_profile = GitHubProfile(github_user)
        github_profile.build_github_profile()
        if bitbucket_user_type not in ['teams', 'users']:
            # todo raise error
            pass
        bitbucket_profile = BitBucketProfile(resource=bitbucket_user, resource_type=bitbucket_user_type)
        bitbucket_profile.build_bitbucket_profile()

        # jsonify the retreieved data dictionary from both accounts
        aggregate_profiles = UserProfile()
        aggregate_profiles.calculate_total_profile_data()
        request.status_code = 200
        return json.dumps(aggregate_profiles.retrieved_data)
    else:
        # todo raise error, required params not available
        pass
