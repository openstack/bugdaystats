$(function() {
    var options = {
        xaxis: { mode: "time", timeformat: "%0H:%0M" },
        yaxis: { min: '0' },
        series: { stack: true, lines: { show: true, fill: true }},
        legend: { position: "nw" }
    };

    var new_stats = new Array();
    var open_stats = new Array();
    var inprogress_stats = new Array();
    var incomplete_stats = new Array();

    $.getJSON(datafile, function(JSONdata) {
        records  = JSONdata['records']
        for (var i = 0; i < records.length; i++) {
            xval = records[i].date * 1000
            new_stats.push([xval, records[i].new]);
            open_stats.push([xval, records[i].confirmed + records[i].triaged]);
            inprogress_stats.push([xval, records[i].inprogress]);
            incomplete_stats.push([xval, records[i].incomplete]);
        };
        var plot = $.plot(
            $(range),
            [
                { 'label': 'New', 'color': 2, data: new_stats },
                { 'label': 'Incomplete', 'color': 1, data: incomplete_stats },
                { 'label': 'In progress', 'color': 0, data: inprogress_stats },
                { 'label': 'Total open', 'color': 3, data: open_stats }
            ],
            options);
    });
});
