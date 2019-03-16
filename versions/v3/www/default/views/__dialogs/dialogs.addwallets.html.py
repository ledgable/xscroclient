
<py>

chainid_ = vars.uidin

</py>

<section>
	
	<section class="innerpart" data-component="droppable" data-event="{'action':'Admin.Wallets','event':'uploadFile','args':{}}">
		
		<ul class="actions collection clear">
			<li class="header">
				<header>
					<h2>Wallets</h2>
					<h1>Add Wallets to Chain</h1>
				</header>
			</li>
			<li class="right">
				<span class="green button" data-event="{'action':'Admin.Wallets','event':'createWallets','args':{'uid':'<py>print(chainid_, file=stdout)</py>'}}">Create</span>
			</li>
		</ul>
		
		<form class="controldata" id="edit__addwallets">
			
			<ul class="fields steps">
				
				<li class="selected">
					
					<ul class="fields">
						
						<li>Add a new wallet by providing wallet address and password - Note no passwords are transmitted to the server - only the calculated md5-hash (digest) is sent</li>
					
					</ul>
				
				</li>
			
			</ul>
		
			<section data-component="repeater" data-datasource="arr:newwallets" data-cache="0" data-id="uid" data-mode="none">
		
				<ul class="list fields"></ul>

				<div class="template item" data-itemclass="wallet__line fullwidth">
					
					<condition eval="%walletid%">
						<result is="null">
							<div class=""><input id="wallet_%uid%" name="wallet_%uid%" data-event="{'action':'Admin.Wallets','event':'updateWallet','args':{'uid':'%uid%'}}" type="text" class="w300" data-req="true" data-default="Wallet Address" value="Wallet Address" data-validator="username"></input><span class="field req">Wallet Address</span></div>
						</result>
						<result is="default">
							<div class=""><input id="wallet_%uid%" name="wallet_%uid%" data-event="{'action':'Admin.Wallets','event':'updateWallet','args':{'uid':'%uid%'}}" type="text" class="w300" data-req="true" data-default="Wallet Address" value="%walletid%" data-validator="username"></input><span class="field req">Wallet Address</span></div>
						</result>
					</condition>

					<condition eval="%password%">
						<result is="null">
							<div class=""><input id="password_%uid%" name="password_%uid%" data-event="{'action':'Admin.Wallets','event':'updateWallet','args':{'uid':'%uid%'}}" type="text" class="w200" data-req="true" data-default="Password" value="Password" data-validator="alltext"></input><span class="field req">Password</span></div>
						</result>
						<result is="default">
							<div class=""><input id="password_%uid%" name="password_%uid%" data-event="{'action':'Admin.Wallets','event':'updateWallet','args':{'uid':'%uid%'}}" type="text" class="w200" data-req="true" data-default="Password" value="%password%" data-validator="alltext"></input><span class="field req">Password</span></div>
						</result>
					</condition>
						
				</div>

				<div class="template static_after">
					<span class="blue button" data-event="{'action':'Admin.Wallets','event':'addWalletLine','args':{}}">Add Line</span>
				</div>

			</section>
				
		</form>
		
	</section>

</section>
