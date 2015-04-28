$(function () {
  $("#slider").slider({
    step : 1,
    max: track.length,
    values: [1],
    slide: function (event, ui) {
      var idx = ui.values[0];
      $("#stats").text("Pos " + idx + " lat: " + track[idx][0] + " lon: " + track[idx][1]);
    }
  }); //function
}); // jQuery
