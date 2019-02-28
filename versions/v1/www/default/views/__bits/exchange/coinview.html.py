
<py>

chainid_ = None

if ("chainid" in vars.keys()):
	chainid_ = vars.chainid

</py>

<h3>Minted Coins <py>print(chainid_, file=stdout)</py></h3>

<section data-component="repeater" data-datasource="/api/<py>print(chainid_, file=stdout)</py>/children/0" data-enumerate='tokens' data-cache="0" data-id="uid" data-mode="none">
		
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
					<span class="resizing upper">%token%</span>
					<span class="w100 tright">%volume:fn:currency%</span>
					<span class="w100 tright">%balance:fn:currency%</span>
				</span>
			
			</div>

	</div>
	
</section>
