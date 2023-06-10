{% args free_flash_mb, free_mem_kb, esp_tim, db %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>Esp Bookmark</title>
    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
  </head>
  
  <body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
      <div class="container">
	<a class="navbar-brand" href="#">Bookmark</a>
	<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
	</button>
	<div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item active">
              <a class="nav-link" href="/ntp">Ntptime</a>
            </li>
          </ul>
	</div>
      </div>
    </nav>    
    <!-- Page Content -->
    <div class="container">
      <div class="row">
	<div class="col-lg-12 text-center">
	  <h2>System Overview</h2>
	  <div class="table-responsive">
            <table class="table table-striped table-sm">
              <thead>
		<tr>
		  <th>Time</th>
		  <th>Free Flash(MB)</th>
		  <th>Free Memory(KB)</th>		  
		</tr>
              </thead>
              <tbody>
		<tr>
		  <td>{{esp_tim}}</td>
		  <td>{{free_flash_mb}}</td>
		  <td>{{free_mem_kb}}</td>
		</tr>
              </tbody>
            </table>
	  </div>

	  <h2>Bookmarks</h2>
	  <div class="table-responsive">
            <table class="table table-striped table-sm">
              <thead>
		<tr>
		  <th>Bookmark time</th>
		  <th>URL</th>
		</tr>
	      </thead>
	      <tbody>
		{% for key in db %}
		<tr>
		  <td><a href="/del?/key={{str(key, "utf-8")}}">{{ str(key, "utf-8") }}</a></td>
		  <td><a href="{{str(db[key], "utf-8")}}">{{ str(db[key], "utf-8") }}</a></td>
		</tr>
		{% endfor %}    
	      </tbody>
            </table>	    
         </div>

	  <h2>Bookmarks 2</h2>
	  <div class="table-responsive">
            <table class="table table-striped table-sm" id="bm_tables">
              <tr>
                  <th>Time</th>
              </tr>
            </table>	    
         </div>

	  
	</div>
      </div>
    </div>
    <!-- Bootstrap core JavaScript -->
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>  
    <!-- <script> -->
    <!-- var bm_LIST_API  = 'http://10.0.0.218:8081/list'; -->
    <!-- var bm_QUERY_API = 'http://10.0.0.218:8081/query?/key='; -->

    <!-- function drawRow(rowData) { -->
    <!-- 	var row = $("<tr />") -->
    <!-- 	$("#bm_tables").append(row); -->
    <!-- 	// $.ajax({ -->
    <!-- 	//     dataType: "json", -->
    <!-- 	//     url: bm_QUERY_API, -->
    <!-- 	//     data: rowData, -->
    <!-- 	//     success: function(url_data) { -->
    <!-- 	// 	console.log(url_data) -->
    <!-- 	//     } -->
    <!-- 	// });	 -->
    <!-- 	row.append($("<td>" + rowData + "</td>")); -->
    <!-- } -->

    <!-- $(document).ready(function(){ -->
    <!-- 	// $.get(bm_esp8266_LIST_API, function(data) { -->
    <!-- 	//     console.log(data); -->
    <!-- 	// }); -->
    <!-- 	$.ajax({ -->
    <!-- 	    dataType: "json", -->
    <!-- 	    url: bm_LIST_API, -->
    <!-- 	    success: function(data) { -->
    <!-- 		$.each(data, function( index, value ) { -->
    <!-- 		    drawRow(value) -->
    <!-- 		}); -->
    <!-- 	    } -->
    <!-- 	}); -->
    <!-- }); -->
    <!-- </script> -->
  </body>  
</html>

