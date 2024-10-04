# Micebot
A ROS simulation for gathering robot 

## Setting up the enviroment
### Ubuntu
-----
* **Enable GUI within Docker containers**

  > **! Caution:** This method exposes PC to external source. Therefore, a more secure alternative way is expected for using GUI within Docker containers. This problem was raised in [Using GUI's with Docker](https://wiki.ros.org/es/docker/Tutorials/GUI#:~:text=%2D%2Dpulse.-,Using%20X%20server,-X%20server%20is)

```bash
#This command is required to run every time the PC is restarted
xhost + 
```
Make a X authentication file with proper permissions for the container to use (Only for ubuntu)

```bash
# If not working, try to run "sudo rm -rf /tmp/.docker.xauth" first
cd ./src/micebot_dockerfiles/
chmod +x ./install/xauth.sh && ./install/xauth.sh
```

* **Launch the environment**
  
Build the docker image (for the first time) and start the container
```bash
cd ./src/micebot_dockerfiles
docker compose up -d 
```

Open a container in interactive mode
```bash
docker exec -it micebot bash
```
To stop containers, run
```bash
cd ./src/micebot_dockerfiles
docker compose down
```

To commit a container to a new image, run
```bash
# Do not do this if you're not familiar with Docker commit action. This changes your docker images.
docker commit micebot micebot:noetic
```
More other useful Docker's CLI can be found in [Docker CLI cheetsheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf)

### Windows
-----

* **Enable GUI within Docker containers using XLaunch**
Download and install [Xming](https://sourceforge.net/projects/xming/)

Open XLaunch and follow the steps below:
1. Choose "Multiple windows" and click "Next"
2. Choose "Start no client" and click "Next"
3. Choose "Disable access control" and click "Next"
4. Choose "No" and click "Next"
5. Choose "Start a program" and click "Next"
6. Choose "C:\Program Files\Docker\Docker\resources\bin\docker.exe" and click "Next"
7. Click "Finish"

Build the docker image (for the first time) and start the container
```bash
cd ./src/micebot_dockerfiles
docker compose -f docker-compose.windows.yml up -d 
```

Open a container in interactive mode
```bash
docker exec -it micebot bash
```
To stop containers, run
```bash
cd ./src/micebot_dockerfiles
docker compose down
```

To commit a container to a new image, run
```bash
# Do not do this if you're not familiar with Docker commit action. This changes your docker images.
docker commit micebot micebot:noetic
```
More other useful Docker's CLI can be found in [Docker CLI cheetsheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf)


## Starting up the system with simulation

-----

Start the simulation

```bash
docker compose up -d 
```

Open a container in interactive mode

```bash
docker exec -it micebot bash
```

Start the simulation

```bash
roslaunch micebot_launch micebot_gazebo.launch
```