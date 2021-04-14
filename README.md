# README Etiki-Prototype1
Etiki Webserver using django. Etiki – Wikipedia for corporate sustainability assessment

## Dependencies
- Python >= 3.7
- django >= 2.2.9
- NodeJS >= 6.9.0

## Apps
### etilog
- Main app
- User interface: Search and filter requests
- Model definition (ImpactEvent, Company, …) 
### etikicapture
- User interface for import of new articles which creates new Impact Event. 
- Automatic extraction (using Readabilipy) and categorization of articles (using external NLP endpoint)
### usermgmt
- app for user management (registration, login, privileges, …)
### etikptype1
- django server settings
### impexport
- import of DB data
- export of NLP data
### prediki
- not used at the moment
- internal NLP endpoint

## Installation
- Install django
- Install NodeJS
- install node packages in package.json: `npm install`
- install python packages using pip: `python -m pip install -r requirements.txt`

## Run in development environment
- `python EtikiPtype1/manage.py runserver 0.0.0.0:8000`