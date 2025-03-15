const API_SERVER = 'https://fifteen598.pythonanywhere.com';
const map = L.map('map').setView([37.71783399900819, -97.29209838253563], 15);

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
    const homeCoords = [37.71783399900819, -97.29209838253563];

    let index = 1;
    for (const [user, coords] of Object.entries(users)) {
        const userCoords = [coords.latitude, coords.longitude];
        const distance = map.distance(userCoords, homeCoords);
        const isHome = distance <= 100;

        // Get both Home and Away images
        const homeImage = document.getElementById(`status_home_${index}`);
        const awayImage = document.getElementById(`status_away_${index}`);
        if (isHome) {
            awayImage.style.display = "none";
            homeImage.style.display = "block";
        } else {
            homeImage.style.display = "none";
            awayImage.style.display = "block";
        }
        index++;
        if (index > 5) break; // Ensure we don't exceed the set number of images
    }
}

async function updateLocation(name, latitude, longitude) {
    try {
      const response = await fetch(`${FLASK_SERVER_URL}/update_location`, {
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

(function($) { "use strict";

	window.test = function () {
		var body = undefined;
		var menu = undefined;
		var menuItems = undefined;
		var init = function init() {
			body = document.querySelector('body');
			menu = document.querySelector('.menu-icon');
			menuItems = document.querySelectorAll('.nav__list-item');
			applyListeners();
		};
		var applyListeners = function applyListeners() {
			menu.addEventListener('click', function () {
				return toggleClass(body, 'nav-active');
			});
		};
		var toggleClass = function toggleClass(element, stringClass) {
			if (element.classList.contains(stringClass)) element.classList.remove(stringClass);else element.classList.add(stringClass);
		};
		init();
	}();        
              
})(jQuery); 
