<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Trip Planner</title>
</head>
<body>
    <div>
        <form action="/add_location" method="post" id="location-form">
            Name: <input type="text" name="name" required>
            Location Name: <input type="text" name="location_name" required>
            <input type="submit" value="Add Location">
        </form>
    </div>
    <br>
    <div>
        <button id="load-locations">Load Locations</button>
        <div id="locations"></div>
    </div>
    <div>
        <a href="/map">Show me the map</a>
    </div>
    <script src="/static/index.js"></script>
</body>
</html>