# WarehouseApp backend

Install dependencies with

```
pip install -r requirements.txt
```

and run the server with

```
uvicorn main:app
```

The server is build to make no more API calls than is strictly necessary for the task.
Because the client API has a 5 minute internal cache, the data will be renewed every 6 minutes to assure it is up-to-date.
When starting up the server, it will not make any hardcoded pre-calls, which will slow down the first frontend call per category.
This was a deliberate design call to ensure that not a single unnecessary API call will be made (because the API is very slow..).
After a category has been fetched once, the data will be cached and renewed automatically until the server is shut down.