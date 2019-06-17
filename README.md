EY HACKATHON 

DOCKER FILE - To run the project :
      
      1. Download the repository and download, reaname and position the .npz file under the main folder
      2. Extract Dockerfile out of the repository and run a command shell form that outer directory
      3. Install docker for your host system.
      4. Execute "docker build -t flask:make ." from the terminal.
      5. Docker will downlaod the dependencies, it might take a while so be patient.
      6. After successful completetion you will see " Successfully tagged flask:Docker " as output if it doesnt work please open a issue
      7. After sucessful image building run " docker run --rm -it --network=host -p 5000:5000 flask:make " this would result in server logging windows.
      8. You can now go to your browser at "localhost:5000" and acess the project.
      9. If you face a issue raise a issue at github.


VIDEO WALKTHROUGH - https://vimeo.com/342645947

![Panel Page](https://github.com/amansheaven/EY_FileClaims/blob/master/Screenshot%20from%202019-06-17%2009-59-48.png?raw=true)
