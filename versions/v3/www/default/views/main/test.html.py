
<form id="testform">

	<input id="address" name="address" type="text" value="address"></input>
	<textarea id="paymentinfo" name="paymentinfo"></textarea>

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
