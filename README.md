# e-commerce_scraper/ Webapp  
Done in linux/ Python 3.8.10  
For educational purposes.

## Django Webapp to search and scrape products' information from websites (only 10 available now) and store in sqlite3 database 

### Websites
  - kotsovolos.cy
  - kotsovolos.gr
  - plaisio.gr
  - mediamarkt.gr
  - public.cy
  - public.gr
  - stephanis.com.cy
  - electroline.com.cy
  - sofroniouelectronics.com
  - cosmodata.gr
  
### Gets
  - title
  - price
  - availability
#### for all listings that appear on the search on respective websites.  


### For linux server
   > Edit the file `sites-enabled/scraping_app.conf` according to your project path  
   > Put the `sites-enabled` folder and `apache2.conf` in `/etc/apache2`  
   > Put `config.json` in `/etc`  

### Usage 
- clone this repository 
  - `git clone https://github.com/themistysky/e_commerce_scraper webapp`
  - `cd webapp` 
- create virtual environment, install dependencies, 
  - `python3 -m venv scraping_app/env`
  - `source scraping_app/env/bin/activate`
  - `cat <requirements.txt | xargs -n 1 pip install` 
- edit `/scraping_app/scraping_app/settings.py`
  - add your domain name/IP address in the list `ALLOWED_HOSTS`
  - Turn on or off `DEBUG` based on your needs (Turning on DEBUG will show server error details in browser)
- collect static 
  - `python3 manage.py collectstatic` 
- make migrations 
  - `python3 manage.py makemigrations`
  - `python3 manage.py migrate`
- create superuser in sqlite3
  - `python3 manage.py createsuperuser`
    - enter username, password, etc.
- run server through django
  - `python3 manage.py runserver <your domain name/IP address>: <port number>`  
  (use port 80 to avoid giving port number in browser, use sudo to access port 80 through django)
  - go to browser and hit <your domain name>:<port number>
- give permissions to apache2 
  - sudo chmod -R 775 scraping_app
  - sudo chown -R :www-data scraping_app
- run server through apache2
  - sudo service apache2 restart  
- go to browser and hit `<your domain name>`
 
 
<br>  
<br>  
<br>  
<br> 

  ###### <i>Try at your own risk.</i>
