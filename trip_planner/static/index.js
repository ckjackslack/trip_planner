var recentLocations = null;

document.addEventListener('DOMContentLoaded', function() {
    const clearBtn = document.getElementById('clear-locations');
    const deleteAllBtn = document.getElementById('delete-locations');
    const generateMapBtn = document.getElementById('generate-map');
    const inputLocs = document.querySelector('textarea[name="locs"]');
    const inputPlace = document.querySelector('input[name="place"]');
    const loadLocationsBtn = document.getElementById('load-locations');
    const locationForm = document.getElementById('location-form');
    const mapFrame = document.getElementById('map-frame');
    const tableBodyElem = document.getElementById('data-rows');

    clearBtn.addEventListener('click', function() {
        tableBodyElem.innerHTML = "";
    });

    deleteAllBtn.addEventListener('click', function() {
        fetch('/clear_locations', {
            method: 'DELETE',
        })
        .then(data => {
            clearBtn.click();
            setTimeout(function() {
                generateMapBtn.click();
            }, 2000);
        });
    });

    generateMapBtn.addEventListener('click', function() {
        fetch('/create_map')
        .then(response => {
            setTimeout(function() {
                mapFrame.contentWindow.location.reload();
            }, 2000);
        });
    });

    function render_locations(locations) {
        let rows = "";
        const order = [
            "id",
            "name",
            "location",
            "latitude",
            "longitude",
            "distance",
        ]
        let row = [];
        for (let loc of locations) {
            row = order.map((o) => loc[o]);
            rows += `<tr><td>${row.join("</td><td>")}</td></tr>`;
        }
        return rows;
    }

    loadLocationsBtn.addEventListener('click', function() {
        fetch('/get_locations')
        .then(response => response.json())
        .then(data => {
            const locations = data.locations;
            if (locations) {
                recentLocations = locations;
                tableBodyElem.innerHTML = render_locations(locations);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    locationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(locationForm);
        let size = formData.get("locs").split("\n").length;
        if (size > 5) {
            alert("Cannot add more than 5 locations at once.");
            return;
        }
        fetch('/add_locations', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            loadLocationsBtn.click();
            inputPlace.value = "";
            inputLocs.value = "";
            setTimeout(function() {
                generateMapBtn.click();
            }, 1000);
        })
        .catch(error => console.error('Error:', error));
    });

    loadLocationsBtn.click();
});