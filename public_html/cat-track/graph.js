function appendVoteGraphTo ( counts ) {
    counts = counts.map( function ( d ) { return { count: d.count, time: new Date( d.time ), fmtTime: d.time }; } );
    var WIDTH = 600, HEIGHT = 250, MARGIN = { top: 15, bottom: 35, left: 0, right: 20 };
    var maxCount = d3.max( counts, function ( d ) { return d.count; } );
    MARGIN.left += 5 * Math.log10( maxCount );
    WIDTH += 5 * Math.log10( maxCount );

    var xScale = d3.time.scale()
        .range( [ MARGIN.left, WIDTH + MARGIN.left ] )
        .domain( d3.extent( counts, function ( d ) { return d.time; } ) );

    var yScale = d3.scale.linear()
        .range( [ HEIGHT, 0 ] )
        .domain( [ 0, maxCount ] );

    var xAxis = d3.svg.axis()
        .scale( xScale )
        .orient( "bottom" );
    var yAxis = d3.svg.axis()
        .scale( yScale )
        .orient( "left" );
    var line = d3.svg.line()
        .x( function ( d ) { return xScale( d.time ); } )
        .y( function ( d ) { return yScale( d.count ); } )
    var svg = d3.select( "#graph" ).append( "svg" )
        .attr( "width", WIDTH + MARGIN.left + MARGIN.right)
        .attr( "height", HEIGHT + MARGIN.top + MARGIN.bottom);

    // We rotate the tick labels so they don't overlap
    // Source: http://stackoverflow.com/a/16863559/1757964
    svg.append( "g" ).call( xAxis )
        .attr( "class", "x axis" )
        .attr( "transform", "translate(0," + HEIGHT + ")" )
        .selectAll( "text" )
        .style("text-anchor", "end")
        .attr( "transform", "rotate(-35)" );

    svg.append( "g" ).call( yAxis )
        .attr( "transform", "translate(" + MARGIN.left + ",0)" )
        .attr( "class", "y axis" );
    svg.append( "path" )
        .datum( counts )
        .attr( "d", line )
        .attr( "class", "line" )

    // Tooltip
    var tooltip = svg.append( "g" ).style( "display", "none" );

    tooltip.append( "circle" )
        .style( "fill", "none" )
        .style( "stroke", "blue" )
        .attr( "r", 4 );

    tooltip.append( "text" )
        .attr( "class", "time" )
        .attr( "dy", -27 )
        .style( "stroke", "black" )
        .style( "stroke-width", "0.1px" );

    tooltip.append( "text" )
        .attr( "class", "count" )
        .attr( "dy", -10 )
        .style( "stroke", "none" );

    // Element to capture mouse events
    var mouseEventSinkId = "vh-mouse-event-sink";
    svg.append( "rect" )
        .attr( "id", mouseEventSinkId )
        .attr( "width", WIDTH )
        .attr( "height", HEIGHT )
        .attr( "fill", "none" )
        .attr( "transform", "translate(" + MARGIN.left + ",0)" )
        .style( "pointer-events", "all" )
        .on( "mouseover", function () { tooltip.style( "display", null ); } )
        .on( "mouseout", function () { tooltip.style( "display", "none" ); } );

    document.getElementById( mouseEventSinkId ).addEventListener( "mousemove", function ( event ) {
        var eventTime = xScale.invert( event.clientX - document.getElementById( mouseEventSinkId ).getBoundingClientRect().left + MARGIN.left );
        var targetIndex = d3.bisector( function ( d ) { return d.time; } ).left( counts, eventTime, 1 );
        var leftDatapoint = counts[ targetIndex - 1 ];
        var rightDatapoint = counts[ targetIndex ];
        var datapoint = eventTime - leftDatapoint.time > rightDatapoint.time - eventTime ? rightDatapoint : leftDatapoint;
        var transform = "translate(" + xScale( datapoint.time ) + ", " + yScale( datapoint.count ) + ")";
        tooltip.select( "circle" ).attr( "transform", transform );
        tooltip.select( "text.time" )
            .attr( "transform", transform )
            .text( datapoint.fmtTime );
        tooltip.select( "text.count" )
                .attr( "transform", transform )
            .text( datapoint.count );
    } );

    // Download link
    var downloadText = "Time,Count\n";
    counts.forEach( function ( countObject ) {
        downloadText += countObject.fmtTime + "," + countObject.count + "\n";
    } );
    downloadText = downloadText.trim();
    document.getElementById( "graph" ).appendChild( createDownloadDiv( downloadText ) );

    // Align download links
    //$( "div.download" ).css( "width", $( "svg" ).first().outerWidth() );
}

function createDownloadDiv( data ) {
    var textArea = document.createElement( "textarea" );
    textArea.style.display = "none";
    textArea.setAttribute( "readonly", "readonly" );
    textArea.addEventListener( "click", function () {
        this.select();
        document.execCommand( "copy" );
    } );
    textArea.value = data;

    // Make link
    var div = document.createElement( "div" );
    div.className = "download";
    var p = document.createElement( "p" );
    var a = document.createElement( "a" );
    a.setAttribute( "href", "#" );
    a.textContent = "View";
    a.addEventListener( "click", function () {
        // If the text area isn't in the DOM yet, make it so
        if( !textArea.parentNode ) {
            this.parentNode.parentNode.appendChild( textArea );
        }

        textArea.style.display = textArea.style.display === "none" ? "" : "none";
        this.textContent = this.textContent === "View" ? "Hide" : "View";
        return false;
    } );
    p.appendChild( a );
    p.appendChild( document.createTextNode( " the data for this graph." ) );
    div.appendChild( p );
    return div;
}

appendVoteGraphTo( graph_data );
