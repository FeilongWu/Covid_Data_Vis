# Covid_Data_Vis

## Usage
### Use Microsoft Windows 10 as the operating system.
- Clone this repo using Git Bash:
```bash
git clone https://github.com/FeilongWu/Covid_Data_Vis.git
```
### All the commands below are executed using Command Prompt unless specified otherwise.
- Set the repository you just cloned as your working directory. The path to the directory may vary for different users. An example command is shown below:
```bash
cd "C://Users//your//name//Covid_Data_Vis"
```

- If you have <strong>venv</strong> installed, please skip. Use the following command to install  <strong>venv</strong>. This requires Python3.8:
```bash
pip install --user virtualenv
```
- Create a virtual environment (named Covid_vis) and activate it:
```bash
python -m venv Covid_vis
.\Covid_vis\Scripts\activate
```
- Install dependency(ies) for the environment.:
```bash
pip install -r requirements.txt
```
- You can extract a dependency list:
 ```bash
pip freeze > requirements.txt
```
- Use <strong>bokeh serve</strong> to execute Python script to launch the visualization:
 ```bash
python -m bokeh serve --show Dashboard.py
```
### Build your container for using the dashboard
- Refer to the instructions above to clone this repository. Please make sure you have installed [Docker Desktop](https://www.docker.com/products/docker-desktop) in your computer. Also, make sure that your docker daemon is running. In Command Prompt, go to the repository you just cloned. An example command is as below.
 ```bash
cd "C://Users//your//name//Covid_Data_Vis"
```
- Run the following command to build your image named as "dashboard".
 ```bash
docker build --tag dashboard:1.0 .
```
- After the image has been successfully built. You can run the following command to execute your image.
 ```bash
docker run -p 5006:5006 -it dashboard:1.0
```
- Once it has been served, open your browser and go to the link below to access to the dashboard being served.
 ```bash
http://localhost:5006/Dashboard
```
