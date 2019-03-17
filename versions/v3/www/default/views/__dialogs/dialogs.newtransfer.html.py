
<py>


</py>

<section>
	
	<section class="innerpart">
		
		<ul class="actions collection clear">
			<li class="header">
				<header>
					<h2>Transfer</h2>
					<h1>Create Transaction</h1>
				</header>
			</li>
			<li class="right">
				<span class="green button" data-event="{'action':'User.Tokens','event':'transferFunds','args':{}}">Create</span>
			</li>
		</ul>
		
		<form class="controldata" id="edit__newtransfer">
			
			<ul class="fields steps">
				
				<li class="selected">
					
					<ul class="fields">
						
						<li>Fill in the required information to transfer funds to another</li>
						
						<li>
							<div class=""><textarea name="note" type="text" data-allowreturn="1" class="w400 h150" data-req="true" data-default="Payment Note" data-validator="anychar">Payment Note</textarea><span class="field req">Payment Note</span></div>
						</li>
						
						<li>Note: You must acknowledge the transaction to execute</li>
					
					</ul>

					<section data-component="repeater" data-datasource="arr:newtransfers" data-cache="0" data-id="uid" data-mode="none">
						
						<ul class="list fields"></ul>
							
						<div class="template item" data-itemclass="wallet__line fullwidth">
							
							<condition eval="%walletid%">
								<result is="null">
									<div class=""><input data-event="{'action':'User.Tokens','event':'updateTransfer','args':{'uid':'%uid%'}}" name="walletid_%uid%" type="text" class="w250" data-req="true" data-default="Recipient Wallet Address" value="Recipient Wallet Address" data-validator="anychar"></input><span class="field req">Recipient Wallet Address</span></div>
								</result>
								<result is="default">
									<div class=""><input data-event="{'action':'User.Tokens','event':'updateTransfer','args':{'uid':'%uid%'}}" name="walletid_%uid%" type="text" class="w250" data-req="true" data-default="Recipient Wallet Address" value="%walletid%" data-validator="anychar"></input><span class="field req">Recipient Wallet Address</span></div>
								</result>
							</condition>
							
							<condition eval="%volume%">
								<result is="null">
									<div class=""><input data-event="{'action':'User.Tokens','event':'updateTransfer','args':{'uid':'%uid%'}}" name="volume_%uid%" class="tright w100" type="text" data-req="true" data-default="0.0" value="0.0" data-validator="decimal"></input><span class="field req">Volume</span></div>
								</result>
								<result is="default">
									<div class=""><input data-event="{'action':'User.Tokens','event':'updateTransfer','args':{'uid':'%uid%'}}" name="volume_%uid%" class="tright w100" type="text" data-req="true" data-default="0.0" value="%volume%" data-validator="decimal"></input><span class="field req">Volume</span></div>
								</result>
							</condition>

							<condition eval="%ppt%">
								<result is="null">
									<div class=""><input data-event="{'action':'User.Tokens','event':'updateTransfer','args':{'uid':'%uid%'}}" name="ppt_%uid%" class="tright w100" type="text" data-req="true" data-default="0.0" value="0.0" data-validator="decimal"></input><span class="field req">Price Per Token</span></div>
								</result>
								<result is="default">
									<div class=""><input data-event="{'action':'User.Tokens','event':'updateTransfer','args':{'uid':'%uid%'}}" name="ppt_%uid%" class="tright w100" type="text" data-req="true" data-default="0.0" value="%ppt%" data-validator="decimal"></input><span class="field req">Price Per Token</span></div>
								</result>
							</condition>

							<condition eval="%rowindex%">
								<result is="null"></result>
								<result is="default">
									<div class=""><span class="icon icon_cancel" data-event="{'action':'User.Tokens','event':'removeLine','args':{'uid':'%uid%'}}"></span><span class="field">&nbsp;</span></div>
								</result>									
							</condition>
								
						</div>
							
						<div class="template static_after">
							<span class="blue button" data-event="{'action':'User.Tokens','event':'addTransferLine','args':{}}">Add Transfer</span>
						</div>
							
					</section>
				
				</li>
			
			</ul>
		
		</form>

	</section>

</section>
