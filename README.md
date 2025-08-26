# AutomART

Repo for the Software of the AutomART on the Raspberry PI

## TLDR
- `webappDev` holds the development env. for the webpage that can control the bot.
    - Inside use `npm run dev` to develop and `npm run build` to build directly to the serve directory of the webserver

- `server` and `client` holds the python code that is run on the robot.
- `startServer.sh` shall be run as a linux service on the pi
- `startClient.sh` shall be added to the ~/.bashrc file and the pi shall run in Console-Only-Mode. (`sudo raspi-config`) 