/**
 * Created by kripanshubhargava on 4/9/18.
 */

$(document).ready(function() {
    console.log("Oh yrasd")
    var obj = JSON.parse(input_json);
    console.log(" json ", obj)
    var all_obj = obj[1];

    get_variables(obj)
    function get_variables(input) {
            var variable_list=[];

             // console.log('all obj ', all_obj.variables)
             for(var i in all_obj.variables)
            {
               variable_list.push(i)
            }

                // console.log('variable list', variable_list)
                d3.select("#variables").selectAll("p")
                    .data(variable_list)
                    .enter()
                    .append("p")
                    .attr("classed","true")
                .text(function (d) {
                    return d;
                }).on('mouseover',disply_information)
                    .on('mouseout',clean_div)
                    .style('margin-top','5px')
                    .style('background-color','#f0f8ff').attr("data-container", "#variables")

                ;

        }
// disply_information('cylinders')
     function disply_information(d,i){
        var varname = d;

        console.log('varname',d)
        var char_list = []
            console.log('all object ',all_obj)
            for(var i in all_obj['variables'][varname]){
                char_list.push({ name:i, value:all_obj['variables'][varname][i]})
            }
            // console.log(char_list)
          d3.select("#desc").selectAll("p")
                    .data(char_list)
                    .enter()
                    .append("p")
                    .attr("classed","true")
                     // perhapse ensure this id is unique by adding '_' to the front?
                .text(function (d,i) {
                    var row =d.name + ' : '+ d.value;
                    return row;
                })
                    .style('margin-top','5px')
                    .style('background-color','#f0f8ff').attr("data-container", "#variables")
                // .attr("onmouseover", console.log("oh yeah"))
                // .attr("onmouseout", console.log("oh out"))
                ;
         if(all_obj['variables'][varname]['plottype']=='bar'){
             
         }
         else{
            density_cross(all_obj['variables'][varname])}

     }

     function clean_div() {

document.getElementById("desc").innerHTML = "";
     }


      function density_cross(density_env) {
         console.log("density env ",density_env)
        // setup the x_cord according to the size given by user
        var yVals = density_env.ploty;
        var xVals = density_env.plotx;

        // an array of objects
        var data2 = [];
        for (var i = 0; i < density_env.plotx.length; i++) {
            data2.push({x: density_env.plotx[i], y: density_env.ploty[i]});
        }
        data2.forEach(function (d) {
            d.x = +d.x;
            d.y = +d.y;
        });

        var min_x = d3.min(data2, function (d, i) {
            return data2[i].x;
        });
        var max_x = d3.max(data2, function (d, i) {
            return data2[i].x;
        });
        var avg_x = (max_x - min_x) / 10;
        var min_y = d3.min(data2, function (d, i) {
            return data2[i].y;
        });
        var max_y = d3.max(data2, function (d, i) {
            return data2[i].y;
        });
        var avg_y = (max_y - min_y) / 10;
        var x = d3.scale.linear()
            .domain([d3.min(xVals), d3.max(xVals)])
            .range([0, width_cross]);
        var invx = d3.scale.linear()
            .range([d3.min(data2.map(function (d) {
                return d.x;
            })), d3.max(data2.map(function (d) {
                return d.x;
            }))])
            .domain([0, width_cross]);
        var y = d3.scale.linear()
            .domain([d3.min(data2.map(function (d) {
                return d.y;
            })), d3.max(data2.map(function (d) {
                return d.y;
            }))])
            .range([height_cross, 0]);
        var xAxis = d3.svg.axis()
            .scale(x)
            .ticks(5)
            .orient("bottom");
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");
        var area = d3.svg.area()
            .interpolate("monotone")
            .x(function (d) {
                return x(d.x);
            })
            .y0(height_cross - avg_y)
            .y1(function (d) {
                return y(d.y);
            });
        var line = d3.svg.line()
            .x(function (d) {
                return x(d.x);
            })
            .y(function (d) {
                return y(d.y);
            })
            .interpolate("monotone");

        var plotsvg = d3.select("#plots")
            .append("svg")
            .attr("id", "plotsvg_id")
            .style("width", width_cross + margin_cross.left + margin_cross.right) //setting height to the height of #main.left
            .style("height", height_cross + margin_cross.top + margin_cross.bottom)
            .style("margin-left","20px")
            .append("g")
            .attr("transform", "translate(0," + margin_cross.top + ")");
        plotsvg.append("path")
            .attr("id", "path1")
            .datum(data2)
            .attr("class", "area")
            .attr("d", area);
        plotsvg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + (height_cross  ) + ")")
            .call(xAxis);
        plotsvg.append("text")
            .attr("x", (width_cross / 2))
            .attr("y", (margin_cross.top + padding_cross -10))
            .attr("text-anchor", "middle")
            .text(density_env.name)
            .style("text-indent","20px")
            .style("font-size","12px")
            .style("font-weight","bold");


    }

    // this is the function to add the bar plot if any
    // function bar_cross(bar_env) {
    //     var barPadding = .015;  // Space between bars
    //     var topScale = 1.2;      // Multiplicative factor to assign space at top within graph - currently removed from implementation
    //     var plotXaxis = true;
    //
    //     // Data
    //     var keys = Object.keys(bar_env.plotvalues);
    //     var yVals = new Array;
    //     var ciUpperVals = new Array;
    //     var ciLowerVals = new Array;
    //     var ciSize;
    //
    //     var xVals = new Array;
    //     var yValKey = new Array;
    //
    //     if (bar_env.nature === "nominal") {
    //         var xi = 0;
    //         for (var i = 0; i < keys.length; i++) {
    //             if (bar_env.plotvalues[keys[i]] == 0) {
    //                 continue;
    //             }
    //             yVals[xi] = bar_env.plotvalues[keys[i]];
    //             xVals[xi] = xi;
    //             if ($private) {
    //                 if (bar_env.plotvaluesCI) {
    //                     ciLowerVals[xi] = bar_env.plotValuesCI.lowerBound[keys[i]];
    //                     ciUpperVals[xi] = bar_env.plotValuesCI.upperBound[keys[i]];
    //                 }
    //                 ciSize = ciUpperVals[xi] - ciLowerVals[xi];
    //             }
    //             yValKey.push({y: yVals[xi], x: keys[i]});
    //             xi = xi + 1;
    //         }
    //         yValKey.sort((a, b) => b.y - a.y); // array of objects, each object has y, the same as yVals, and x, the category
    //         yVals.sort((a, b) => b - a); // array of y values, the height of the bars
    //         ciUpperVals.sort((a, b) => b.y - a.y); // ?
    //         ciLowerVals.sort((a, b) => b.y - a.y); // ?
    //     } else {
    //         for (var i = 0; i < keys.length; i++) {
    //             yVals[i] = bar_env.plotvalues[keys[i]];
    //             xVals[i] = Number(keys[i]);
    //             if ($private) {
    //                 if (bar_env.plotvaluesCI) {
    //                     ciLowerVals[i] = bar_env.plotvaluesCI.lowerBound[keys[i]];
    //                     ciUpperVals[i] = bar_env.plotvaluesCI.upperBound[keys[i]];
    //                 }
    //                 ciSize = ciUpperVals[i] - ciLowerVals[i];
    //             }
    //         }
    //     }
    //
    //     if ((yVals.length > 15 & bar_env.numchar === "numeric") | (yVals.length > 5 & bar_env.numchar === "character")) {
    //         plotXaxis = false;
    //     }
    //     var minY=d3.min(yVals);
    //     var  maxY = d3.max(yVals); // in the future, set maxY to the value of the maximum confidence limit
    //     var  minX = d3.min(xVals);
    //     var  maxX = d3.max(xVals);
    //     var   x_1 = d3.scale.linear()
    //         .domain([minX - 0.5, maxX + 0.5])
    //         .range([0, width_cross]);
    //
    //     var invx = d3.scale.linear()
    //         .range([minX - 0.5, maxX + 0.5])
    //         .domain([0, width_cross]);
    //
    //     var  y_1 = d3.scale.linear()
    //     // .domain([0, maxY])
    //         .domain([0, maxY])
    //         .range([0, height_cross]);
    //
    //     var xAxis = d3.svg.axis()
    //         .scale(x_1)
    //         .ticks(yVals.length)
    //         .orient("bottom");
    //
    //     var yAxis = d3.svg.axis()
    //         .scale(y_1)
    //         .orient("left");
    //
    //     var plotsvg1 = d3.select(plot_b)
    //         .append("svg")
    //         .attr("id","plotsvg1_id")
    //         .style("width", width_cross + margin_cross.left + margin_cross.right) //setting height to the height of #main.left
    //         .style("height", height_cross + margin_cross.top + margin_cross.bottom)
    //         .style("margin-left","20px")
    //         .append("g")
    //         .attr("transform", "translate(0," + margin_cross.top + ")");
    //
    //     var rectWidth = x_1(minX + 0.5 - 2 * barPadding); //the "width" is the coordinate of the end of the first bar
    //     plotsvg1.selectAll("rect")
    //         .data(yVals)
    //         .enter()
    //         .append("rect")
    //         .attr("id","path2")
    //         .attr("x", function (d, i) {
    //             return x_1(xVals[i] - 0.5 + barPadding);
    //         })
    //         .attr("y", function (d) {
    //             return y_1(maxY - d);
    //         })
    //         .attr("width", rectWidth)
    //         .attr("height", function (d) {
    //             return y_1(d);
    //         })
    //         .attr("fill", "#fa8072");
    //
    //     if (plotXaxis) {
    //         plotsvg1.append("g")
    //             .attr("class", "x axis")
    //             .attr("transform", "translate(0," + height_cross + ")")
    //             .call(xAxis);
    //     }
    //
    //     plotsvg1.append("text")
    //         .attr("x", (width_cross / 2))
    //         .attr("y", margin_cross.top + padding_cross-10)
    //         .attr("text-anchor", "middle")
    //         .text(bar_env.name)
    //         .style("text-indent","20px")
    //         .style("font-size","12px")
    //         .style("font-weight","bold");
    //
    // }

 });