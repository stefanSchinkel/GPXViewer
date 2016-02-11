/*global $, track */

$(function () {
  "use strict";
  $("#slider").slider({
    step: 1,
    max: track.length,
    values: [1],
    slide: function (event, ui) {
      var idx, d, v,  msg;
      idx = ui.values[0];

      // order is lat, lon, distance, time, speed
      d = track[idx][2] / 1000;
      d = d.toFixed(2);
      v = track[idx][4].toFixed(2);

      if (v.length === 4) {
        v = ' ' + v;
      }

      msg = d + " km " + "00:00h " + v + "km/h";
      $("#stats").text(msg);
    }
  }); //function
}); // jQuery
