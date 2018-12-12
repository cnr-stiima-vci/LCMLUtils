function importSelectedClasses(buffered_files) 
{
	var enabled_checkboxes = $('#loaded-classes-list tbody input[type="checkbox"]').filter(function() {
    return !this.disabled && this.checked;
    
    });
    for (var idx = 0; idx < enabled_checkboxes.length; idx++) {
    	debugger;
    	var ctr = $(enabled_checkboxes[idx].parentNode.parentNode)[0];
    	var file_idx = 0;//parseInt(ctr.getAttribute('file-idx'));
    	var uuid = ctr.getAttribute('uuid');
    	var map_code = ctr.childNodes[2].textContent;
    	var text = text = buffered_files[file_idx];
    	var xmlDocument = $.parseXML(text);
		var thel = $(xmlDocument).find('LC_LandCoverClass').filter(function() {
			return this.getAttribute('uuid')==uuid;
    	});
    	var element = thel[0];
    	var sXML = new XMLSerializer().serializeToString(element);
    	var name = thel.find('name')[0].innerHTML;
    	var description = thel.find('description')[0].innerHTML;
    	var map_code = thel.find('map_code')[0].innerHTML;
    	ClassAdd(map_code, name, description, sXML);
    	$('#LCML-query').hide();
        $('#querybuilder-save-btn').hide();
	}
}

function clearImportTable() {
	var tbody = $('#loaded-classes-list tbody');
	tbody.empty();
}

function updateImportTable(text)
{
	var parser = new DOMParser();
	var xmlDoc = parser.parseFromString(text,"text/xml");
	var lc_classes = xmlDoc.getElementsByTagName('LC_LandCoverClass');
	var tbody = $('#loaded-classes-list tbody');
	for (var idx=0; idx<lc_classes.length; idx++)
	{
		if (lc_classes[idx].querySelectorAll('name').length>0)
		{
			var name = lc_classes[idx].querySelectorAll('name')[0].textContent;
			var map_code = lc_classes[idx].querySelectorAll('map_code')[0].textContent;
			var uuid = lc_classes[idx].getAttribute('uuid');
		    tbody.append($('<tr>').attr('uuid',uuid).attr('file-idx',idx.toString())
	            .append($('<td>').addClass('col-md-1')
	                .append($('<input>').attr('type','checkbox').addClass('checkthis'))
	            )
	            .append($('<td>').addClass('col-md-2').text(map_code))
	            .append($('<td>').addClass('col-md-5').text(name))
	        );
		}
	}
}


function importLCCS3ClassesFromFiles(buffered_files)
{
	console.log('importLCCS3ClassesFromFiles');
	var files = this.inputLCCS3File.files;
	for (var idx=0;idx<files.length;idx++)
	{
		var currFile = files[idx];
		var reader = new FileReader();
		reader.onload = (function(theFile, buffered_files){
		    var fileName = theFile.name;
		    return function(e){
		        console.log(fileName);
		        var text = e.target.result;
		        console.log(text);
		        buffered_files.push(text);
		        clearImportTable();
		        updateImportTable(text);
		    };
		})(currFile, buffered_files);   
		var text = reader.readAsText(currFile);
	}
}
