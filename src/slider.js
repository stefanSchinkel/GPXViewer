/*global $, track */


$(function () {
"use strict";
  $("#slider").slider({
    step: 1,
    max: track.length,
    values: [1],
    slide: function (event, ui) {
      var idx = ui.values[0];
      // order is lat, lon, distance, speed
      var msg = "Pos: " + idx + " " +
            "lat: " + track[idx][0].toFixed(2) + " " +
            "lon: " + track[idx][1].toFixed(2) + " " +
            "V: " + track[idx][3].toFixed(2)  + " " +
            "Dist: " + track[idx][2].toFixed(2);

      $("#stats").text(msg);
    }
  }); //function
}); // jQuery
