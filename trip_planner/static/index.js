document.addEventListener('DOMContentLoaded', function() {
    const locationForm = document.getElementById('location-form');
    const loadLocationsBtn = document.getElementById('load-locations');
    const locationsDiv = document.getElementById('locations');
    const clearBtn = document.getElementById('clear-locations');
    const tableBodyElem = document.getElementById('data-rows');
    const generateMapBtn = document.getElementById('generate-map');
    const inputName = document.querySelector('input[name="name"]');
    const inputLocationName = document.querySelector('input[name="location_name"]');
    const deleteAllBtn = document.getElementById('delete-locations');

    clearBtn.addEventListener('click', function() {
        tableBodyElem.innerHTML = "";
    });

    deleteAllBtn.addEventListener('click', function() {
        fetch('/delete_all', {
            method: 'DELETE',
        })
        .then(data => {
            clearBtn.click();
        });
    });

    generateMapBtn.addEventListener('click', function() {
        fetch('/generate_map')
        .then(response => response.json())
        .then(data => {
            console.log(data);
        });
    });

    locationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(locationForm);
        fetch('/add_locations', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            setTimeout(() => {
                loadLocationsBtn.click();
            }, 5000);
            setTimeout(() => {
                generateMapBtn.click();
                setTimeout(() => {
                    location.reload();
                }, 3000);
            }, 15000);
        })
        .catch(error => console.error('Error:', error));
    });

    function render_locations(locations) {
        let rows = "";
        const order = ["id", "name", "location", "latitude", "longitude", "distance"]
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
                tableBodyElem.innerHTML = render_locations(locations);
                inputName.value = "";
                inputLocationName.value = "";
            }
        })
        .catch(error => console.error('Error:', error));
    });

    loadLocationsBtn.click();
});