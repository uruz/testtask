# Assumptions

The API is read-only, in real world wallets may be created via the same API, but it would require proper authentication
and authorization, which is out of scope for this task.
There are a lot of ways to ensure proper balance for wallet accounting for transactions, but they depend on the
system requirements which are unknown. So, for the purpose of simplicity, I've used MySQL trigger to do that.
Building SQLAlchemy migration is weird, considering lack of SQLAlchemy mentions before, so I used default Django
migrations.
I haven't prepared the fake data, so the `web` docker services would be run empty.

# Quick start
`docker compose build`
`docker compose up db -d`
`docker compose up web`

# Run tests
`docker build tests`
`docker run tests`
