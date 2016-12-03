function searchTrailers()
{   
    var searchType = document.getElementById('search_type').selectedIndex;
    var searchAmountSelect = document.getElementById('trailer_amount');
    var searchAmount = searchAmountSelect[searchAmountSelect.selectedIndex].value;
    var searchArea = document.getElementById('search_input');
    var searchText = $.trim(searchArea.value);
    var url = ( searchType == '0' ? "/api/search/title" : "/api/search/imdbId");
    
    var trailers_are = document.getElementById('trailers_area');
    trailers_are.innerHTML = "";

    $('#loading').show();

    if (searchText.length === 0) {
        return false;
    }
    $.ajax({
        'url' : url,
        'type' : 'GET',
        'dataType': 'json',
        'data' : {
            'query' : searchText,
            'count' : searchAmount
        },
        'success' : function (data) {
            $('#loading').hide();
            
            trailers_are.innerHTML += "<h2 style='display:inline-block;'>" + data['title'] + "</h2> \
                <a style='padding-left:20px;' src='http://www.imdb.com/title/" 
                + data['imdbid'] + "'>View in IMDb<a/><hr/>";
            console.log(data);
            for (var trailer in data['trailers'])
            {
                trailers_are.innerHTML += data['trailers'][trailer]['embed'];
            }
            var top10DateRangeSelect = document.getElementById('top10_daterange');
            var top10DateRangeSelectValue = top10DateRangeSelect[top10DateRangeSelect.selectedIndex].value;
            getTop10(top10DateRangeSelectValue);
        },
        error: function (errormessage) {
            $('#loading').hide();
            document.getElementById('trailers_area').innerHTML = "<h1>No movies found!</h1>";
        }
    });
}
function getTop10(days)
{
    $.ajax({
        'url' : '/api/search/top',
        'type' : 'GET',
        'dataType': 'json',
        'data' : {
            'query' : days
        },
        'success' : function (data) {
            var top10_area = document.getElementById('top10_searches');
            top10_area.innerHTML = "";
            data = $.parseJSON(data);
            var i = 1;
            for (var movie in data)
            {
                top10_area.innerHTML += "<li class='list-group-item'>" + i + ". " + data[movie]['title'] + ", Searched " + data[movie]['searches'] + " times.</li>";
                ++i;
            }
        }
    });
}

function getDays(index)
{
    var top10DateRangeSelect = document.getElementById('top10_daterange');
    return top10DateRangeSelectValue = top10DateRangeSelect[index].value;
}

function validFields()
{   
    amount = $('#trailer_amount').val();
    if (amount == 0) {
        console.log("Meni");
    } else {
        $('#search_input').removeAttr("disabled");
        $('#search_button').removeAttr("disabled");
    }
}
