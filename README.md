Written using Django and the Django REST framework

Utilized an LLM to create boilerplate code / test cases

To run:

```
make run
```

To test:
```
make test
```

Here are some example curl requests I was using to test:

Creating a user
```
curl -X POST http://127.0.0.1:8000/users/ \
-H "Content-Type: application/json" \
-d '{
  "name": "Eve Example",
  "email": "eve@example.com",
  "phone_number": "555-1234"
}'
```

Listing existing users
```
curl "http://127.0.0.1:8000/users/"
```

Creating a task
```
curl -X POST http://127.0.0.1:8000/tasks/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Task 1",
  "status": "done",
  "due_date": "2025-10-31T10:00:00Z",
  "user_id": <uuid>
}'
```

Listing existing tasks with filtering
```
curl "http://127.0.0.1:8000/users/?limit=1&offset=1"
```

```
curl "http://127.0.0.1:8000/users/?limit=1&offset=1&user_id=<uuid>"
```

Retrieving a summary of tasks:
```
curl "http://127.0.0.1:8000/tasks/summary/"
```