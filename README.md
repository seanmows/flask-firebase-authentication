#### Flask Server with Authentication using JWT and Firebase
```This is a demo server showing JWT tokens and flask```

You can use postman to demo, change config and env variables with your credentials

## Getting Started

Configure firebase
```
# Start webserver
flask run
```

## Routes
1. "\" is open to everyone
2. "\login" login is open to everyone
3. "\books" requires a valid access token to access
4. "\refresh" required a valid refresh token and will generate a access token