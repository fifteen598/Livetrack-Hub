const API_SERVER = 'https://fifteen598.pythonanywhere.com';
const apiKey = "AIzaSyAje7bOq4ngPCC1rJ1h0Md2yHpPxCRMBMU";
const map = L.map('map').setView([37.7178, -97.2921], 14);
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors & CartoDB'
}).addTo(map);

let markers = {};
let streetMap, panorama; 
async function fetchAndUpdate() {
  try {
      const response = await fetch(`${API_SERVER}/fetch_records`);
      const users = await response.json();
      updateMarkers(users);
      updateStatuses(users);
  } catch (error) {
      console.error("Error fetching data:", error);
  }
}

function  updateMarkers(users) {
  Object.entries(users).forEach(([user, coords]) => {
    const userCoords = [coords.latitude, coords.longitude];
    if (markers[user]) {
      markers[user].setLatLng(userCoords);
    } else {
      markers[user] = L.marker(userCoords).addTo(map)
        .bindPopup(`<b>${user}</b><br>Location Updated`)
        .bindTooltip(user, { permanent: true, direction: "top", offset: [-15, -15]});
    }
  });
}

function initializeStreetView() {
  console.log("Initializing Street View...");

  const panoElement = document.getElementById("pano");
  if (!panoElement) {
      console.error("Error: 'pano' div not found!");
      return;
  }

  const location = { lat: 37.7749, lng: -122.4194 };

  panorama = new google.maps.StreetViewPanorama(panoElement, {
      position: location,
      pov: { heading: 34, pitch: 10 },
      visible: true
  });

  panorama.addListener("status_changed", () => {
      console.log("Street View Status:", panorama.getStatus());
  });

  console.log("Street View initialized:", panorama);
}

function updateStatuses(users) {
  // Draw or update geofence circle
  if (geofenceCenter && geofenceRadius) {
    if (window.geofenceCircle) map.removeLayer(window.geofenceCircle);
    window.geofenceCircle = L.circle(geofenceCenter, {
      color: 'green',
      fillColor: '#3f3',
      fillOpacity: 0.2,
      radius: geofenceRadius,
    }).addTo(map);
  }

  const statusContainer = document.getElementById("status-container");
  statusContainer.innerHTML = "";

  Object.entries(users).forEach(([user, coords]) => {
    const userCoords = [coords.latitude, coords.longitude];

    // Determine isHome
    let isHome = false;
    if (geofenceCenter) {
      const distance = map.distance(userCoords, geofenceCenter);
      isHome = distance <= geofenceRadius;
    }

    const panoElement = document.getElementById("pano");
    const statusElement = document.createElement("div");
    statusElement.classList.add("status-item", isHome ? "home" : "away");
    statusElement.innerHTML = `
      <span class="status-name">${user}</span>
      <span class="status-text ${isHome ? "home" : "away"}">${isHome ? "Home" : "Away"}</span>
    `;

    statusElement.addEventListener("click", () => {
      map.setView(userCoords, 17);
      panorama = new google.maps.StreetViewPanorama(panoElement, {
        position: { lat: userCoords[0], lng: userCoords[1] },
        pov: { heading: 34, pitch: 10 },
        visible: true
      });
    });

    statusContainer.appendChild(statusElement);

    setTimeout(() => {
      statusElement.classList.add("fade-in");
    }, 100);
  });
}


// FUNCTION TO UPDATE LOCATION
async function updateLocation(name, latitude, longitude) {
    try {
      const response = await fetch(`${API_SERVER}/update_location`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, latitude, longitude }),
      });
  
      if (!response.ok) {
        console.error("Error updating location:", await response.text());
      }
    } catch (error) {
      console.error("Error sending location update:", error);
    }
  }

fetchAndUpdate();
setInterval(fetchAndUpdate, 5000);

function toggleMenu() {
  document.body.classList.toggle('nav-active');
  setTimeout(() => {
    map.invalidateSize();
  }, 200);
}

