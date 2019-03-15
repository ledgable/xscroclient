
<form id="testform" class="controldata">

	<ul class="fields">
	
		<li>
			<input id="address" name="address" type="text" value="<py>print(vars.host, file=stdout)</py>"></input>
		</li>

		<li>
			<p>Enter the base64 document here - use <a class="link" target="__blank" href="https://www.base64encode.org">https://www.base64encode.org</a> to convert from json to base64</p>
		</li>
			
		<li>
			<textarea class="w400 h300" id="paymentinfo" name="paymentinfo"></textarea>
		</li>

	</ul>

</form>

<button onclick="myPayFunction('testform')">Process Payment</button>

<script>

	function myPayFunction(formid) {
	
		var address = document.getElementById("address").value;
		var paymentinfo = document.getElementById("paymentinfo").value;
		var url = "http://" + address + "/pay";
		
		$.ajax({
			   url: url,
			   type: "GET",
			   beforeSend: function(xhr) {
				   xhr.setRequestHeader('Payment', paymentinfo);
			   },
			   success: function() {
				   setTimeout(function() {
						  window.location.href = url;
						}, 333);
			   }
		});

	}

</script>
