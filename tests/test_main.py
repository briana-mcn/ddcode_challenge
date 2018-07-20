"""I would test the following:

- for the condition where all query parameters are present
    - test that the GitHubProfile is instantiated with the github query param
    - the method to build the github profile is called
    - if the correct resource type for bitbucket is passed in the query parmater:
        - test the instantiation of the bitbucket profile is passed with the user and the user type
        - test that the build bitbucket profile method is called
    - if not the expected q. params are passed:
        - assert that a RequestError is raised
    - assert that the calculate languages method is called on the github profile instance
    - assert the responding status code is set to 200
    - assert the json object of the retrieved data dict is returned with the call
- when any query param is absent:
    - assert RequestError is raised
    
- test confirm dict equality
    - if dicts are identical don't raise an error
    - if they are not, make sure the request status is set to 500 and assert a VCSMangerError is raised
"""
