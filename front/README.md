# WarehouseApp frontend

Run

```
npm install
```

in this folder to install dependencies.
After this, simply run

```
npm start
```

to use the app (which will be very boring without first starting up the [backend](/back)!).
If the backend is started for the first time (or reloaded), the first time loading data for each category
will take some time (tens of seconds per category). After that it will take care of renewing the information without any delay to the user,
and switching between categories will be lightning fast!

# Update 11.2.2021:

The front now acknowledges server status, and prevents the user to make unnecessary calls to the server upon server startup.
After the safe time of 90 seconds or server responding that it is ready, the user is able to select a category. This "soft-lock" ensures that
the server-side cache loop is initialized correctly, and that the user will never have to wait long for category responses.
