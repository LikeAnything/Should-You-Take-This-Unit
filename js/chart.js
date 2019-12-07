

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





function visualise(unitCode) {
      // Setting up the svg
      const svg = d3.select("body")
      .append("svg")
      .attr("height", "100%")
      .attr("width", "100%"),
      // get height and width automatically
      width = window.innerWidth||document.documentElement.clientWidth||document.body.clientWidth,
      height = window.innerHeight||document.documentElement.clientHeight||document.body.clientHeight,
      // margin = {left: 50, right: 50, top: 40, bottom: 0},


      chartGroup = svg.append("g").attr("class", "chart").attr("transform","translate("+width/2+","+height/2+")");

      // add a giant circle in the middle
      const circleRadius = height/3;
      chartGroup.append("circle")
            .attr("class", "back")
            .attr("r", circleRadius)  // roughly 1/3 size
            // .attr("cy", height/2)
            // .attr("cx", width/2)

      const padding = (height / 50),
            points = [
            {x: circleRadius * Math.cos(Math.PI/2), y: -circleRadius * Math.sin(Math.PI/2), text: "Assessment"},
            {x: circleRadius * Math.cos(21 * Math.PI/10), y: -circleRadius * Math.sin(21 * Math.PI/10), text: "Assessment"},
            {x: circleRadius * Math.cos(17 * Math.PI/10), y: -circleRadius * Math.sin(17* Math.PI/10), text: "Assessment"},
            {x: circleRadius * Math.cos(13 * Math.PI/10), y: -circleRadius * Math.sin(13* Math.PI/10), text: "Assessment"},
            {x: circleRadius * Math.cos(9 * Math.PI/10), y: -circleRadius * Math.sin(9* Math.PI/10), text: "Assessment"}
                  ],
            pentagonGroup = svg.append("g").attr("class", "pentagon");

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
            .attr("fill", "lightgray")
            .attr("d", line(points))
}

queryUnit();

