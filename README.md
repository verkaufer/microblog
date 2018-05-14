# microblog

Implements a Twitter-esque web application using:
- Django 2+ & Python3.6
- VueJS
- Docker

## Project Requirements & Specs

- Allow the user to be able to authenticate (username and password only)
- Allow user to post messages to their Feed
- Allow users to follow another user
- The "main feed" for a user (e.g. homepage) should show the posts created by the people they follow in a chronological order (most recent to least recent)
    - Pagination not in scope
- Allow user to decide if their feed is private (i.e. visible only to people following that user) or public (visible to even unauthenticated users)


## Project Setup

This project uses Docker for local development. To bring up all containers, run `make up` or `make build`. 

To SSH into a container, run `make shell-django` or `make shell-frontend` to access the Django or VueJS containers, respectively. 

### Local nginx proxy
**IMPORTANT**
This project's nginx proxy requires a special URL. Before starting the containers, execute the following command:
```
sudo -- sh -c -e "echo '127.0.0.1    microblog.docker' >> /private/etc/hosts";
```

This command adds `microblog.docker` to your Hosts file and points it at the `localhost` IP address.