# Covid_Data_Vis

## Usage
### Use Microsoft Windows 10 as the operating system.
- Clone this repo using bash:
```bash
git clone https://github.com/FeilongWu/Covid_Data_Vis.git
```
### All the commands below are executed using Command Prompt.
- If you want to create a virtual ennvironment under the directory of the cloned repository, you need to go to the directory you just cloned. The directory may vary for differen users. An example is shown below:
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
- Install dependency(ies). If you do not have "requirements.txt" under your working directory, you can copy it from the repository and paste it under your working directory:
```bash
pip install -r requirements.txt
```
- You can extract a dependency list:
 ```bash
pip freeze > requirements.txt
```
- Assum you have "Dashbaord.py" under you working directory. Use <strong>bokeh serve</strong> to execute it:
 ```bash
python -m bokeh serve --show Dashbaord.py
```