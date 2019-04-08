
<form name="_xclick" action="http://127.0.0.1:8080/pay" method="post">
	<input type="hidden" name="chainid" value="">
	<input type="hidden" name="transactionid" value="1234567890">
	<input type="hidden" name="recipientwallet" value="Wallet ID">
	<input type="hidden" name="recipientdisplay" value="Some Company">
	<input type="hidden" name="currency" value="SQUID">
	<input type="hidden" name="description" value="Teddy Bear's Picnic">
	<input type="hidden" name="amount" value="1.11">
	<input type="hidden" name="callbacksuccess" value="http://127.0.0.1:8080/success">
	<input type="hidden" name="callbackfailure" value="http://127.0.0.1:8080/fail">
	<input type="hidden" name="callbackcancel" value="http://127.0.0.1:8080/cancel">
	<input type="image" width="120px" src="/images/paynow.png" border="0" name="submit" alt="Use XSCRO payments - Its free!!">
</form>
