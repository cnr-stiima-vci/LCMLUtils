d3.classGraph = (function () {
    var customNodes = new Array(),
    tmpNodes,
    label_w = 70,
    branch_w = 40,
    layer_wider_label = new Array(),
    classgraph;

    function initclassgraph(div_id, config_dd) {
        var data = config_dd;
        customNodes = [];
        layer_wider_label = [];
        tmpNodes = d3.layout.tree().size([500, 400]).nodes(data);
        // Create a svg canvas
        classgraph = d3.select("#"+div_id).append("svg:svg")
            .attr("id","svg-chart")
            .attr("width", 800)
            .attr("height", 500)
            .append("svg:g")
            .attr("transform", "translate(40, 30)"); // shift everything to the right
        var fakeTxtBox = classgraph.append("svg:text")
            .attr("id", "fakeTXT")
            .attr("text-anchor", "right")
            .text(data.name);
        layer_wider_label[0] = fakeTxtBox.node().getComputedTextLength()+10;
        classgraph.select("#fakeTXT").remove();
        data.y = getNodeY(data.id);
        data.x = 0;
        data.depth = parseInt(data.layer);
        customNodes.push(data);
        prepareNodes(data.children);
        //align nodes.
        updateNodesXOffset();
        drawChart();
    }

    function updateNodesXOffset(){
        var x_offsets = new Array();
        x_offsets[0] = 0;
        customNodes.forEach(function(node) {
            node.x = 0;
            if (node.layer > 0) {
                node.x = x_offsets[node.layer - 1] + layer_wider_label[node.layer - 1] + branch_w;
                x_offsets[node.layer] = node.x;
            }
        });
    };

    function getNodeY(id) {
        var ret = 0;
        tmpNodes.some(function(node) {
            if (node.id === id) {
                //return x:d3.tree has a vertical layout by default.
                ret = node.x;
                return;
            }
        })
        return ret;
    }

    function prepareNodes(nodes) {
        nodes.forEach(function(node) {
            prepareNode(node);
            if (node.children) {
                prepareNodes(node.children);
            }
        });
    }

    function prepareNode(node) {
        node.y = getNodeY(node.id);
        //fake element to calculate labels area width.
        var fakeTxtBox = classgraph.append("svg:text")
            .attr("id", "fakeTXT")
            .attr("text-anchor", "right")
            .attr("font-weight", "bold")
            .text(node.name);
        var text_lengths = new Array();
        text_lengths.push(fakeTxtBox.node().getComputedTextLength()+10);
        var attributes = node.attributes || new Array();
        var attribute = null;
        if (attributes.length>0)
        {
            var attr_idx = 0;
            for (attr_idx = 0; attr_idx < attributes.length; attr_idx++)
            {
                var fakeline = classgraph.append("svg:text")
                    .attr("id", "fakeattr"+attr_idx)
                    .attr("text-anchor", "right")
                    .text(node.attributes[attr_idx]);
                text_lengths.push(fakeline.node().getComputedTextLength());
                classgraph.select("#fakeattr"+attr_idx).remove();
            }
        }
        //var this_label_w = fakeTxtBox.node().getComputedTextLength();
        var this_label_w = Math.max.apply(null, text_lengths);
        classgraph.select("#fakeTXT").remove();
        if (layer_wider_label[node.layer] == null) {
            layer_wider_label[node.layer] = this_label_w;
        } else {
            if (this_label_w > layer_wider_label[node.layer]) {
                layer_wider_label[node.layer] = this_label_w;
            }
        }
    //                node.x = nodex;
        //x will be set
        node.depth = parseInt(node.layer);
        customNodes.push(node);
    }


    function customSpline(d) {
        var p = new Array();
        p[0] = d.source.x + "," + d.source.y;
        p[3] = (d.target.x+5) + "," + d.target.y;
        var m = (d.source.x + d.target.x) / 2
        p[1] = m + "," + d.source.y;
        p[2] = m + "," + d.target.y;
        //This is to change the points where the spline is anchored
        //from [source.right,target.left] to [source.top,target.bottom]
        //                var m = (d.source.y + d.target.y)/2
        //                p[1] = d.source.x + "," + m;
        //                p[2] = d.target.x + "," + m;
        return "M" + p[0] + "C" + p[1] + " " + p[2] + " " + p[3];
    }

    function getRandomColor() {
      var letters = '0123456789ABCDEF';
      var color = '#';
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }

    function drawChart() {
        customNodes.forEach(function(node) {
            var dxoff = 6;
            var nodeSVG = classgraph.append("svg:g")
            .attr("transform", "translate(" + node.x + "," + node.y + ")")
            if (node.depth > 0) {
                /*
                nodeSVG.append("svg:circle")
                .attr("stroke", node.children ? "#3191c1" : "#269926")
                .attr("fill", "#fff")
                .attr("r", 3);
                */
            }
            var attributes = node.attributes || new Array();
            var offy = (attributes.length*20)/2;
            /* compute bounding box width */

            /* draw rectangles */

            /* draw text */
            var txtBox = nodeSVG.append("svg:text")
                .attr("dx", dxoff)
                .attr("dy", 4-offy)
                .attr("fill", "black")
                .attr("font-weight", "bold")
                .text(node.name);
            var text_lengths = new Array();
            text_lengths.push(txtBox.node().getComputedTextLength()+10);
            var attr_idx = 0;
            for (attr_idx = 0; attr_idx < attributes.length; attr_idx++)
            {
                var txtBoxSecond = nodeSVG.append("svg:text")
                    .attr("dx", dxoff)
                    .attr("dy", 20+(attr_idx)*20-offy)
                    .attr("fill", "black")
                    .text(attributes[attr_idx]);
                text_lengths.push(txtBoxSecond.node().getComputedTextLength());
            }
            //var txtW = txtBox.node().getComputedTextLength();
            var txtW = Math.max.apply(null, text_lengths);
            //var offy = 0;
            //debugger;
            var RectBox = nodeSVG.insert("svg:rect",":first-child")
                .attr("width", txtW + dxoff)
                .attr("height", 20) //+
                .attr("y", -12-offy)
                .attr("x", "5")
                .attr("fill", node.classcolor || "transparent") // getColorForLandCoverClass(node["basic_element"])
                .attr("stroke", "black")
                .attr("stroke-width", 1);
            var RectBox2 = nodeSVG.insert("svg:rect",":first-child")
                .attr("width", txtW + dxoff)
                .attr("height", attributes.length*20)
                .attr("y", -12+20-offy)
                .attr("x", "5")
                .attr("fill", node.classcolor || "transparent") // getColorForLandCoverClass(node["basic_element"])
                .attr("stroke", "black")
                .attr("stroke-width", 1);
            if (node.current) {
                nodeSVG.insert("rect", "text")
                    .attr("fill", node.children ? "#3191c1" : "#269926")
                    .attr("width", txtW + dxoff)
                    .attr("height", "20")
                    .attr("y", "-12")
                    .attr("x", "5")
                    .attr("rx", 4)
                    .attr("ry", 4)
            }
            if (node.children) {
                node.x = node.x + txtW + 24;
                //prepare links;
                var links = new Array();
                node.children.forEach(function(child) {
                    var st = new Object();
                    st.source = node;
                    //                        st.parent = node;
                    st.target = child;
                    st.target.x+=2;
                    st.warning = child.warning;
                    links.push(st);
                });

                //draw links (under nodes)
                classgraph.selectAll("pathlink")
                    .data(links)
                    .enter().insert("svg:path", "g")
                    .attr("class", function(d) {
                        return d.warning === "true" ? "link warning" : "classgraphlink"
                    })
                    .attr("d", customSpline);
                //draw a node at the end of the link
                nodeSVG.append("svg:circle")
                    .attr("stroke", "#3191c1")
                    .attr("fill", "#fff")
                    .attr("r", 5.5)
                    .attr("transform", "translate(" + (txtW + 17) + ",0)");        
            }
        });
        var bbox = classgraph.node().getBBox();
        d3.select("#svg-chart")
            .style("width",bbox.width+bbox.x+50)
            .style("height",bbox.height+bbox.y+100);
    }
    return {
        initialize: initclassgraph
    };
})();