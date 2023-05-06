const UNIVERSITY_BOUNDS = {
  north: 32.2889202745635,
  south: 32.25945500590698,
  west: -106.76882238451887,
  east: -106.72869806516044
};

var marker = null;

// based on https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete
function initMap2() {
  const map2 = new google.maps.Map(document.getElementById("map2"), {
    center: { lat: 32.28296453439094, lng: -106.75150567938039 },
    restriction: {
      latLngBounds: UNIVERSITY_BOUNDS,
      strictBounds: false,
    },
    minZoom: 17,
    maxZoom: 19,
    zoom: 18,
    mapTypeControl: false,
  });

  var center_position = { lat: 32.28296453439094, lng: -106.75150567938039 };
  marker = new google.maps.Marker({
    position: center_position,
    map2,
    anchorPoint: new google.maps.Point(0, -29),
  });
  marker.setMap(map2);

  google.maps.event.addListener(map2, 'idle', function(){
      console.log('this logs after the panTo finishes.');
      if(document.getElementById("location") != null)
      {
        marker.setMap(null);
        document.getElementById("location").value = map2.getBounds().getCenter()
        var center_position = map2.getBounds().getCenter()
        marker = new google.maps.Marker({
          position: center_position,
          map2,
          anchorPoint: new google.maps.Point(0, -29),
        });
        marker.setMap(map2);
      }
  });
}

window.initMap2 = initMap2;