function loadGoogleMapsAPI() {
  if (!apiKey) {
    console.error("API key is missing.");
    return;
  }

  // Remove existing script to avoid duplicates
  const existingScript = document.querySelector('script[src*="maps.googleapis.com"]');
  if (existingScript) existingScript.remove();

  const script = document.createElement("script");
  script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=initializeStreetView&v=weekly&loading=async`;
  script.async = true;
  script.defer = true;
  document.head.appendChild(script);
}

$(document).ready(function() {
  $('#view-selector .panel-list-item').on('click', function(event) {
    event.preventDefault();
    $('#view-selector .panel-list-item').removeClass('active-link');
    $(this).addClass('active-link');

    const viewToShow = $(this).data('view');
    $('.view-panel').addClass('hidden');
    $('.label').addClass('hidden');
    $('#' + viewToShow).removeClass('hidden');

    if (viewToShow === 'map') {
      setTimeout(() => {
        map.invalidateSize();
      }, 200);
    }
  });
});


// CLOCK AND DATE FUNCTION
function  updateClock(){
  const now = new Date();
  const hours = now.getHours() % 12 || 12;
  const minutes = now.getMinutes().toString().padStart(2, "0");
  const ampm = now.getHours() >= 12 ? "PM" : "AM";
  const formattedTime = `${hours}:${minutes} ${ampm}`;

  const options = { weekday: "short", month: "short", day: "numeric" };
  const formattedDate = now.toLocaleDateString("en-US", options);

  document.getElementById("clock").textContent = formattedTime;
  document.getElementById("date").textContent = formattedDate;
}

// Update clock every second
setInterval(updateClock, 1000);
updateClock(); // Initialize immediately



document.addEventListener('DOMContentLoaded', () => {
  const menuWrap = document.querySelector('.nav-but-wrap');
  if (menuWrap) {
    menuWrap.addEventListener('click', () => {
      toggleMenu();
    });
  }

  const streetViewButton = document.querySelector('[data-view="street"]');

  if (streetViewButton) {
    streetViewButton.addEventListener("click", () => {
      loadGoogleMapsAPI();
    });
  }
  const viewSelector = document.getElementById('view-selector');
  if (viewSelector) {
    viewSelector.addEventListener('click', (event) => {
      const li = event.target.closest('.panel-list-item');
      if (!li) return;

      const viewName = li.getAttribute('data-view');
      if (!viewName) return;

      // Optionally mark selected link as "active-link"
      document.querySelectorAll('.panel-list-item').forEach((item) => {
        item.classList.remove('active-link');
      });
      li.classList.add('active-link');

      // Hide all center panels
      document.querySelectorAll('.view-panel').forEach((panel) => {
        panel.style.display = 'none';
      });

      // Show only the chosen one
      const newActive = document.getElementById(viewName);
      if (newActive) {
        newActive.style.display = 'block';
      }

      // Stop the link from actually navigating (if using <a>)
      event.preventDefault();
    });
  }

});

(function($) {
  "use strict";
  const init = () => {
    const frame = document.querySelector('.frame');
    const menuIcon = document.querySelector('.menu-icon');

    if (menuIcon && frame) {
      menuIcon.addEventListener('click', () => {
        frame.classList.toggle('nav-active');
      });
    }
    const repositionBtn = document.getElementById('reposition-btn');
    if (repositionBtn) {
      repositionBtn.addEventListener('click', () => {
        // Re-center map or any other action
        map.setView([37.7178, -97.2921], 14);
      });
    }
  };
  init();
})(jQuery);

document.getElementById("radius-input").addEventListener("input", (e) => {
  document.getElementById("radius-value").textContent = e.target.value;
});

let geofenceCenter = null;
let geofenceRadius = 100;

document.getElementById("radius-input").addEventListener("input", (e) => {
  document.getElementById("radius-value").textContent = e.target.value;
});

document.getElementById("geofence-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const address = document.getElementById("address-input").value;
  const radius = parseInt(document.getElementById("radius-input").value);

  const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${apiKey}`;
  try {
    const response = await fetch(url);
    const data = await response.json();
    const location = data.results[0]?.geometry?.location;

    if (location) {
      geofenceCenter = [location.lat, location.lng];
      geofenceRadius = radius;

      
      document.querySelectorAll('.view-panel').forEach((panel) => {
        panel.classList.add('hidden');
      });
      document.getElementById('map').classList.remove('hidden');
      document.querySelector('.label')?.classList.add('hidden');

      
      setTimeout(() => {
        
        document.querySelectorAll('.panel-list-item').forEach((item) => {
          item.classList.remove('active-link');
        });
        document.querySelector('[data-view="map"]').classList.add('active-link');
      
        
        document.querySelectorAll('.view-panel').forEach((panel) => {
          panel.style.display = 'none';
        });
        const mapPanel = document.getElementById('map');
        if (mapPanel) {
          mapPanel.style.display = 'block';
          map.invalidateSize(); 
        }
      

        // Draw circle
        if (window.geofenceCircle) map.removeLayer(window.geofenceCircle);
        window.geofenceCircle = L.circle(geofenceCenter, {
          color: 'green',
          fillColor: '#3f3',
          fillOpacity: 0.2,
          radius: radius,
        }).addTo(map);

        map.setView(geofenceCenter, 15);
        console.log("Drew geofence at", geofenceCenter, "with radius", radius);
      }, 200);

      alert("Geofence set locally!");
    } else {
      alert("Failed to geocode address.");
    }
  } catch (err) {
    console.error("Geocoding error:", err);
    alert("Failed to set geofence.");
  }
});


