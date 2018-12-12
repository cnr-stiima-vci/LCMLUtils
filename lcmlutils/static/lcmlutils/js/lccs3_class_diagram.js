var base_classes_dd = {
    "LC_Vegetation": { "color":"green"},
    "LC_AbioticSurface": { "color":"orange"},
    "LC_ArtificialSurface": { "color":"pink"},
    "LC_NaturalSurface": { "color": "brown"},
    "LC_WaterBodyAndAssociatedSurface": { "color": "cyan"}
};

function bind_lc_classes_to_color_map()
{
    var deferreds = [];
    var idx = 0;
    var base_classes_keys = Object.keys(base_classes_dd);
    var deferreds_count = base_classes_keys.length;
    for(idx=0;idx<deferreds_count;idx++)
    {
        var url = derel_url(base_classes_keys[idx]);
        deferreds.push(
            $.ajax(url, 
            {
                base_class_name: base_classes_keys[idx],
                color: base_classes_dd[base_classes_keys[idx]]["color"],
                success: function(data, textStats, jqXHR) {
                    console.log(data);
                    var idx = 0;
                    var total = data.objects.length;
                    for (idx=0;idx<total;idx++) {
                        var name = data.objects[idx];
                        if (!(name in lc_classes_color_map))
                            lc_classes_color_map[name] = {"lists":[]};
                        lc_classes_color_map[name]["lists"].push({
                            "base_class": this.base_class_name,
                            "count": total,
                            "color": this.color
                        });
                    }
                }
            })
        );
    };
    $.when.apply(null, deferreds).done(function() {
        console.log("bind_lc_classes_to_color_map completed!" );
        console.log(lc_classes_color_map);
        var beltypes = Object.keys(lc_classes_color_map);
        var count = beltypes.length;
        var idx = 0;
        for (idx = 0; idx < count; idx++)
        {
            var lists = lc_classes_color_map[beltypes[idx]]["lists"];
            var el = lists.reduce(function(prev, curr) {
                return prev.count < curr.count ? prev : curr;
            });
            lc_classes_color_map[beltypes[idx]].color = el.color;
        }
        console.log(lc_classes_color_map);
    });
};

function getColorForLandCoverClass(colormap, lcc_name)
{
    var default_color = "transparent";
    var color = default_color;
    var beltypes = Object.keys(colormap);
    if (beltypes.indexOf(lcc_name)!=-1)
        color = colormap[lcc_name].color;
    return color;
}

function derel_url(lc_base_name)
{
    return "/services/schema-derived-elements?name="+lc_base_name;
}


String.prototype.trunc =
     function( n, useWordBoundary ){
         if (this.length <= n) { return this; }
         var subString = this.substr(0, n-1);
         return (useWordBoundary 
            ? subString.substr(0, subString.lastIndexOf(' ')) 
            : subString) + "...";
      };

function get_nextSibling(n) {
    var y = n.nextSibling;
    while (y.nodeType!= 1) {
        y = y.nextSibling;
    }
    return y;
}

function get_firstChild(n) {
    var y = n.firstChild;
    while (y.nodeType != 1) {
        y = y.nextSibling;
    }
    return y;
}

function get_children(thisNode) {
    var nodes = [];
    var childrenCount = thisNode.childElementCount;
    if (childrenCount>0)
    {
        var n = get_firstChild(thisNode);
        if (childrenCount>0 && n !== undefined)
        {
            nodes.push(n);
            childrenCount -= 1;
        }
        while (childrenCount>0)
        {
            n = get_nextSibling(n);
            nodes.push(n);
            childrenCount -= 1;  
        };    
    }
    return nodes;
}

function get_node_classname(node) 
{
    var name = node.tagName;
    if ("uuid" in node.attributes)
        name = name + " [" + node.attributes["uuid"].value + "-" + node.attributes["id"].value + "]";
    return name;
}

function get_node_title(node, classDict) 
{
    var name = node.tagName;
    if ("name" in classDict["simple_attrs"])
        name = name + " (" + classDict["simple_attrs"]["name"] +")";
    return name;
}

function get_short_node_title(node, classDict) 
{
    var name = node.tagName;
    if ("name" in classDict["simple_attrs"])
        name = classDict["simple_attrs"]["name"];
    return name;
}

