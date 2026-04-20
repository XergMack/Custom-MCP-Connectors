# Remaining Family Scaffold Status

This scaffold intentionally does NOT guess live API shapes.

What is real and proven:
- requests
- notes
- worklogs
- tasks

What is scaffolded only:
- technicians
- users_requesters
- departments_groups_sites
- assets
- cmdb
- contracts
- purchase
- problems
- changes
- projects
- solutions
- catalog
- admin

Rule:
Each scaffolded family must be implemented only after:
1. docs/API shape is verified
2. payload shape is mapped
3. live example is tested
