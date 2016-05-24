/*global $, stats, track, marker */

$(function () {
  "use strict";
  $("#slider").slider({
    step: 1,
    max: stats.length,
    values: [1],
    slide: function (event, ui) {
      var idx, lat, lon, d, v, time, minutes, seconds, hours, msg;
      idx = ui.values[0];
      lat = track[idx][0];
      lon = track[idx][1];
      // order is distance, duration, speed
      d = stats[idx][0] / 1000;
      d = d.toFixed(2);
      time = stats[idx][1];

      hours = Math.floor(time / 3600);
      minutes = Math.floor((time - (hours * 3600)) / 60);
      seconds = time - (hours * 3600) - (minutes * 60);

      if (hours   < 10) {hours   = "0" + hours; }
      if (minutes < 10) {minutes = "0" + minutes; }
      if (seconds < 10) {seconds = "0" + seconds; }
      var tms = hours + ":" + minutes + ":" + seconds;
      v = stats[idx][2].toFixed(2);

      if (v.length < 5) { v = ' ' + v; }

      msg = d + " km " + tms + "h "  + v + "km/h";
      $("#stats").text(msg);

      // move the marker
      marker.setLatLng([lat, lon]);
    }
  }); //function
}); // jQuery
