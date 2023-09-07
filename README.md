# Nometa-Bot
Developed by students of the [Simulator ML (Karpov.Courses)](https://karpov.courses/simulator-ml)

<details open>
<summary>Repository structure</summary>

* `deployment/` - docker application deployment files
* `docs/` - project documentation folder
* `exploration/` - data mining folder
* `static/` - scripts to launch components
* `src/` - application source folder
     * `app/` - telegram bot files
     * `metrics/` - files for evaluating the quality of models
     * `models/` - folder with training scripts and inference
     * `utils/` - folder with util functions and variables
* `test/` - application tests (pytest)

</details>

### Launch

1) `git clone https://github.com/SimulatorML/Nometa-Bot.git`
2) Create a telegram bot and get a token through https://t.me/BotFather

Choose a launch option and continue with the steps
<details open>
<summary>Local</summary>

3) install python version: 3.8
4) ```pip install -r requirements.txt```
5) install PyTorch
6) `pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu`

7) Add a variable to your environment on ...

    linux: `export BOT_TOKEN=<your_token>`

    windows (cmd): `setx BOT_TOKEN "<your_token>"`

8) run `python static/start_bot.py`

</details>

<details open>
<summary>Docker</summary>

from the root of the repository run the commands
3) `docker build -t nometa_bot -f deployment/Dockerfile .`
4) `docker run -e BOT_TOKEN=<your_token> -p 8080:8080 nometa_bot`
</details>

After launching the bot, add it to the chat and allow it to read messages
