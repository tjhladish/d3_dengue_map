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

window.updatePolygonColors = (start, timeStep, unprocessedEvents, svgMapObject, position) ->
  ## assert: somewhere else manages curDay, and wraps it when it exceeds max day
  end = start + timeStep
  end = unprocessedEvents.length if end > unprocessedEvents.length

  muni_prevalence = unprocessedEvents[start...end].reduce (acc, day) ->
    for own muni, infections of day when muni != 'total'
      acc[muni] ?= 0
      acc[muni] += infections
    acc

  for muni_obj, muni_id in svgMapObject.selectAll(".district")[0]
    if muni_prevalence[muni_id]?
      yvalue = (1000.0 / timeStep) * (muni_prevalence[muni_id] / (muniMetaData[muni_id]["pop"] || 1)) * 255
      yvalue = 255 if yvalue > 255
      muni_obj.style["fill-opacity"] = yvalue/255
      # if position == "left"
      #
      # else
      #   muni_obj.style["fill"] = d3.rgb 255-yvalue*0.8, 255-yvalue*0.5, 255-yvalue*0.2
    else
      muni_obj.style["fill-opacity"] = 0.0

  if position == "right"
    $("#curDayDiv").html("Current period: "+start+"-"+end)

# mapper = (src) ->
#     graticule = d3.geo.graticule();
#     graticule.precision(0.001);
#     graticule.extent([[-89.5,20.5],[-88.5,21.5]]);
#
#     d3.json src, (error, mx) ->
#       svgMapObject.selectAll("path")
#         .data(topojson.object(mx, mx.objects.yucatan_municipalities).geometries)
#         .enter().append("path")
#         .attr("d", path_projector)
#         .style("stroke", "#333")
#         .style("stroke-width", ".2px")
#         .attr("class", "district")
#         .style("fill", "white");
#      g = svgMapObject.append("g");
#      g.selectAll("path")
#         .data(topojson.object(mx, mx.objects.MEX_adm1).geometries)
#         .enter().append("path")
#         .attr("d", path_projector)
#         .attr("fill", "transparent")
#         .style("stroke", "#333");
#      svgMapObject.append("path")
#        .datum(graticule)
#        .attr("class", "graticule")
#        .attr("d", path_projector);

$ ->
  $('.runstate').click ->
    $(this).toggleClass('running')
    runSimulation()

  # $mapdiv = $('.displaymaps')
  # mapsrc = $mapdiv.data('mapSrc')
  # refmap = d3.select('.displaymaps > svg').append('defs').append('g').attr('id','districts')
  # d3.json mapsrc, (error, districtlines) ->
  #   refmap.data(topojson.object(districtlines, districtlines.objects.yucatan_municipalities).geometries)
  #
  # $mapdiv.children('.map').each (i) ->
  #   console.log(this.id, mapsrc)
