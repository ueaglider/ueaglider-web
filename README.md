# ueaglider-web

A new website to replace the venerable PHP job by Bastien at http://ueaglider.uea.ac.uk/

# Aims

- [ ] Emulate funcionality of old website
  - [ ] Map with dive locations and optional layers
  - [ ] Menu of glider dives
  - [ ] Page of dive plots
  - [ ] Glider status page
  - [ ] Science page
  - [ ] login to add missions and waypoints
  
- [ ] Show all legacy data
  - [ ] Waypoints on map
  - [ ] All figures showing on site

- [ ] Improve the map
  - [ ] No more blue markers
  - [ ] GEBCO 1000 m contour
  - [ ] Add Caravela location
  - [ ] Add ships location (Rob)
  - [ ] Click on a particular dive on the map to get the plots up (Karen)

- [ ] Improve the dive plots
  - [ ] Add/remove lines on main dive plot (Gareth)
  - [ ] Zoom in on plots, spcifically apogee zero crossing (Rob)
  - [ ] Consider streamlit for this functionality (Tom)
  - [ ] Experiment with bokeh for interactivity
  - [ ] Add more mission long plots for e.g. suggested pitch center
  - [ ] Better pcolor plots, using cmocean
  - [ ] Overview of the critical issues - batteries, and when the next call is due (Karen)
  - [ ] Gebco bathymetric depth at the location of the last surfacing (Rob)

- [ ] Security
  - [ ] install bootstrap locally with npm
  - [ ] secure with SSL
  - [ ] Make sure you can't delete stuff from the website
  - [ ] sql injection vulns
  - [ ] XSS vulns

- [ ] include sitemap and robots

- [ ] Documentation

- [ ] Tests

### Inspiration

Other glider sites to check out
- https://iop.apl.washington.edu/seaglider/index.php

# Tools

- flask for the main web app
- sqlalchemy to talk to the database
- leaflet for maps
