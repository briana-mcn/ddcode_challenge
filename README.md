Version Control System Aggregator

## GET aggregated user data

Make GET requests and pass in query parameters to aggregate specific data of BitBucket users and GitHub users:

if running the code locally, send a GET request with user associated data parameters:
```bash
# accepted query params: bitbucket_user, bitbucket_user_type, github_user

curl https://<local-host>/user-profile?bitbucket_user=pygame&bitbucket_user_type=teams&github_user=1
# responds with the data aggregated from the github and bitbucket apis
```


## UserProfile

Profiles are separated on a per external API basis, with a specific client associated with each `UserProfile`.
Any class that inherits from `UserProfile` will have all results of api calls built on the `retrieved_data` dictionary- this aggregates all the from all results into a single jsonifiable dictionary.

i.e:
```
profile = BitBucketProfile('name-of-user', 'user-type')
# builds dictionary by making calls to BitBucket endpoints
profile.build_bitbucket_profile()

profile2 = GitHubProfile('user-name')
profile2.build_bitbucket_profile()

# UserProfile inherited classes append results to the same dictionary
# test that the dictionaries are identical
profile.retrieved_data == proflile2.retrieved_data

```


### BitBucketProfile

The client to connect to the BitBucket API is connected to this class.

### GitHubProfile

The client to connect to the GitHub API is associated with this class.


## Clients

Makes connections to associated external APIs. BaseClient, which instantiates a FutureSession object from request_futures allows for all inherits of the class to make asyncrounous calls.


### BitBucketClient

Client associated with the BitBucket API, with methods associated with differnet endpoints.

Note: BitBucket does not contain 'starring' or 'topic' features like GitHub.
resource_type that may be passed to the client may either be `teams` or `users` (defaults to `teams`)

Note: may be instantiated to retrieve data on different endpoints.


### GitHubClient

Similar to the BitBucket client, makes requests to various GitHub API endpoints.



--------------------------------------------------------------------


What I would do differently:
1. This program is really slow for having concurrency implemented. I would like to refactor,
to make sure the calls are all happening within a single context. This might be a little tricky- some of the API calls
depend on the results of another API call (getting the next paginated response to get all records). I would need 
to research better ways to do this. This approach will also make testing more feasible, where parsing 
logic is separated from the concurrent calls
http://jerrydantonio.com/testing-concurrent-code/
2. Research better ways to update dictionaries and actually update values instead of overwriting values of identical keys
such as what `dict.update()` method does. I might have to implement a specific script for this use case.
3. Not sure if the UserProfile classes are necessary- I believe I could get by not having them. The original intent
of using them was to have the convenient identical `retrieved_data` class in both the `BitBucketProfile` 
and `GitHubProfile` parent class, but that implementation is not great.  I could create a function within the main 
routing function that create an almighty dict that would merge all required data from each external service- 
this would allow for more version control systems' APIs to be integrated into the program, and each vcs to have it's own dictionary of data.
4. Blueprint out my concept before working on a single piece to know how all components will interact- write test after a few units can be tested
