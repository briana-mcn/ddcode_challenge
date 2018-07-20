"""I would test the following:
BitBucketClient = bbc

- test that bbc inherit from `BaseClient`
- test the attributes are set upon initialization
- test `get_repository_data`
    - mock the call to `retrieve_all_paged_objects` and confirm its called with the expected vars
    - confirm the mock is returned
- test `get_repo_commits`
    - mock `retrieve_page_object_count`, confirming that it's called with the expected params
    - all input repos call the `retrieve_page_object_count` for the number of repos available
    - test the appending of the total commit values by mock the return value for the number of times
    `retrieve_page_object_count` is called.
- `get_repo_issues` same as `get_repo_commits` except no testing the calculator feature
- `get_repo_watchers` identical to `get_repo_issues`



for the following, I'm not certian how to test concurrency- would need to research this
- get_followers
    - have a size key be returned in a ok response, test that the json response is then returned
    - test if size key not returned in ok reponse, error is raised
    - test that an error is raised when response in not ok
- get_followings same as above
- retrieve_all_paged_objects
    - if resp.status is not 200, test raise
    - if 200 response:
        - test with no next key in json resp
            - assert the json values key data is returned
        - test wih next key in json resp and 200 ok:
            - assert the function returns the value key data from both calls
        - test not 200 response with next key
            - assert error is raised
- get_multiple_repo_record_count
    - if 200 resp, assert the size value is returned
    - if resp is 404
        - and error message eludes to issue tracker, assert 0 is returned
        - if not related to issue tracker assert an error is raised
    - test non 404 or 200 resp raises error
        
- retrieve_page_object_count
    - non- 200 response raises error
    - 200 response:
        - no next key in json response and has a non-0 value:
            - assert the input page size + the len of the json value is returned
        - no next key and value key is 0:
            - page size only is returned
        - next key available and non-200 resp:
            - error raised
        - next key and 200 status code:
            - assert the return value equals the page size + both length of last page records
"""
