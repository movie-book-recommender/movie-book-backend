# Setting up and running Docker in cPouta

## Setting up a port for Docker in cPouta

As a first step, a new security group **docker** was created in cPouta. It opens a port to access Docker in the virtual machine from the internet. Please note that when a new security group is create it should be associated with the moviebook_test instance to enable it.

## Pulling the latest front end data to cPouta

Then, the repository for the front end of movie book recommender project was cloned to cPouta.

```
cd /home/ubuntu/frontend
git clone https://github.com/movie-book-recommender/movie-book-recommender-project.git
```

In the future when the software is updated, it can be just pulled in from GitHub.

## Installing Docker in cPouta

Docker was installed in cPouta using instructions, e.g., https://docs.docker.com/engine/install/ubuntu/.

## Creating a new Docker image in cPouta

Then a Docker image was created in cPouta. First command below creates an image. If this is successful, then the second command can be used to start the image as a container.

```
sudo docker build -t mvbkrec .
sudo docker run -d -p 5000:5000 mvbkrec
```

This assumes that the folder you are in contains the files Dockerfile, .dockerignore, and docker-compose.yml.

## Other useful commands

* To check what containers are running, use `sudo docker container ls`
* To stop a container from running, use `sudo docker kill <name of the container>`
* To clean up after exiting containers, use `sudo docker system prune`
* If you want to see what images are available, use `sudo docker image ls`
* To delete an image, use `sudo docker image rm <name of the image>`
* If you are unsure whether there is traffic coming to a port, use `sudo tcpdump -v port <port number>`