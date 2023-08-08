document.addEventListener('DOMContentLoaded', function() {
    const locationForm = document.getElementById('location-form');
    const loadLocationsBtn = document.getElementById('load-locations');
    const locationsDiv = document.getElementById('locations');

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
        })
        .catch(error => console.error('Error:', error));
    });

    function render_locations(locations) {
        const header_cols = ["ID", "Name", "Location name", "Lat", "Lon"];
        const header_as_str = "<th>" + header_cols.join("</th><th>") + "</th>";
        let content = `<table><thead><tr>${header_as_str}</tr></thead><tbody>`;
        for (const loc of locations) {
            content += `<tr><td>${loc.join("</td><td>")}</td></tr>`;
        }
        return content + "</tbody></table>";
    }

    loadLocationsBtn.addEventListener('click', function() {
        fetch('/get_locations')
        .then(response => response.json())
        .then(data => {
            const locations = data.locations;
            console.log(locations);
            locationsDiv.innerHTML = render_locations(locations);
            locationForm.childNodes[1].value = "";
            locationForm.childNodes[3].value = "";
        })
        .catch(error => console.error('Error:', error));
    });

    loadLocationsBtn.click();
});