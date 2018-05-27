heatmap = new google.maps.visualization.HeatmapLayer({
        data:[],
        map: null
    });

function init(){
    document.getElementById("enter").addEventListener("click", getLeafN);
    array = document.getElementsByClassName("leaflabel");
    for(i = 0; i<array.length; i++){
        array[i].addEventListener("click", updateColors);
    }

    map = new google.maps.Map(document.getElementById('ratemap'), {
        center: {lat: 43.752594, lng: -79.313432},
        zoom: 15
    });

    document.getElementById("rate-btn").addEventListener("click", getLocation);

   // document.getElementById("subm").addEventListener("click", pushData);

    google.maps.event.addListener(map, "bounds_changed", function() {
       // send the new bounds back to your server
       var bounds = map.getBounds().toJSON();
       requestsRating(bounds["east"], bounds["west"], bounds["south"], bounds["north"],10);
       console.log("call heatmap request");
    });

    requestsRating(-79.313432,-79.437372 ,43.752594,43.634184, 0);
}

function initRateMap(lng, lat, rat) {
    heatmap.setMap(null);
    heatmap = new google.maps.visualization.HeatmapLayer({
        data: getPoints(lng, lat, rat),
        map: map,
        radius: 75,
        dissipating: true,
        maxIntensity: 5
    })

    //google.maps.event.addListener(map, "", function() {
   // send the new bounds back to your server
   //setBound(map.getBounds(),10);
//});
}

var gradient = [
        'rgba(0,0,0,0)',
        'rgba(0,0,0,0)',
        'rgba(0, 191, 255, 1)',
        'rgba(0, 127, 255, 1)',
        'rgba(0, 63, 255, 1)',
        'rgba(0, 0, 255, 1)',
        'rgba(0, 0, 223, 1)',
        'rgba(0, 0, 191, 1)',
        'rgba(0, 0, 159, 1)',
        'rgba(0, 0, 127, 1)',
        'rgba(63, 0, 91, 1)',
        'rgba(127, 0, 63, 1)',
        'rgba(191, 0, 31, 1)',
        'rgba(255, 0, 0, 1)'
        ];



function requestsRating(longlo, longhi, latlo, lathi, slide){
    console.log("made request")
    var data = {longloJ:longlo, longhiJ: longhi, latloJ: latlo, lathiJ: lathi,slideJ:slide}
    var path = 'http://localhost:8000/ratings/map/';
    var xhr = new XMLHttpRequest();
    xhr.open("POST", path);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");  //Send the proper header info

    xhr.onreadystatechange = function() {//Call a function when the state changes (i.e. response comes back)
        // Update the dropdown when response is ready
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            var nodeList = JSON.parse(this.responseText);
            initRateMap(nodeList['long'], nodeList['lat'], nodeList['wt'])
        }
        else{
            console.log("Server Response: Error"); //RME
        }
    };
    console.log(data)
    var jsonString= JSON.stringify(data);     //generate JSON string
    xhr.send(jsonString);                       //send request to server
    // document.getElementById("console").innerHTML += "Sent request to " + path + ": "  + jsonString + "<br>"; //RME


}

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
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
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'Error: Please enable location services.' :
        'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(this.map);
}

function getPoints(lng, lat, rat) {

    var result = [];
    for (var i = 0 ; i < lat.length ; i++) {
        result.push(
            {location: new google.maps.LatLng(lat[i], lng[i]), weight:rat[i]}
            );
    }
    return result;
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

init();