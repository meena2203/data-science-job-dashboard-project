// Set the main coordinates (US coordinates) for our map
var myMap = L.map("map", {
    center: [37.0902, -95.7129],
    zoom: 5
  });

     
// Add attribution (the tile layer) to Openstreet map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);


// URL for fetching the data from app.py
var link = '/api/map_data';

// Create icon objects using GitHub resource
var iconColor;
var greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var goldIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});


// Create function to determine the color of a popup 
function chooseColor(work_environment) {
  // console.log('chooseColor: ' + work_environment)
  if (work_environment == 'onsite') return 'red';
  else if (work_environment == 'remote') return 'green';   
  else return 'gold';  
}

// Use d3.json function to read in the data from the url
d3.json(link).then(function(data) {
    
  for (const value of Object.values(data)) {         
    
    // Create the color code for different work_environment
    var job_mode = value['attribute'];
    if (job_mode == 'onsite') iconColor = redIcon;
    else if (job_mode == 'remote') iconColor = greenIcon;    
    else iconColor = goldIcon; 

    // Create a layer with the retrieved data and store it as a variable  
    var marker = L.marker([value['latitude'], value['longitude']], {icon: iconColor});
        
    // Bind a popup to the markers with required information; convert the job posting link to a hyperlink
    marker.bindPopup(
      '<h3> Title: ' + value['title'] + '</h3><hr /><hr />Company: ' +
      value['company'] + '<br /><br />Attribute: ' +
      value['attribute'] + '<br /><br />Location: ' + value['location'] 
      + '<br /><br />Posted Date: ' + value['posted_date'] 
      + '<br /><br />Link: ' + '<a href="'+ (value['link']) +'">'+'<h5> Apply Here </h5></a>').addTo(myMap);          
      
    }

    // Creating legend for the map
    var legend = L.control({position: 'bottomright',});

    legend.onAdd = function (map) {
      
      var div = L.DomUtil.create('div', 'info legend'),
          work_environment = ['onsite', 'remote', 'hybrid'];

      // loop through the work_environment range and generate a label with a colored square for each range
      for (var i = 0; i < work_environment.length; i++) {
          div.innerHTML +=
              '<i style="background:' + chooseColor(work_environment[i]) + '"></i> ' +
              work_environment[i] + '<br>';
      }

      return div;  
    };
    legend.addTo(myMap);   
})  