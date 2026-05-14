# Feature Switch
The service allows wrapping features in "feature flags" and provides the ability
to activate/deactivate features on the fly (without deployment).

## Installation

1. Install Python 3.12
2. Install Docker
3. Install Git
4. Clone the repository
5. Create a virtual environment (Python 3.12)
6. Run:
```shell script
pip install --upgrade pip pip-tools && make install-dev && make install-hooks
```

## Step-by-Step Guide
1. **Create an admin user** (interactive mode):
```shell script
python manage.py user create-admin
```
You will be prompted to enter:
-Email address
-Password (twice for confirmation)
Alternatively, you can create a user non-interactively:
```shell script
python manage.py user create-admin --email admin@example.com --password your_password
```
2. Create your Team via the /admin panel
3. Create your TeamService and link it to the corresponding Team
4. Add the necessary FeatureFlags to your project
5. Activate/deactivate flags as needed. Flags can also be edited or deleted
6. Refer to Swagger /docs for the endpoints that report flag activity status and TTL relevance.


## Upcoming Functionality
- Notifications (an interface to notify about expired flags to facilitate their subsequent removal)
