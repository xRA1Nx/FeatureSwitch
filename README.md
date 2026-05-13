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
1. Log in to the /admin panel using your credentials (a .env account is temporarily used)
2. Create your Team via the /admin panel
3. Create your TeamService and link it to the corresponding Team
4. Add the necessary FeatureFlags to your project
5. Activate/deactivate flags as needed. Flags can also be edited or deleted
6. Use Swagger /docs for endpoints showing flag activity status and TTL relevance.


## Upcoming Functionality
- Add User entity, role-based access control, and corresponding authorization changes
- Notifications (an interface to notify about expired flags to facilitate their subsequent removal)
