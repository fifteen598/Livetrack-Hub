const API_SERVER = 'https://fifteen598.pythonanywhere.com';
const map = L.map('map').setView([37.7178, -97.2921], 14);
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors & CartoDB'
}).addTo(map);

async function fetchAndUpdate() {
  try {
      const response = await fetch(`${API_SERVER}/fetch_records`);
      const users = await response.json();
      updateStatuses(users); 
  } catch (error) {
      console.error("Error fetching data:", error);
  }
}

function updateStatuses(users) {
  const homeCoords = [37.72407864223953, -97.1753984504353];
  const statusContainer = document.getElementById("status-container");

  statusContainer.innerHTML = "";

  Object.entries(users).forEach(([user, coords]) => {
      const userCoords = [coords.latitude, coords.longitude];
      const distance = map.distance(userCoords, homeCoords);
      const isHome = distance <= 100;


      const statusElement = document.createElement("div");
      statusElement.classList.add("status-item");
      statusElement.innerHTML = `
          <span class="status-name">${user}</span>
          <span class="status-text ${isHome ? "home" : "away"}">${isHome ? "Home" : "Away"}</span>
      `;

      statusElement.addEventListener("click", () => {
          map.setView(userCoords, 17);
      });

      // Append to status container
      statusContainer.appendChild(statusElement);

      // Animate status change
      setTimeout(() => {
          statusElement.classList.add("fade-in");
      }, 100);
  });
}


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
}
document.addEventListener('DOMContentLoaded', () => {
  const menuWrap = document.querySelector('.nav-but-wrap');
  if (menuWrap) {
    menuWrap.addEventListener('click', () => {
      toggleMenu();
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


