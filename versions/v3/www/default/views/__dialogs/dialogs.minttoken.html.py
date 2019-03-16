
<py>

chainid_ = vars.uidin

</py>

<section>
	
	<section class="innerpart">
		
		<ul class="actions collection clear">
			<li class="header">
				<header>
					<h2>Tokens</h2>
					<h1>Mint New Token</h1>
				</header>
			</li>
			<li class="right">
				<span class="green button" data-event="{'action':'Admin.Tokens','event':'mintToken','args':{'uid':'<py>print(chainid_, file=stdout)</py>'}}">Create</span>
			</li>
		</ul>
		
		<form class="controldata" id="edit__minttoken">
			
			<ul class="fields steps">
				
				<li class="selected">
					
					<ul class="fields">
						
						<li>Fill in the required information to create a new token</li>
					
						<li>
							<div class=""><input name="volume" class="tright w150" type="text" data-req="true" data-default="0.0" value="0.0" data-validator="decimal"></input><span class="field req">Volume</span></div>
							
							<div class=""><input name="ppt" class="tright w150" type="text" data-req="true" data-default="0.0" value="0.0" data-validator="decimal"></input><span class="field req">Price Per Token</span></div>
						</li>

						<li>
							<div class=""><input name="walletid" type="text" class="w400" data-req="true" data-default="Recipient Wallet Address" value="Recipient Wallet Address" data-validator="anychar"></input><span class="field req">Recipient Wallet Address</span></div>
						</li>
							
						<li>
							<div class=""><textarea name="note" type="text" data-allowreturn="1" class="w400 h150" data-req="true" data-default="Payment Note" data-validator="anychar">Payment Note</textarea><span class="field req">Payment Note</span></div>
						</li>
							
						<li>Note: The token is not automatically acknowledged after creation</li>

					</ul>
				
				</li>
		
			</ul>
				
		</form>
	
	</section>

</section>
