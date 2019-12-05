// Setting up the svg
const svg = d3.select("body")
              .append("svg")
              .attr("height", "100%")
              .attr("width", "100%"),
      // get height and width automatically
      width = window.innerWidth||document.documentElement.clientWidth||document.body.clientWidth,
      height = window.innerHeight||document.documentElement.clientHeight||document.body.clientHeight,
      // margin = {left: 50, right: 50, top: 40, bottom: 0},
      chartGroup = svg.append("g").attr("transform","translate("+width/2+","+height/2+")");

// add a giant circle in the middle
chartGroup.append("circle")
          .attr("class", "back")
          .attr("r", height/3)  // roughly 1/3 size
          // .attr("cy", height/2)
          // .attr("cx", width/2)
