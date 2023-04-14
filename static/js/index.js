const UNIVERSITY_BOUNDS = {
  north: 32.2889202745635,
  south: 32.25945500590698,
  west: -106.76882238451887,
  east: -106.72869806516044
};

// based on https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete
function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
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

  const input = document.getElementById("pac-input");

  const options = {
    strictBounds: true
  };

  const autocomplete = new google.maps.places.Autocomplete(input, options);

  autocomplete.setBounds(UNIVERSITY_BOUNDS);

  const infowindow = new google.maps.InfoWindow();
  const infowindowContent = document.getElementById("infowindow-content");

  infowindow.setContent(infowindowContent);

  const marker = new google.maps.Marker({
    map,
    anchorPoint: new google.maps.Point(0, -29),
  });

  autocomplete.addListener("place_changed", () => {
    infowindow.close();
    marker.setVisible(false);

    const place = autocomplete.getPlace();

    // If the place has a geometry, then present it on a map.
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(17);
    }

    marker.setPosition(place.geometry.location);
    marker.setVisible(true);
    infowindowContent.children["place-name"].textContent = place.name;
    infowindowContent.children["place-address"].textContent =
      place.formatted_address;
    infowindow.open(map, marker);
  });

  var pac_input = document.getElementById('pac-input'); // go to first result on enter press https://stackoverflow.com/questions/7865446/google-maps-places-api-v3-autocomplete-select-first-option-on-enter
  (function pacSelectFirst(input) {
      // store the original event binding function
      var _addEventListener = (input.addEventListener) ? input.addEventListener : input.attachEvent;

      function addEventListenerWrapper(type, listener) {
          // Simulate a 'down arrow' keypress on hitting 'return' when no pac suggestion is selected,
          // and then trigger the original listener.
          if (type == "keydown") {
              var orig_listener = listener;
              listener = function(event) {
                  var suggestion_selected = $(".pac-item-selected").length > 0;
                  if (event.which == 13 && !suggestion_selected) {
                      var simulated_downarrow = $.Event("keydown", {
                          keyCode: 40,
                          which: 40
                      });
                      orig_listener.apply(input, [simulated_downarrow]);
                  }

                  orig_listener.apply(input, [event]);
              };
          }

          _addEventListener.apply(input, [type, listener]);
      }

      input.addEventListener = addEventListenerWrapper;
      input.attachEvent = addEventListenerWrapper;
  })(pac_input);
}

window.initMap = initMap;