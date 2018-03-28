//MARGIN
var margin = {top: 20, right: 55, bottom: 40, left: 60},
    width  = 1000 - margin.left - margin.right,
    height = 400  - margin.top  - margin.bottom;

//PARSEDATE
var parseDate = d3.time.format("%m/%d/%Y").parse;

// X e Y RANGE
var x = d3.time.scale()
        .range([0, width]);
var y = d3.scale.linear()
      .rangeRound([height, 0]);

//LINE
var line = d3.svg.line()
    .interpolate("bundle")
    .x(function (d) { return x(d.Date)})
    .y(function (d) { return y(d.value); });


//COLOR RANGE
var color = d3.scale.ordinal()
      .range(["#1f5188", "#b10318"]);

//SVG
var svg = d3.select("#graph").append("svg")
    .attr("width",  width  + margin.left + margin.right)
    .attr("height", height + margin.top  + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//TABLE
var table = d3.select("#table-location")
    .append("table")
    .attr("class", "table"),
    thead = table.append("thead"),
    tbody = table.append("tbody");

//DATA
d3.csv("/static/conrace.csv", function (error, data) {
        data.forEach(function(d) {
            d.Date = parseDate(d.Date);
        });

    var dateVar = 'Date';
    var sourceVar = 'Source';
    var modeVar = 'Mode';
    var headlineVar = 'Headline';
    var ratingVar = '538 Rating';
    var sampleVar = 'Sample Subpopulation';
    var moeVar = 'MoE';
    var sponsorVar = 'Sponsor';
    var IDVar = 'ID';


    var varVote = d3.keys(data[0])
        .filter(function (key) { return key !== dateVar;})
        .filter(function (key) { return key !== sourceVar;})
        .filter(function (key) { return key !== headlineVar;})
        .filter(function (key) { return key !== modeVar;})
        .filter(function (key) { return key !== ratingVar;})
        .filter(function (key) { return key !== sampleVar;})
        .filter(function (key) { return key !== moeVar;})
        .filter(function (key) { return key !== sponsorVar;})
        .filter(function (key) { return key !== IDVar;});

    //COLOR DOMAIN
    color.domain(varVote);

    //Initial Date
    var mindate = new Date("2017-01-23T00:00:00+00:00");


    //Axis Scale
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")

        .ticks(d3.time.month, 2)
        .tickFormat(d3.time.format("%b %Y"))
        .tickPadding([10]);


     var yGridlines = d3.svg.axis()
            .scale(y)
            .tickSize(-width,0,0)
            .tickFormat("")
            .tickValues([1])
            .orient("left");

    var yAxis = d3.svg.axis()
        .scale(y)
        .tickFormat(d3.format("%,"))
        .orient("left");

      function make_x_gridlines() {
        return d3.axisBottom(x)
            .ticks(5)
      }


    //New series Data
    var seriesData = varVote.map(function (name) {
      return {
            name: name,
            values: data.map(function (d) {
              return {name: name, Date: d[dateVar], value: +d[name], source: d[sourceVar], headline: d[headlineVar]};
            })};});

    // X e Y DOMAIN
    x.domain([mindate, d3.max(data, function(d) { return d.Date; })]);
    y.domain([d3.min(seriesData, function (c) {
        return d3.min(c.values, function (d) { return d.value - .1; });
      }),
      d3.max(seriesData, function (c) {
        return d3.max(c.values, function (d) { return d.value + .1; });
      })
    ]);

    //APPEND GRIDLINES



    //APPEND LINES
    var series = svg.selectAll(".series")
        .data(seriesData)
        .enter().append("g")
        .attr("class", "series");

        series.append("path")
            .attr("class", "line")
            .attr("d", function (d) { return line(d.values); })
            .style("stroke", function (d) { return color(d.name); })
            .style("stroke-width", "4px")
            .style("fill", "none");

        //APPEND CIRCLES
        series.selectAll(".point")
            .data(function (d) { return d.values; })
            .enter().append("circle")
            .attr("class", "point")
            .attr("cx", function (d) { return x(d.Date); })
            .attr("cy", function (d) { return y(d.value); })
            .attr("r", "4px")
            .style("fill", function (d) { return color(d.name) })
            .style("stroke", function (d) { return color(d.name); })
            .style("stroke-width", "1px")

            .on("mouseover", function (d) { showPopover.call(this, d)
            d3.select(this)
                .transition()
                .duration(500)
                .ease("elastic")
                .style("fill", function (d) { return color(d.name); })
                .style("stroke", function (d) { return color(d.name); })
                .style("stroke-width", "3px")
                .attr("r", "7px")
            })

            .on("mouseout",  function (d) { removePopovers();
             d3.select(this)
            .transition()
            .duration(500)
            .ease("elastic")
            .style("fill", function (d) { return color(d.name); })
            .style("stroke", function (d) { return color(d.name); })
             .style("stroke-width", "1px")
            .attr("r", "4px")
            })

        //APPEND AXIS
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")


    //POPOVER
    function removePopovers () {
      $('.popover').each(function() {
        $(this).remove();
      });}

    var t = d3.time.format("%d %b %Y");

    function showPopover (d) {
      $(this).popover({
        title: t(d.Date),
        placement: 'auto top',
        container: '#Container',
        trigger: 'manual',
        html : true,
        content: function() {
          return d.name.bold() + " " +
                 d3.round(((d.value)* 100), 1) + "%"+
                 "<br/>Source: " +
                 d.source.italics()+
                 "<br/>Headline: " +
                 d.headline.italics(); }});
      $(this).popover('show')
    }

});

//TABLE
d3.csv("/static/conrace.csv", function(error, data) {
		  if (error) throw error;

		  var sortAscending = true;
		  var table = d3.select('#page-wrap').append('table');
		  var titles = d3.keys(data[0]);
		  var headers = table.append('thead').append('tr')
		                   .selectAll('th')
		                   .data(titles).enter()
		                   .append('th')
                       .style("background-color","#AAB3E8")
                       .style("border-color","#AAB3E8")
		                   .text(function (d) {
			                    return d;
		                    })
		                   .on('click', function (d) {
		                	   headers.attr('class', 'header');

		                	   if (sortAscending) {
		                	     rows.sort(function(a, b) { return b[d] < a[d]; });
		                	     sortAscending = false;
		                	     this.className = 'aes';
		                	   } else {
		                		 rows.sort(function(a, b) { return b[d] > a[d]; });
		                		 sortAscending = true;
		                		 this.className = 'des';
		                	   }

		                   });

		  var rows = table.append('tbody').selectAll('tr')
		               .data(data).enter()
		               .append('tr');
		  rows.selectAll('td')
		    .data(function (d) {
		    	return titles.map(function (k) {
		    		return { 'value': d[k], 'name': k};
		    	});
		    }).enter()
		    .append('td')
		    .attr('data-th', function (d) {
		    	return d.name;
		    })
        .on("mouseover", function(d){
            d3.select(this)
                .style("background-color", "rgba(170,179,232,.7)");
        })
        .on("mouseout", function(d){
            d3.select(this)
                .style("background-color","#FFFFFF");
        })
		    .text(function (d) {
		    	return d.value;
		    });
	  });


//LAST DATA

var frontpageArea = d3.select("#svgCommittees")
    .append("svg")
    .attr("width",  width  + margin.left + margin.right)
    .attr("height", height/2 + margin.top  + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    d3.csv("/static/Data3.csv", function(error, data){

        var ultimidati = d3.values(data[0])
            .filter(function (d, i) {
                return i === 0 || i === 1;});

        var yesNo = ["Dem", "Rep"]
        var avg = ["Five Day Rolling  Average"]

        var frontpage = frontpageArea.selectAll(".frontpage")
            .data(ultimidati)
            .enter().append("g")
            .attr("class", "frontpage")
            .attr("transform", function (d, i) {
              return "translate(" + i * 250 + ", 45)";
            });


        frontpage.append("text")
                .data(yesNo)
                .attr("x", 450)
                .attr("y", 0)

                .text(function (d) {return d})
                .style("fill", function (d) { return color(d) })
                .style("font-size","36");

        frontpage.append("text")
                .data(avg)
                .attr("x", 0)
                .attr("y", 0)

                .text(function (d) {return d})
                .style("font-size","36");

        frontpage.append("text")
                .attr("x", 550)
                .attr("y", 0)

                .text(function (d) { return d3.round((d*100), 1)+"%"; })
                .style("fill", function (d) { return color(d) })
                .style("font-size","36");

})
