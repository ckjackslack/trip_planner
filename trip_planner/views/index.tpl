<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Trip Planner</title>
    <link rel="stylesheet" type="text/css" href="/static/bulma.min.css">
</head>
<body>
    <section class="section">
        <div class="container">
            <h1 class="title">Trip Planner</h1>
            <form action="/add_location" method="post" id="location-form">
                <div class="field">
                    <label class="label">Place</label>
                    <div class="control">
                        <input class="input" type="text" name="place" required>
                    </div>
                </div>
                <div class="field">
                    <label class="label">Locations</label>
                    <div class="control">
                        <textarea class="textarea" name="locs"></textarea>
                    </div>
                </div>
                <div class="field">
                    <div class="control">
                        <button type="submit" class="button is-link">Add Locations</button>
                    </div>
                </div>
            </form>
            <br>

            <button id="load-locations" class="button is-info">Load Locations</button>
            <button id="clear-locations" class="button is-danger">Clear</button>
            <button id="generate-map" class="button is-warning">Generate map</button>
            <button id="delete-locations" class="button is-danger">Delete all</button>

            <div id="locations" class="content mt-4">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Location name</th>
                            <th>Latitude</th>
                            <th>Longitude</th>
                        </tr>
                    </thead>
                    <tbody id="data-rows">
                    </tbody>
                </table>
            </div>

            <iframe src="/map" width="800" height="600"></iframe>
            <br>
            <a href="/map">Show map on separate page</a>
        </div>
    </section>
    <script src="/static/index.js"></script>
</body>
</html>