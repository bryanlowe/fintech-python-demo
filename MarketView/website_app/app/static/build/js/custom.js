// Initialize market view functionality
var datatable = null;
$(function(){
    $('#brand_share_btn').click(function(){
        brandShareView();
    });
    $('#sales_growth_btn').click(function(){
        salesGrowthView();
    });
    $('#industry_btn').click(function(){
        industryView();
    });
    $('#product_trends_btn').click(function(){
        productTrendsView();
    });
    $('#pricing_btn').click(function(){
        pricingView();
    });
});

function createDataTable(data){
    // create headers
    var thead = '<tr><th></th>';
    for(var i = 0, ii = data.thead.length; i < ii; i++){
        thead += '<th>' + data.thead[i] + '</th>';
    }
    thead += '</tr>';
    $('#datatable-thead').html(thead);

    // refresh or create table
    if(datatable){
        datatable = $('#datatable-responsive').DataTable({
            "data": data.tbody,
            "destroy": true
        });
    } else {
        datatable = $('#datatable-responsive').DataTable({
            "data": data.tbody,
        });
    }
}

function createLineChart(data){
    // create dataset for line chart
    datasets = [];
    for(var i = 0, ii = data.tbody.length; i < ii; i++){
        dataObj = {};
        dataObj.data = [];
        for(var j = 0, jj = data.tbody[i].length; j < jj; j++){
            if(j == 0){
                dataObj.label = data.tbody[i][j];
            } else {
                dataObj.data.push(data.tbody[i][j]);
            }
        }
        dataObj.fill = false;
        dataObj.pointBorderWidth = 1;
        dataObj.backgroundColor = CHART_COLORS[i].backgroundColor;
        dataObj.borderColor = CHART_COLORS[i].borderColor;
        dataObj.pointBorderColor = CHART_COLORS[i].pointBorderColor;
        dataObj.pointBackgroundColor = CHART_COLORS[i].pointBackgroundColor;
        dataObj.pointHoverBackgroundColor = CHART_COLORS[i].pointHoverBackgroundColor;
        dataObj.pointHoverBorderColor = CHART_COLORS[i].pointHoverBorderColor;
        datasets.push(dataObj);
    }
    // remove the blank header
    var ctx = $("#lineChart")[0];
    var lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.thead,
            datasets: datasets
        },
    });
    $('#lineChart').show();
}

// retrieve brand share view data
function brandShareView(request){
    request = request || {'data_type': 'revenue', 'time_frame': 'month'};
    $.post('/marketview/brandshare', request, function(data){
        createDataTable(data);
        createLineChart(data);
        $('#getting_started').hide();
        $('#market_view').show();
    });
}

// retrieve sales growth view data
function salesGrowthView(request){
    request = request || {'data_type': 'revenue', 'time_frame': 'month'};
    $.post('/marketview/salesgrowth', request, function(data){
        createDataTable(data);
        $('#getting_started').hide();
        $('#market_view').show();
    });
}

// retrieve industry view data
function industryView(request){
    request = request || {'data_type': 'revenue', 'time_frame': 'month'};
    $.post('/marketview/industry', request, function(data){
        createDataTable(data);
        $('#getting_started').hide();
        $('#market_view').show();
    });
}

// retrieve product trends view data
function productTrendsView(request){
    request = request || {'data_type': 'revenue', 'time_frame': 'month'};
    $.post('/marketview/producttrends', request, function(data){
        createDataTable(data);
        $('#getting_started').hide();
        $('#market_view').show();
    });
}

// retrieve pricing view data
function pricingView(request){
    request = request || {'data_type': 'revenue', 'time_frame': 'month'};
    $.post('/marketview/pricing', request, function(data){
        createDataTable(data);
        $('#getting_started').hide();
        $('#market_view').show();
    });
}