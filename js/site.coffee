---
---
updateFunctionTimer = undefined

stopSimulation = () ->
  if updateFunctionTimer?
    clearInterval(updateFunctionTimer)
    updateFunctionTimer = undefined

startSimulation = () ->
  if not updateFunctionTimer?
    updateFunctionTimer = setInterval(update,1);

runSimulation = () ->
  if updateFunctionTimer?
    stopSimulation()
  else
    startSimulation()

mapper = (src) ->
    graticule = d3.geo.graticule();
    graticule.precision(0.001);
    graticule.extent([[-89.5,20.5],[-88.5,21.5]]);

    d3.json src, (error, mx) ->
      svgMapObject.selectAll("path")
        .data(topojson.object(mx, mx.objects.yucatan_municipalities).geometries)
        .enter().append("path")
        .attr("d", path_projector)
        .style("stroke", "#333")
        .style("stroke-width", ".2px")
        .attr("class", "myyuc")
        .style("fill", "white");
     g = svgMapObject.append("g");
     g.selectAll("path")
        .data(topojson.object(mx, mx.objects.MEX_adm1).geometries)
        .enter().append("path")
        .attr("d", path_projector)
        .attr("fill", "transparent")
        .style("stroke", "#333");
     svgMapObject.append("path")
       .datum(graticule)
       .attr("class", "graticule")
       .attr("d", path_projector);

$ ->
  $('.runstate').click ->
    $(this).toggleClass('running')
    runSimulation()

  $mapdiv = $('.displaymaps')
  mapsrc = $mapdiv.data('mapSrc')
  refmap = d3.select('.displaymaps > svg').append('defs').append('g').attr('id','districts')
  d3.json mapsrc, (error, districtlines) ->
    refmap.data(topojson.object(districtlines, districtlines.objects.yucatan_municipalities).geometries)

  $mapdiv.children('.map').each (i) ->
    console.log(this.id, mapsrc)
