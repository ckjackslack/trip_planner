document.addEventListener('DOMContentLoaded', function() {
    const locationForm = document.getElementById('location-form');
    const loadLocationsBtn = document.getElementById('load-locations');
    const locationsDiv = document.getElementById('locations');
    const clearBtn = document.getElementById('clear-locations');
    const tableBodyElem = document.getElementById('data-rows');
    const generateMapBtn = document.getElementById('generate-map');
    const inputName = document.querySelector('input[name="name"]');
    const inputLocationName = document.querySelector('input[name="location_name"]');

    clearBtn.addEventListener('click', function() {
        tableBodyElem.innerHTML = "";
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
        fetch('/add_location', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            loadLocationsBtn.click();
            generateMapBtn.click();
            setTimeout(() => location.reload(), 1000);
        })
        .catch(error => console.error('Error:', error));
    });

    function render_locations(locations) {
        let rows = "";
        for (const loc of locations) {
            rows += `<tr><td>${loc.join("</td><td>")}</td></tr>`;
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