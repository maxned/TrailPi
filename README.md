# TrailPi
ECS 193 Senior Design Project for a DIY Web Cameras Network

### Networking
Currently have outlines for server and client scripts, with functional communication\
Two modes for client connection:

  0) `check_in`, to show camera is active
  1) `new_image`, to transfer a new image to server

Starts in a testing mode with lots of debugging output to follow steps\
Running:
  1) open two terminals
  2) run server on first terminal\
    2.1. `cd server`\
    2.2. `python3.7 TrailServerMain.py`
  3) run client on second terminal\
    3.1. `cd client`\
    3.2. `python3.7 TrailCamMain.py`
  4) choose mode to test
