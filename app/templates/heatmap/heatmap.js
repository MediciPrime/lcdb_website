// function createCooccurance() {
//     d3.json("/static/foo.json?q=1280549782", function(miserables) {
//         cooccurance(miserables);
//     })
// }

function createCooccurance(data) {
    console.log(data);
    cooccurance(data);
}
    
function cooccurance(miserables) {

    console.log(miserables)
    
    // locate the margin position?
    var margin = {top: 100, right: 0, bottom: 10, left: 100},
        width = 800,
        height = 800;

    // 'rangeBands' is equivalent to 'range'
    var x = d3.scale.ordinal().rangeBands([0, width]),

        // 'jaccard' values can range from 0 to 4 w/ nothing out of bounds
        z = d3.scale.linear().domain([0, 4]).clamp(true),

        // variable for the color, uses 'category10' colors
        c = d3.scale.category10().domain(d3.range(10));

    // create svg box mainly based on the margin
    //margin-left and -top values have been hardcoded
    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("margin-left", 20 + "px")
	.style("margin-top", 20 + "px")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // create the matrix containing the values for the square
    var matrix = [],

        // create 'nodes' variable with all values from miserables.nodes
        nodes = miserables.nodes,

        // number of nodes i.e. characters
        n = nodes.length;
    
    // add attributes 'index' & 'count' for each of the nodes/characters
    nodes.forEach(function(node, i) {
        node.index = i;  // adds attribute index to nodes
        node.count = 0;  // adds attribute count to nodes

        // creates a single row containing 77 columns for the matrix
        // thus filling the empty matrix with 77 rows and 77 columns
        // all containing x, y and z.
        matrix[i] = d3.range(n).map(function(j) { return {x: j, y: i, z: 0};});
    });

    // once the matrix is created a z-value is set
    // Convert links to matrix; count character occurrences.
    miserables.links.forEach(function(link) {
        matrix[link.source][link.target].z += link.jaccard;
        matrix[link.target][link.source].z += link.jaccard;
        matrix[link.source][link.source].z += link.jaccard;
        matrix[link.target][link.target].z += link.jaccard;
        nodes[link.source].count += link.jaccard;
        nodes[link.target].count += link.jaccard;
    });

    //alert("matrix = "+  ) 
    
    // Precompute the orders.
    var orders = {
        name: d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].name, nodes[b].name); }),
        count: d3.range(n).sort(function(a, b) { return nodes[b].count - nodes[a].count; }),
        group: d3.range(n).sort(function(a, b) { return nodes[b].yoclust - nodes[a].yoclust; })
    };

    // The default sort order, by names A - Z
    x.domain(orders.name);

    // add 800px * 800px light gray rectangle
    svg.append("rect")
        .attr("class", "background")
        .attr("width", width)
        .attr("height", height);

    // translates row according to x(i)
    var row = svg.selectAll(".row")
        .data(matrix)
        .enter().append("g")
        .attr("class", "row")
        .attr("transform", function(d, i) {  return "translate(0," + x(i) + ")"; })
        .each(row);

    // append a horizonal line that has a length equal to the 'width'
    row.append("line")
        .attr("x2", width);

    // include the names along the rows
    row.append("text")
        .attr("x", -6)
        .attr("y", x.rangeBand() / 5)
        .attr("dy", ".32em")
        .attr("text-anchor", "end")
        .text(function(d, i) { return nodes[i].name; });

    // set variable 'column' to translate and rotate
    var column = svg.selectAll(".column")
        .data(matrix)
        .enter().append("g")
        .attr("class", "column")
        .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

    // create a line with length size equal to 'width'
    column.append("line")
        .attr("x1", -width);

    // add the rectangle names along the horizonal
    column.append("text")
        .attr("x", 6)
        .attr("y", x.rangeBand() / 5)
        .attr("dy", ".32em")
        .attr("text-anchor", "start")
        .text(function(d, i) { return nodes[i].name; });

    // guessing this adds the colors and rectangles
    function row(row) {
        var cell = d3.select(this).selectAll(".cell")
            .data(row.filter(function(d) { return d.z; }))
            .enter().append("rect")
            .attr("class", "cell")
            .attr("x", function(d) { return x(d.x); })
            .attr("width", x.rangeBand())
            .attr("height", x.rangeBand())
            .style("fill-opacity", function(d) { return z(d.z); })
            .style("fill", function(d) { return nodes[d.x].yoclust == nodes[d.y].yoclust ? c(nodes[d.x].yoclust) : null; })
            .on("mouseover", mouseover)
            .on("mouseout", mouseout);
    }

    // turns labels red when mouse goes over rectangle
    function mouseover(p) {
        d3.selectAll(".row text").classed("active", function(d, i) { return i == p.y; });
        d3.selectAll(".column text").classed("active", function(d, i) { return i == p.x; });
    }

    // turns labels black when mouse is no longer over rectangle
    function mouseout() {
        d3.selectAll("text").classed("active", false);
    }

    // implements reordering of rectangles
    d3.select("#order").on("change", function() {
        clearTimeout(timeout);
        order(this.value);
    });

    // describes how the ordering will take place
    function order(value) {
        x.domain(orders[value]);

        var t = svg.transition().duration(2500);

        t.selectAll(".row")
            .delay(function(d, i) { return x(i) * 4; })
            .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
            .selectAll(".cell")
            .delay(function(d) { return x(d.x) * 4; })
            .attr("x", function(d) { return x(d.x); });

        t.selectAll(".column")
            .delay(function(d, i) { return x(i) * 4; })
            .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });
    }

    var timeout = setTimeout(function() {
        order("group");
        d3.select("#order").property("selectedIndex", 2).node().focus();
    }, 5000);
}
