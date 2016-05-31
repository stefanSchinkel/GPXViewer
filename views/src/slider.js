/*global $, stats, track, marker, info */
/*jshint -W081 */
$(function () {
  "use strict";
  function formatTime(seconds) {
    var hours = Math.floor(seconds / 3600);
    var mins = Math.floor((seconds - (hours * 3600)) / 60);
    var secs = seconds - (hours * 3600) - (mins * 60);
    if (hours   < 10) {hours   = "0" + hours; }
    if (mins < 10) {mins = "0" + mins; }
    if (secs < 10) {secs = "0" + secs; }
    return hours + ":" + mins + ":" + secs;
  }


  $("#slider").slider({
    step: 1,
    max: stats.length,
    values: [1],
    slide: function (event, ui) {
      var idx, lat, lon, d, v, tms, msg;
      idx = ui.values[0];
      lat = track[idx][0];  //
      lon = track[idx][1];

      // distance
      d = stats[idx][0] / 1000;
      d = d.toFixed(2);

      // time
      tms = formatTime(stats[idx][1]);

      // speed
      v = stats[idx][2].toFixed(2);
      if (v.length < 5) {
        console.log(v)
        console.log('++++')
        v = '&nbsp;' + v;
        console.log(v)
        }


      msg = d + "  km<br />" + tms + "  h<br> "  + v + "  km/h";

      // write to info box
      info.update({"time" : msg});

      // move the marker
      marker.setLatLng([lat, lon]);
    }
  }); //function
}); // jQuery
