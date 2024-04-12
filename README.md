
# REQUIREMENTS 
This project requirees Python Version 3.11.7 and Pip.
If you install Python, it should also intall Pip for you.
To install python you can follow this link [https://www.python.org/downloads/release/python-3117/]


After you have installed python , cd into the root directory of the project and then run the following command in your commandline.
This should install all the necessery depedecies of this project.

``` pip install -r requirements.txt ``` 

# HOW TO RUN THE CODE
After running this command you should now be ready to run the scraper. Run the follwing command for that.
This will produce a csv file named output.csv in the root directory of the project.

``` scrapy crawl kleinanzeigen_houses -o output.csv ```

# CHANGE SETTINGS SUCH AS LOCATION
To change settings related to this project. You can go to settings.py [./settings.py(https://github.com/benjaminmishra/kleinanzeigen-spider/blob/main/scrpae/settings.py)] file.

Here you can find settings such as MAIN_AREA , SUB_AREAS and ZIMMERS etc.
