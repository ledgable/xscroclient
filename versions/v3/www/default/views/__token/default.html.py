
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
	
	<pyinclude>views/__bits/appvars.html.py</pyinclude>
	
	<pyinclude>views/__bits/page/footer.html.py</pyinclude>

</section>
