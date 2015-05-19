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

$ ->
  $('.runstate').click ->
    $(this).toggleClass('running')
    runSimulation()
