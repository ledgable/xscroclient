
<py>

balance_ = 0.0
token_ = vars.token
if token_ != None:
	balance_ = token_.balance

</py>

<section class="trading__view">
	<canvas data-component="statplot" data-datasource="/api/<py>print(vars.chainid, file=stdout)</py>/data/0"></canvas>
</section>

<section class="inner clear">
	
	<section class="grid_l clear nomargin">
		
		<aside>
			<header>
				<h2 class="tright">Balance</h2>
				<h1 class="tright"><py>print(self.curr(balance_), file=stdout)</py></h1>
			</header>
		</aside>
			
		<section>
			<header>
				<h1>Token / Overview</h1>
				<h2><span class="pagenav link" data-url="/chain/<py>print(vars.chainid, file=stdout)</py>"><py>print(vars.chainid, file=stdout)</py></span></h2>
			</header>
		</section>

	</section>

	<p>For detail click on the hyperlinks to drill down for more data</p>

	<ul class="actions collection clear">
		<li class="header"><span class="upper"><py>print(vars.tokenid, file=stdout)</py></span></li>
		<li class="right">
			<span class="button red" data-event="{'action':'Xscro.Tokens','event':'destroyToken','args':{'chainid':'<py>print(vars.chainid, file=stdout)</py>','tokenid':'<py>print(vars.tokenid, file=stdout)</py>'}}">Destroy</span>
		</li>
	</ul>

	<ul class="actions collection clear">
		<li class="header"><span>Heirarchy</span></li>
		<li class="right"></li>
	</ul>
	
	<section data-component="repeater" data-datasource="/api/<py>print(vars.chainid, file=stdout)</py>/enumerate/<py>print(vars.tokenid, file=stdout)</py>" data-enumerate='data' data-cache="0" data-sorton="transid" data-id="uid" data-mode="none">
		
		<ul class="list grid bordered"></ul>
		
		<div class="template header">
			
			<div class="fullwidth">
				
				<span class="fullwidth">
					<span class="w50 column"></span>
					<span class="w250 column">Token</span>
					<span class="w250 column">Recipient</span>
					<span class="wauto column">Comment</span>
					<span class="w100 column tright">Price</span>
					<span class="w100 column tright">Balance</span>
				</span>
			
			</div>
		
		</div>
		
		<div class="template item" data-itemclass="transaction__entry">
			
			<div class="fullwidth">
				
				<span class="fullwidth">
					<span class="w50 tright">%transid%</span>
					<span class="w250 upper pagenav link" data-url="/chain/<py>print(vars.chainid, file=stdout)</py>/token/%uid%">%uid%</span>
					<span class="w250 upper pagenav link" data-url="/chain/<py>print(vars.chainid, file=stdout)</py>/owner/%id_recipient%">%id_recipient%</span>
					<span class="resizing upper">%additional%</span>
					<span class="w100 tright">%token_price:fn:currency%</span>
					<span class="w100 tright">%balance:fn:currency%</span>
				</span>
			
			</div>
		
		</div>
	
	</section>

	<ul class="actions collection clear">
		<li class="header"><span>Recent Transactions</span></li>
		<li class="right">
			<span class="button orange" data-event="{'action':'Xscro','event':'refresh','args':{}}">Refresh</span>
		</li>
	</ul>

	<section data-component="repeater" data-datasource="/api/<py>print(vars.chainid, file=stdout)</py>/list/token/<py>print(vars.tokenid, file=stdout)</py>" data-enumerate='data' data-cache="0" data-sorton="transid" data-id="uid" data-mode="none">
		
		<ul class="list grid bordered"></ul>
		
		<div class="template header">
			
			<div class="fullwidth">
				
				<span class="fullwidth">
					<span class="w50 column"></span>
					<span class="w250 column">Token</span>
					<span class="w250 column">Recipient</span>
					<span class="wauto column">Comment</span>
					<span class="w100 column tright">Price</span>
					<span class="w100 column tright">Volume</span>
				</span>

			</div>

		</div>

		<div class="template item" data-itemclass="transaction__entry">
			
			<div class="fullwidth">
				
				<span class="fullwidth">
					<span class="w50 tright">%transid%</span>
					<span class="w250 upper pagenav link" data-url="/chain/<py>print(vars.chainid, file=stdout)</py>/token/%uid%">%uid%</span>
					<span class="w250 upper pagenav link" data-url="/chain/<py>print(vars.chainid, file=stdout)</py>/owner/%id_recipient%">%id_recipient%</span>
					<span class="resizing upper">%additional%</span>
					<span class="w100 tright">%token_price:fn:currency%</span>
					<span class="w100 tright">%volume:fn:currency%</span>
				</span>
			
			</div>

		</div>
	
	</section>
	
	<section>
		
		<ul class="actions collection clear">
			<li class="header"><span>Transfer To Recipient</span></li>
			<li class="right">
				<span class="button green" data-event="{'action':'Xscro.Tokens','event':'transferToken','args':{'chainid':'<py>print(vars.chainid, file=stdout)</py>','tokenid':'<py>print(vars.tokenid, file=stdout)</py>'}}">Transfer</span>
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
							<div><input name='ignore' readonly class="upper w400" data-req="true" type='text' data-default='uid' value='<py>print(vars.tokenid, file=stdout)</py>' data-validator='uuid'></input><span class="field req">uid</span></div>
						</li>
						
						<li>
							<div><input name='id_recipient' class="upper w400" data-req="true" type='text' data-default='id_recipient' value='id_recipient' data-validator='anychar'></input><span class="field req">id_recipient</span></div>
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
							<div><input name='additional' class="w400" data-req="true" type='text' data-default='comment' value='Token transferred' data-validator='anychar'></input><span class="field req">comment</span></div>
						</li>
			
					</ul>
				
				</section>
				
				<aside class="notes">
					
					<p>Supply the details on the right to transfer a new token</p>

				</aside>
					
			</section>

		</form>
	
	</section>

	<pyinclude>views/__bits/appvars.html.py</pyinclude>
	
	<pyinclude>views/__bits/page/footer.html.py</pyinclude>

</section>
