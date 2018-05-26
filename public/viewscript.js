function initViewMap() {
    map = new google.maps.Map(document.getElementById('viewmap'), {
        center: {lat: 43.6532, lng: -79.3832},
        zoom: 15
    });
}

initViewMap()