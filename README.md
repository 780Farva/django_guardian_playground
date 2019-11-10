# Django Guardian Playground (with DRF)
I made this repository to learn [django guardian](https://github.com/django-guardian/django-guardian) on top of the [django rest framework](https://github.com/encode/django-rest-framework/tree/master).

At this stage, I'm unable to effectively give a non-staff user view permissions to list their own selves through the api.
The tests in the users app demonstrate this.

# Project Structure
This project uses a custom user, as defined in `users.models`.

CRUD operations on this model are exposed using a DRF ViewSet in the `users.views`.

Permissions are given to users inside a signal receiver in `users.models`.

The admin group is created in migration `0005_make_admins_group.py` and that group's permissions are enforced in 
the same signal receiver.
