
<py>

chainid_ = "43b706140904439f90cfac32dc4088de"

</py>

<header>
	<h2>Welcome</h2>
	<h1>Service Administration</h1>
</header>

<section class="" data-component="stepshow">

	<ul class="pips clear">
		
		<li class="pip selected"><span>Transactions</span></li>
		<li class="pip"><span>Pending</span></li>
		<li class="pip"><span>Wallets</span></li>
		<li class="action right"><span class="button red upper" data-event="{'action':'Security.User','event':'logout','args':{}}">Logout</span></li>
	
	</ul>

	<ul class="steps">
		
		<li class="selected">
		
			<section class="transactions">
		
				<ul class="actions collection clear">
					<li class="header"><span>Recent Transactions</span></li>
					<li class="right">
						<span class="button orange" data-event="{'action':'Xscro','event':'refresh','args':{}}">Refresh</span>
					</li>
				</ul>

				<section data-component="repeater" data-datasource="/api/<py>print(chainid_, file=stdout)</py>/transactions/last/100" data-enumerate='transactions' data-cache="0" data-sorton="!transid" data-id="uid" data-mode="none">
					
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
								<span class="w250 upper pagenav link" data-url="/chain/<py>print(chainid_, file=stdout)</py>/token/%uid%">%uid%</span>
								<span class="w250 upper pagenav link" data-url="/chain/<py>print(chainid_, file=stdout)</py>/token/%id_parent%">%id_parent%</span>
								<span class="w250 upper pagenav link" data-url="/chain/<py>print(chainid_, file=stdout)</py>/owner/%id_recipient%">%id_recipient%</span>
								<span class="resizing upper">%additional%</span>
								<span class="w100 tright">%token_price:fn:currency%</span>
								<span class="w100 tright">%volume:fn:currency%</span>
							</span>
						
						</div>

					</div>
	
				</section>
	
			</section>
		
		</li>

		<li>
		
			<section class="transactions">
				
				<ul class="actions collection clear">
					<li class="header"><span>Recent Transactions</span></li>
					<li class="right">
						<span class="button orange" data-event="{'action':'Xscro','event':'refresh','args':{}}">Refresh</span>
					</li>
				</ul>
			
				<section data-component="repeater" data-datasource="/api/<py>print(chainid_, file=stdout)</py>/transactions/last/100" data-enumerate='transactions' data-cache="0" data-sorton="!transid" data-id="uid" data-mode="none">
				
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
								<span class="w250 upper pagenav link" data-url="/chain/<py>print(chainid_, file=stdout)</py>/token/%uid%">%uid%</span>
								<span class="w250 upper pagenav link" data-url="/chain/<py>print(chainid_, file=stdout)</py>/token/%id_parent%">%id_parent%</span>
								<span class="w250 upper pagenav link" data-url="/chain/<py>print(chainid_, file=stdout)</py>/owner/%id_recipient%">%id_recipient%</span>
								<span class="resizing upper">%additional%</span>
								<span class="w100 tright">%token_price:fn:currency%</span>
								<span class="w100 tright">%volume:fn:currency%</span>
							</span>
						
						</div>
				
					</div>
				
				</section>

			</section>
				
		</li>
			
		<li>
			
		</li>

	</ul>

</section>
