var express = require('canvas')
var dygraph = require('dygraphs')

module.exports = { 
  testChart: function () {
    // var Dygraph   = dygraph.Dygraph;
    new Dygraph(div, "ny-vs-sf.txt", {
      legend: 'always',
      title: 'NYC vs. SF',
      showRoller: true,
      rollPeriod: 14,
      customBars: true,
      ylabel: 'Temperature (F)',
    });
  }
}