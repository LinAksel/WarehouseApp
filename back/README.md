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

# Update 11.2.2021:

The server will now start filling the internal cache on startup. It communicates the startup time to frontend, so that the user can be informed better about the server status. Unnecessary long parsing was also replaced with a much faster map-based solution, and the server now also keeps brand info cached for 5 minutes to ensure better response times. To prevent loading old data on some multiples of 6, data renewal period is now exactly 5 minutes, mirroring the API cache time.
