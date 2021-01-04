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

- [ ] Improve the dive plots
  - [ ] Add/remove lines on main dive plot (Gareth)
  - [ ] Zoom in on plots, spcifically apogee zero crossing (Rob)
  - [ ] Add more mission long plots for e.g. suggested pitch center
  - [ ] Better pcolor plots, using cmocean

- [ ] Security
  - [ ] Make sure you can't delete stuff from the website
  - [ ] sql injection vulns
  - [ ] XSS vulns

- [ ] Documentation

- [ ] Tests

# Tools

- flask for the main web app
- sqlalchemy to talk to the database
- leaflet for maps
