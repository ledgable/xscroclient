
<section class="inner clear">
	
	<header>
		<h1>Chain / Minter</h1>
		<h2><span class="pagenav link" data-url="/chain/<py>print(vars.chainid, file=stdout)</py>"><py>print(vars.chainid, file=stdout)</py></span></h2>
	</header>

	<p>Create a new token</p>

	<ul class="actions collection clear">
		<li class="header"><span>Create A New Token</span></li>
		<li class="right">
			<span class="button green" data-event="{'action':'Xscro.Tokens','event':'mintNewToken','args':{'chainid':'<py>print(vars.chainid, file=stdout)</py>'}}">Create Token</span>
		</li>
	</ul>

	<form class="controldata" id="token__info">
		
		<section class="grid_r clear">
			
			<section>
				
				<ul class="fields">

					<li>
						<div><input name='ignore' readonly class="upper w400" data-req="true" type='text' data-default='chainid' value='<py>print(vars.chainid, file=stdout)</py>' data-validator='uuid'></input><span class="field req">id_chain</span></div>
					</li>

					<li>
						<div><input name='ignore' readonly class="upper w400" data-req="true" type='text' data-default='uid' value='0' data-validator='uuid'></input><span class="field req">uid</span></div>
					</li>

					<li>
						<div><input name='id_recipient' class="upper w400" data-req="true" type='text' data-default='id_recipient' value='id_recipient' data-validator='uuid'></input><span class="field req">id_recipient</span></div>
					</li>

					<li>
						<div><input name='id_transaction' class="upper w400" data-req="true" type='text' data-default='id_transaction' value='<py>print(self.uniqueId, file=stdout)</py>' data-validator='uuid'></input><span class="field req">id_transaction</span></div>
					</li>
					
					<li>
						<div><input name='id_trader' class="upper w400" data-req="true" type='text' data-default='id_trader' value='id_trader' data-validator='uuid'></input><span class="field req">id_trader</span></div>
					</li>

					<li>
						<div><input name='volume' class="upper w120 tright" data-req="true" type='text' data-default='volume' value='1.0' data-validator='decimal'></input><span class="field req">volume</span></div>
					
						<div><input name='price' class="upper w120 tright" data-req="true" type='text' data-default='price' value='0.0' data-validator='decimal'></input><span class="field req">price</span></div>
					</li>
						
					<li>
						<div><input name='additional' class="w400" data-req="true" type='text' data-default='comment' value='Token minted' data-validator='anychar'></input><span class="field req">comment</span></div>
					</li>
						
				</ul>
			
			</section>
			
			<aside class="notes">
				
				<p>Supply the details on the right to allocate a new token</p>
			
			</aside>
		
		</section>

	</form>

</section>
