---
---
updateFunctionTimer = undefined
muniMetaData  = undefined

window.stopSimulation = () ->
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

combineEvents = (slice) ->
  slice.reduce (acc, day) ->
    for own muni_id, infections of day when muni_id != 'total'
      acc[muni_id] = infections + (acc[muni_id] || 0)
    delete acc['total']
    acc

window.reduceEvents = (unprocessedEvents, timeStep) ->
  for start in [0 .. unprocessedEvents.length] by timeStep
    combineEvents(unprocessedEvents[start ... start+timeStep])

window.updatePolygonColors = (start, timeStep, unprocessedEvents, svgMapObject, position) ->
  ## assert: somewhere else manages curDay, and wraps it when it exceeds max day
  end = Math.min(start + timeStep, unprocessedEvents.length)

  muni_prevalence = combineEvents(unprocessedEvents[start...end])
  svgMapObject.selectAll(".district").style "fill-opacity", (d, muni_id) ->
    if muni_prevalence[muni_id]?
      Math.min((1000.0 / timeStep) * (muni_prevalence[muni_id] / (muniMetaData[muni_id]["pop"] || 1)), 1)
    else
      0.0

  if position == "right"
    $("#curDayDiv").html("Current period: "+start+"-"+end)

window.drawMap = (svgMapObject, tar) ->
  graticule = d3.geo.graticule();
  graticule.precision(0.001);
  graticule.extent([[-89.5,20.5],[-88.5,21.5]]);

  d3.json tar, (error, mx) ->
    svgMapObject.selectAll("path")
      .data(topojson.feature(mx, mx.objects.yucatan_municipalities).features)
      .enter().append("path")
      .attr({ d: path_projector, class: "district" });

    svgMapObject.append("g").selectAll("path")
      .data(topojson.feature(mx, mx.objects.MEX_adm1).features)
      .enter().append("path")
      .attr({ d: path_projector, class: "admin" });

    svgMapObject.append("path")
      .datum(graticule)
      .attr({ d: path_projector, class: "graticule" });

window.drawDailyEvents = (dayNumber, unprocessedEvents) ->
  if unprocessedEvents[dayNumber]?
    updateTimeSeriesIndicator(dayNumber, unprocessedEvents[dayNumber]['total'])

window.calculateTimeSeriesData = (unprocessedEvents) ->
  ([i, (day['total'] || 0)] for day, i in unprocessedEvents)

$ ->
  $('.runstate').click ->
    $(this).toggleClass('running')
    runSimulation()

  $('#dataSetMenu').change(() ->
    $this = $(this);
    tar = $this.find(':selected').parent().data('folder');
    intervention = $this.val();
    $.when(getDataset1(tar+"/base.json"), getDataset2(tar+"/"+intervention+".json"))
      .done () ->
        drawTsPlot(unprocessedEvents1, unprocessedEvents2)
  ).change()

  $displaymaps = $('#displaymaps');
  $.get $displaymaps.data('mapMetaSrc'), (json_string) ->
    console.log "Done downloading muni meta data processing"
    muniMetaData = json_string