function extract_diagram(config, currentNode, parentNode, relationshipType, additional_params) 
{
    var classDict = {};
    if (!("_meta" in config))
        config["_meta"] = {"last_y": 0};
    if (additional_params===undefined)
    {
        additional_params = {};
        additional_params['level'] = 0;
    }
    classDict["attributes"] = [];
    classDict["simple_attrs"] = {};
    classDict["classname"] = get_node_classname(currentNode);
    classDict["x"] = 40 + additional_params["level"] * 60;
    classDict["y"] = 20 + config["_meta"]["last_y"] + 50;
    classDict["width"] = 400;
    //classDict["classcolor"] = "green";
    classDict["classcolor"] = getColorForLandCoverClass(classDict["classname"]);
    
    var childrenDict = {"terminal": [], "recurse": []};
    var nodes = get_children(currentNode);    
    nodes.forEach(function (el, idx, arr) {
        if (el.nodeType==1)
        {
            if (el.tagName!="elements")
                childrenDict["terminal"].push(el);
            else
            {
                var children = get_children(el);
                children.forEach(function(child, childIdx) {
                    childrenDict["recurse"].push(child);
                });
            }
        }
        else
            debugger;
    });
    childrenDict["terminal"].forEach(function (el, idx, arr) {
        var name = el.tagName,
            description = el.textContent,
            attributes = el.attributes;
        if (description.length>0)
        {
            if (name!="name" && name!="description")
                classDict["attributes"].push(name + ": " + description);
            classDict["simple_attrs"][name] = description;
        }
        else
        {
            if ("min" in attributes)
                classDict["attributes"].push(name + ": from " + el.attributes["min"].value + " to " + el.attributes["max"].value);
        }
    });
    classDict["title"] = get_node_title(currentNode, classDict); 
    config.classes.push(classDict);
    if (parentNode)
    {
        var marker_type = null;
        switch(relationshipType)
        {
            case "part-of": marker_type = "filledDiamond"; break;
            default:break;
        };
        config.connectors_meta.push({
            source: get_node_classname(parentNode),
            dest: get_node_classname(currentNode),
            connection_type: marker_type
        });
    }
    config["_meta"]["last_y"] += (classDict["attributes"].length*20+50);
    childrenDict["recurse"].forEach(function (el, idx, arr) {
        extract_diagram(config, el, currentNode, "part-of", {"level": additional_params["level"]+1});
    });
    //console.log(config);
    return config; 
}

function get_readable_name(str) {
  return str.replace("LC_", "").replace("_", " ").replace(/([a-zA-Z])(?=[A-Z])/g, '$1 ').toLowerCase()
}

function extract_nested_diagram(config, currentNode, parentNode, relationshipType, additional_params) 
{
    var classDict = config;
    /*
    if (!("_meta" in config))
        config["_meta"] = {"last_y": 0};
    */
    if (additional_params===undefined)
    {
        additional_params = {};
        additional_params['level'] = 0;
    }
    /*
    classDict["attributes"] = [];
    classDict["simple_attrs"] = {};
    classDict["classname"] = get_node_classname(currentNode);
    classDict["x"] = 40 + additional_params["level"] * 60;
    classDict["y"] = 20 + config["_meta"]["last_y"] + 50;
    classDict["width"] = 400;
    classDict["classcolor"] = "green";
    */
    classDict["id"] = get_node_classname(currentNode);
    classDict["basic_element"] = currentNode.tagName;
    if (currentNode.tagName==="LC_LandCoverElement")
        classDict["basic_element"] = currentNode.attributes["xsi:type"].value;
    classDict["layer"] = additional_params["level"].toString();
    classDict["current"] = false;
    classDict["simple_attrs"] = {};
    classDict["attributes"] = [];
    classDict["children"] = [];
    var childrenDict = {"terminal": [], "recurse": []};
    var nodes = get_children(currentNode);    
    nodes.forEach(function (el, idx, arr) {
        if (el.nodeType==1)
        {
            if (el.tagName!="elements")
                childrenDict["terminal"].push(el);
            else
            {
                var children = get_children(el);
                children.forEach(function(child, childIdx) {
                    childrenDict["recurse"].push(child);
                });
            }
        }
        else
            debugger;
    });
    childrenDict["terminal"].forEach(function (el, idx, arr) {
        var name = el.tagName,
            description = el.textContent,
            attributes = el.attributes;
        if (description.length>0)
        {
            if (name.indexOf("LC_")==0)
            {
                var children = get_children(el);
                var sublist = [];
                children.forEach(function (el, idx, arr) {
                    var name = el.tagName,
                        description = el.textContent,
                        attributes = el.attributes;
                    if (name=="elements")
                    {
                        var children = get_children(el);
                        children.forEach(function (el, idx, arr) {
                           var name = el.tagName,
                                description = el.textContent,
                                attributes = el.attributes; 
                            this.sublist.push(get_readable_name(name) + ": " + get_readable_name(attributes["xsi:type"].value || ""));
                        }, {"sublist": this.sublist});
                    }
                }, {"classDict":classDict,"sublist": sublist});
                classDict["attributes"].push(sublist.join(", "));
            }
            else
                if (name!="name" && name!="description")
                    classDict["attributes"].push(name + ": " + description.trunc(30));
            classDict["simple_attrs"][name] = description;
        }
        else
        {
            if ("min" in attributes)
                classDict["attributes"].push(name + ": from " + el.attributes["min"].value + " to " + el.attributes["max"].value);
        }
    });
    //classDict["title"] = get_node_title(currentNode, classDict); 
    classDict["name"] = get_short_node_title(currentNode, classDict);
    classDict["classcolor"] = getColorForLandCoverClass(additional_params["colormap"], classDict["basic_element"]);
    //config.classes.push(classDict);
    /*
    if (parentNode)
    {
        var marker_type = null;
        switch(relationshipType)
        {
            case "part-of": marker_type = "filledDiamond"; break;
            default:break;
        };
        config.connectors_meta.push({
            source: get_node_classname(parentNode),
            dest: get_node_classname(currentNode),
            connection_type: marker_type
        });
    }
    config["_meta"]["last_y"] += (classDict["attributes"].length*20+50);
    */
    childrenDict["recurse"].forEach(function (el, idx, arr) {
        child = {};
        additional_info = {
            "level": additional_params["level"]+1,
            "colormap": additional_params["colormap"]
        }
        var result = extract_nested_diagram(child, el, currentNode, "part-of", additional_info);
        //classDict["children"].push(child);
        classDict["children"].push(result);
    });
    return config; 
}

