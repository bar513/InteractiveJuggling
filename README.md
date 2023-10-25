# Interactive Juggling Game
An open source project using openCV and Unity3D that let users to get live feedback on their juggling skills while they trying to achieve the best score. Pattern recognition and mini game was also implemented.
All details on project site:

# Code usage
Two different executable apps exist -  python app and unity3D app.

## The python app
Independent app that run all image processing algorithms. python packages list is there.
The "main" file should be run and the app will run - windows of the player as well as debug windows will open, show real time data. The windows tend to show on top on each other so they should be moved in order to reveal all the windows. 
the variable "online" can be set:
* if "online" set to false, the app will work without the need for the unity app
* if "online" set to true, a socket will be open and app will wait to the unity app

## The unity3D app
For the full game experience with sound, score, mini game and patteren recogonition the unity3d app must be executed.
First run the python "main" file, with "online" set to true. then run the unity app. unity must be download to run the app so it will build the app on the current platform.




