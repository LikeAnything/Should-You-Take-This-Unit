

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
      return {
            assessment: (height/3) * (4/5),
            feedback: (height/3) * (3/5),
            satisfaction: (height/3) * (2/5),
            resources: (height/3) * (4/5),
            activities: (height/3) * (5/5)
      }
}



function visualise(unitCode) {
      // Setting up the svg
      const svg = d3.select("#svgElem");
      svg.selectAll("*").remove();
      svg
      .append("svg")
      .attr("height", "100%")
      .attr("width", "100%"),
      // get height and width automatically
      width = window.innerWidth||document.documentElement.clientWidth||document.body.clientWidth,
      height = window.innerHeight||document.documentElement.clientHeight||document.body.clientHeight,
      // margin = {left: 50, right: 50, top: 40, bottom: 0},

      unitScores = getUnitScores(unitCode);


      chartGroup = svg.append("g").attr("class", "chart").attr("transform","translate("+width/2+","+height/2+")");

      const maxRadius = height/3;
      // add 5 concentric circles
      for (i = 0; i < 5; i++) {
            const circleRadius = maxRadius - (height/15)*i;
            chartGroup.append("circle")
                  .attr("class", "back")
                  .attr("stroke-opacity", String(1 - 0.2*i))
                  .attr("r", circleRadius) 
                  // .attr("cy", height/2)
                  // .attr("cx", width/2)
      }

      points = [
            {x: unitScores.assessment * Math.cos(Math.PI/2), y: - unitScores.assessment * Math.sin(Math.PI/2), text: "Assessment"},
            {x: unitScores.feedback * Math.cos(21 * Math.PI/10), y: -unitScores.feedback * Math.sin(21 * Math.PI/10), text: "Feedback"},
            {x: unitScores.satisfaction * Math.cos(17 * Math.PI/10), y: -unitScores.satisfaction  * Math.sin(17* Math.PI/10), text: "Satisfaction"},
            {x: unitScores.resources * Math.cos(13 * Math.PI/10), y: -unitScores.resources * Math.sin(13* Math.PI/10), text: "Resources"},
            {x: unitScores.activities * Math.cos(9 * Math.PI/10), y: -unitScores.activities * Math.sin(9* Math.PI/10), text: "Activities"}
                  ],

      // add a small circle to each point
      points.forEach(p => {
            chartGroup.append("circle")
                        .attr("class", "point")
                        .attr("cx", p.x)
                        .attr("cy", p.y)
                        .attr("r", 2)
                        // .text("Assessment");
            });
      
      // make a line generator
      const line = d3.line()
                  .x(d => d.x)
                  .y(d => d.y)
                  .curve(d3.curveCardinalClosed.tension(0.3));

      // add a path using the line generator
      chartGroup.append("path")
            .attr("fill", "green")
            .attr("fill-opacity", "0.5")
            .attr("stroke", "#003300")
            .attr("d", line(points))



}

queryUnit();

