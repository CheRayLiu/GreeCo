var currentLocation;

function init(){
    document.getElementById("enter").addEventListener("click", getLeafN);
    array = document.getElementsByClassName("leaflabel");
    for(i = 0; i<array.length; i++){
        array[i].addEventListener("click", updateColors);
    }

    initRateMap()
}

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

            currentLocation = JSON.parse(JSON.stringify(pos));

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location: ' + pos.lat + "," + pos.lng);
            infoWindow.open(map);
            map.setCenter(pos);

            // Make rating panel visible
            document.getElementById("ratings-panel").classList.remove("display-none");
            document.getElementById("enter").addEventListener("click", addRating);


        }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }

    //TODO: DO the thing where you close the marker on the screen if more than one click. some for event listener perhaps.
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'Error: Please enable location services.' :
        'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(this.map);
}

function getLeafN(){
    var array = document.getElementsByName("leafn");
    for(i=0; i<array.length;i++){
        if(array[i].checked){
            return array[i].value;
        }
    }
}

function updateColors(){
    //alert("col");
    upTo = getLeafN()-1;
    var array = document.getElementsByName("leafn");
    for(i=0; i<= upTo;i++){
        array[i].parentElement.classList.add("green");
    }
    for(i=upTo+1; i<= array.length;i++){
        array[i].parentElement.classList.remove("green");
    }
}

function addRating() {
    //alert(getLeafN() + "," + currentLocation.lat + "," + currentLocation.lng);
    var params = JSON.stringify({lat:Number(currentLocation.lat), long:Number(currentLocation.lng), rating:Number(getLeafN())});
    var path = 'http://localhost:8000/ratings/rate/';
    var xhr = new XMLHttpRequest();
    xhr.open("POST", path);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.readystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            alert("Success");

        }
        else{
            alert("Error");
        }
    }
    xhr.send(params);

}

init()
