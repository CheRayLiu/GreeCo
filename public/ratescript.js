function initRateMap() {
    map = new google.maps.Map(document.getElementById('ratemap'), {
        center: {lat: 43.6532, lng: -79.3832},
        zoom: 15
    });

    document.getElementById("rate-btn").addEventListener("click", getLocation);
}

function getLocation() {
    infoWindow = new google.maps.InfoWindow;

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location: ' + pos.lat + "," + pos.lng);
            infoWindow.open(map);
            map.setCenter(pos);

            addRating(pos)

        }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }

    //TODO: DO the thing where you close the marker on the screen if more than one click.
}

function addRating(pos) {
    alert(pos.lat + "," + pos.lng);


    var text = '{ ' +
        '"employees" : [' +
        '{ "firstName":"John" , "lastName":"Doe" },' +
        '{ "firstName":"Anna" , "lastName":"Smith" },' +
        '{ "firstName":"Peter" , "lastName":"Jones" } ]}';

    var obj = JSON.parse(text);
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(this.map);
}

initRateMap()