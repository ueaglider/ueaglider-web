# ueaglider-web

A new website to replace the venerable PHP job by Bastien at http://ueaglider.uea.ac.uk/

The development version is now live at https://demo-ueaglider.hopto.org/

# Aims

- [x] Emulate funcionality of old website
  - [x] Map with dive locations and optional layers
  - [x] Menu of glider dives
  - [x] Page of dive plots
  - [x] Glider status page
  - [x] Science page
  - [x] login to add missions and waypoints
  
- [x] Show all legacy data
  - [x] Waypoints on map
  - [x] All figures showing on site

- [ ] Improve the map
  - [x] No more blue markers
  - [x] GEBCO 1000 m contour
  - [ ] Add Caravela location
  - [ ] Add ships location (Rob)
  - [x] Click on a particular dive on the map to get the plots up (Karen)
  - [x] Add graticule (Adrian and Gareth)
  - [x] Add 500m isobath (Karen and Gillian)
  - [x] Add all overlays from old site (Gillian)

- [ ] Improve the dive plots
  - [ ] Add/remove lines on main dive plot (Gareth)
  - [ ] Zoom in on plots, spcifically apogee zero crossing (Rob)
  - [ ] Consider streamlit for this functionality (Tom)
  - [ ] Experiment with bokeh for interactivity
  - [ ] Add more mission long plots for e.g. suggested pitch center
  - [ ] Better pcolor plots, using cmocean
  - [ ] Overview of the critical issues - batteries, and when the next call is due (Karen)
  - [x] Gebco bathymetric depth at the location of the last surfacing (Rob)
  - [x] page for each glider showing most recent mission etc (Gareth)
  
- [ ] Extra pages
  - [x] Summary of each glider
  - [x] Summary of each mission

- [ ] Security
  - [ ] install bootstrap locally with npm
  - [x] secure with SSL
  - [x] Make sure you can't delete stuff from the website
  - [x] sql injection vulns
  - [ ] XSS vulns

- [x] include sitemap and robots

- [ ] Documentation

- [ ] Tests
  - [x] Sitemap url requests
  - [ ] Home tests
  - [ ] Glider tests
  - [ ] Dive tests
  - [ ] Account tests

### Inspiration

Architecture follows several of the paradigms taught by Michael Kenndy in his [flask course on TalkPython.fm](https://training.talkpython.fm/courses/explore_flask/building-data-driven-web-applications-in-python-with-flask-sqlalchemy-and-bootstrap)

Other glider sites to check out
- https://iop.apl.washington.edu/seaglider/index.php
- https://roammiz.com/

# Tools used

- flask for the main web app
- bootstrap for pretty front end stuff
- sqlalchemy to talk to the database
- leaflet (javascript) for maps
