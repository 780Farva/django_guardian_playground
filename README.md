# Django Guardian Playground (with DRF)
I made this repository to learn django guardian on top of the django rest framework.

At this stage, I'm unable to effectively give a non-staff user view permissions to list their own selves through the api.
The tests in the users app demonstrate this.

# Project Structure
This project uses a custom user, as defined in `users.models`.

CRUD operations on this model are exposed using a DRF ViewSet in the `users.views`.

Permissions are given to users inside a signal receiver in `users.models`.

# Current Issue
`users.tests.models` checks that users have the right set of permissions from guardian's perspective.
`users.tests.views` checks that logged in users can access endpoints as intended. This is where my issue shows up.
A given user has the `users.view_customuser` permission, as verified in `users.tests.models`, however the test for
whether a user can list itself through the api at `http://<domain>/users/<user_id>` fails. The particular test is 
`users.tests.test_views.ListUsersTest.test_user_can_list_self`

