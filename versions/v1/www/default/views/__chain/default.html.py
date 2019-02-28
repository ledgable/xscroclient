
<section class="trading__view">
	<canvas data-component="statplot" data-datasource="/api/<py>print(vars.chainid, file=stdout)</py>/data/0"></canvas>
</section>

<section class="inner clear">

	<header>
		<h1>Chain / Overview</h1>
		<h2><py>print(vars.chainid, file=stdout)</py></h2>
	</header>

	<p>For detail click on the hyperlinks to drill down for more data</p>

	<section class="analytics">

		<ul class="actions collection clear">
			<li class="header"><span>Analytics</span></li>
			<li class="right"></li>
		</ul>

		<ul class="collection">
			<li><canvas width="250px" height="250px" data-component="statcircle" data-width="30" data-gap="2" data-mode="0" data-vals="[0.55]" data-colors="['006600']"></canvas></li>
			<li><canvas width="250px" height="250px" data-component="statcircle" data-width="30" data-gap="2" data-mode="0" data-vals="[0.38]" data-colors="['999999']"></canvas></li>
			<li><canvas width="250px" height="250px" data-component="statcircle" data-width="30" data-gap="2" data-mode="0" data-vals="[0.38]" data-colors="['999999']"></canvas></li>
			<li><canvas width="250px" height="250px" data-component="statcircle" data-width="30" data-gap="2" data-mode="0" data-vals="[0.38]" data-colors="['999999']"></canvas></li>
		</ul>
			
	</section>

	<section class="tokens">
	
		<ul class="actions collection clear">
			<li class="header"><span>Tokens</span></li>
			<li class="right">
				<span class="button green pagenav" data-url="/chain/<py>print(vars.chainid, file=stdout)</py>/mint">Mint Token</span>
			</li>
		</ul>

		<section data-component="repeater" data-datasource="/api/<py>print(vars.chainid, file=stdout)</py>/children/0" data-enumerate='tokens' data-cache="0" data-id="uid" data-mode="none">
		
			<ul class="list grid bordered"></ul>
			
			<div class="template header">
				
				<div class="fullwidth">
					
					<span class="fullwidth">
						<span class="w50 column"></span>
						<span class="wauto column">Token</span>
						<span class="w100 column tright">Volume</span>
						<span class="w100 column tright">Balance</span>
					</span>
				
				</div>

			</div>
		
			<div class="template item" data-itemclass="record__entry">
			
				<div class="fullwidth">
				
					<span class="fullwidth">
						<span class="w50"></span>
						<span class="resizing upper pagenav link" data-url="/chain/<py>print(vars.chainid, file=stdout)</py>/token/%token%">%token%</span>
						<span class="w100 tright">%volume:fn:currency%</span>
						<span class="w100 tright">%balance:fn:currency%</span>
					</span>
				
				</div>

			</div>

		</section>
	
	</section>
	
	<section class="transactions">
	
		<ul class="actions collection clear">
			<li class="header"><span>Recent Transactions</span></li>
			<li class="right">
				<span class="button orange" data-event="{'action':'Xscro','event':'refresh','args':{}}">Refresh</span>
			</li>
		</ul>
		
		<section data-component="repeater" data-datasource="/api/<py>print(vars.chainid, file=stdout)</py>/transactions/last/100" data-enumerate='transactions' data-cache="0" data-sorton="!transid" data-id="uid" data-mode="none">
			
			<ul class="list grid bordered"></ul>

			<div class="template header">
			
				<div class="fullwidth">
				
					<span class="fullwidth">
						<span class="w50 column"></span>
						<span class="w250 column">Token</span>
						<span class="w250 column">Parent</span>
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
						<span class="w250 upper pagenav link" data-url="/chain/<py>print(vars.chainid, file=stdout)</py>/token/%id_parent%">%id_parent%</span>
						<span class="w250 upper pagenav link" data-url="/chain/<py>print(vars.chainid, file=stdout)</py>/owner/%id_recipient%">%id_recipient%</span>
						<span class="resizing upper">%additional%</span>
						<span class="w100 tright">%token_price:fn:currency%</span>
						<span class="w100 tright">%volume:fn:currency%</span>
					</span>

				</div>
		
			</div>
		
		</section>
	
	</section>

	<pyinclude>views/__bits/appvars.html.py</pyinclude>
	
	<pyinclude>views/__bits/page/footer.html.py</pyinclude>

</section>
