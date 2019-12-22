

const unitData = data().sort(function (a, b) {
      return a.unitCode > b.unitCode ? 1 : -1;
});

function queryUnit() {
      $(document).ready(function() {

            // the submission button is disabled by default
            document.getElementById("submit").disabled = true;

            const unitList = Array.from(document.getElementById("units").options).map(e => e.value);

            // toggle the submission button so that it is disabled when the input is not in the unit list
            const toggleSubmit = () => {
                  if (unitList.includes(document.getElementById("inputField").value.trim().toUpperCase())) {
                        document.getElementById("submit").disabled = false;
                  }
                  else {
                        document.getElementById("submit").disabled = true;
                  }
            }

            // only allow the user to submit when the input is valid (it must be an option in the datalist)
            $("#inputField").on("input", function () {
                  toggleSubmit();
            });

            // on submission of the form, perform visulisation for the chosen unit
            document.getElementById("form").onsubmit = () => {
            const chosenUnit = document.getElementById("inputField").value.trim().toUpperCase();


            // visualise the chosen unit
            visualise(chosenUnit);


            // After submission, clear the input field and disable submit button
            document.getElementById("inputField").value = "";
            document.getElementById("submit").disabled = true;

            // Stop form from submitting
            return false;
            };

        });
}



function getUnitScores(unitCode) {
      for (i = 0; i < unitData.length; i++) {
            const u = unitData[i];
            if (u.unitCode.toUpperCase() === unitCode.toUpperCase()) {
                  return u
            }
      }
      return { 
            unitCode: 'FIT1003',
            campus: 'SAFRICA',
            year: '2019',
            semester: '1',
            assessment: 3.2288948145676066,
            feedback: 2.071678029963506,
            satisfaction: 3.415435914654315,
            resources: 3.8363324412685156,
            activities: 2.534565720155106,
            };
}


// points going around the pentagon (clockwise)
const pentagonPoints = [
      {x: Math.cos(Math.PI/2),       y: Math.sin(Math.PI/2)},
      {x: Math.cos(21 * Math.PI/10), y: Math.sin(21 * Math.PI/10)},
      {x: Math.cos(17 * Math.PI/10), y: Math.sin(17* Math.PI/10)},
      {x: Math.cos(13 * Math.PI/10), y: Math.sin(13* Math.PI/10)},
      {x: Math.cos(9 * Math.PI/10),  y: Math.sin(9* Math.PI/10)}
      ],
      axisLabels = ["assessment", "feedback", "satisfaction","resources", "activities"]


function drawUnit(svgGroup, unitCode, maxRadius){
      /*
       * Draws a unit on the svgGroup.
       */
      const unitScores = getUnitScores(unitCode),
      // make a line generator
      line = d3.line()
                  .x(d => d.x)
                  .y(d => d.y)
                  .curve(d3.curveCardinalClosed.tension(0.3)),
      // get points using the pentagon scale
      points = pentagonPoints.map((e, i) => {const para = axisLabels[i];
                                             return {x: e.x * unitScores[para], y: - e.y * unitScores[para]}})
                             .map(p => {p.x *= maxRadius / 5; p.y *= maxRadius / 5; return p});
      // pick a colour
      colour = d3.interpolateRainbow(Math.random());
      // colour = d3.color(d3.interpolateRainbow(Math.random())).brighter(0.5);  // makes a colour brighter. not sure if necessary..


      // add a path using the line generator
      svgGroup.append("path")
              .attr("class", "area")
              .attr("fill", colour)
              .attr("d", line(points))

      // add a small circle to each point
      points.forEach(p => {
            svgGroup.append("circle")
                    .attr("class", "point")
                    .attr("cx", p.x)
                    .attr("cy", p.y)
                    .attr("r", 2)
            });

}


function visualise(unitCode) {
      // Setting up the svg
      const svg = d3.select("#svgElem");
      svg.selectAll("*").remove();
      svg.append("svg")
         .attr("height", "100%")
         .attr("width", "100%");

      // useful parameters
      // get height and width automatically
      const width = window.innerWidth||document.documentElement.clientWidth||document.body.clientWidth,
      height = window.innerHeight||document.documentElement.clientHeight||document.body.clientHeight,
      maxRadius = height/3;

      // group where area will be added
      const chartGroup = svg.append("g").attr("class", "chart").attr("transform","translate("+width/2+","+height/2+")");
      drawUnit(chartGroup, unitCode, maxRadius);


      // add 5 concentric circles
      for (i = 0; i < 5; i++) {
            const circleRadius = maxRadius - (height/15)*i;
            chartGroup.append("circle")
                  .attr("class", "back")
                  .attr("stroke-opacity", String(1 - 0.2*i))
                  .attr("r", circleRadius)
      }

      // creating axes
      const axisGroup = chartGroup.append("g").attr("class", "axis"),
            linearScale = d3.scaleLinear()
                            .domain([0, 100])
                            .range([maxRadius, 0]);
      for (i = 0; i < 5; i++) {
            // make a new group for each axis
            let group = axisGroup.append("g")
                     .attr("class", "axis a"+i)
                     .attr("transform","rotate("+ i * 72 +") " +"translate(0,-"+maxRadius+")")
            let axis = d3.axisLeft(linearScale);
            group.call(axis)
      }
}






queryUnit();
