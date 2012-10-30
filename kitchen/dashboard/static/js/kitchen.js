function getDefaultDataTableConfig() {
    return {
        "bPaginate": false,
        "oLanguage": {
            "sSearch": "",
            "sInfo" : "Showing _TOTAL_ nodes",
            "sInfoEmpty": "No nodes found",
            "sInfoFiltered": " (filtering from _MAX_ total)",
            "sZeroRecords": "No nodes to display"
        },
        "oSearch": {
            "sSearch": getSearchText(),
        },
        "aoColumnDefs": [
            /* Expander */ { "bSortable": false, "aTargets": [0] },
            /* Fqdn */ { "bVisible": false, "aTargets": [1] }
        ],
        "sDom": '<"top"if>rt<"bottom"lp><"clear">'
    }
}


function getSearchText() {
    /*
     * Gets the predefined search text from the current page url
     */
    var searchText = "";
    if (window.location.hash !== "") {
      searchText = window.location.hash.substring(1);
    }
    return searchText;
}

function drawNodeListTable(searchText) {
    /*
     * Creates a list of nodes DataTable
     */
    oTable = $('#nodes').dataTable(getDefaultDataTableConfig());
    setSearchBox();
    setExtendedRows(oTable);
}

function drawNodeVirtTable(searchText) {
    /*
     * Creates the guests DataTable, grouped by hosts
     */
    // Extend the default DataTable config
    dataTableConfig = getDefaultDataTableConfig();
    dataTableConfig['aoColumnDefs'].push({ "bVisible": false, "aTargets": [2] });  // Grouper column
    dataTableConfig['aaSortingFixed'] = [[ 2, 'asc' ]];
    dataTableConfig['aaSorting'] = [[ 3, 'asc' ]];
    dataTableConfig['fnDrawCallback'] = function (oSettings) {
        if (oSettings.aiDisplay.length == 0) {
            return;
        }
        var nTrs = $('#nodes tbody tr');
        var iColspan = nTrs[0].getElementsByTagName('td').length;
        var sLastGroup = "";
        for (var i=0;i<nTrs.length;i++) {
            var iDisplayIndex = oSettings._iDisplayStart + i;
            var sGroup = oSettings.aoData[oSettings.aiDisplay[iDisplayIndex]]._aData[2];
            if (sGroup != sLastGroup) {
                var nGroup = document.createElement('tr');
                var nCell = document.createElement('td');
                nCell.colSpan = iColspan;
                nCell.id = "host_grouper";
                nCell.innerHTML = sGroup;
                nGroup.appendChild(nCell);
                nTrs[i].parentNode.insertBefore(nGroup, nTrs[i]);
                sLastGroup = sGroup;
            }
        }
    };
    oTable = $('#nodes').dataTable(dataTableConfig);
    setSearchBox();
    setExtendedRows(oTable);
}

function setSearchBox() {
    /*
    * Sets a predefined string inside the DataTables filter box
    */
    $('#nodes_filter input').attr("placeholder", "Search");
    $('#nodes_filter input:text').focus();
}

function setExtendedRows(oTable) {
    /*
     * Sets an event listener for opening and closing details
     */
    $('#nodes td.control').html('<i class="icon-chevron-right"></i>');
    $('#nodes td.control').live('click', function () {
        var nTr = $(this).parents('tr')[0];
        if (oTable.fnIsOpen(nTr)) {
            $(this).html('<i class="icon-chevron-right"></i>');
            oTable.fnClose(nTr);
        }
        else {
            $(this).html('<i class="icon-chevron-down"></i>');
            oTable.fnOpen(nTr, fnFormatNodeDetails(oTable, nTr), 'details');
        }
    } );
}

function fnFormatNodeDetails (oTable, nTr) {
    /* 
     * Establishes the content of the extended row.
     * The node key in DataTables will always be placed in the index 1 column.
     */
    var aData = oTable.fnGetData(nTr);
    var node = undefined;
    for(var i=0;i<nodes.length;i++) {
        if (nodes[i].name.substring(0, aData[1].length) == aData[1]) {
            node = nodes[i];
            break;
        }
    }
    var sOut = '<pre>';
    nodeJson = syntaxHighlight(JSON.stringify(node, undefined, 4));
    sOut += nodeJson;
    sOut += '</pre>';
    return sOut;
}

function syntaxHighlight(json) {
    /* 
    * Highlights JSON code
    */
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}
