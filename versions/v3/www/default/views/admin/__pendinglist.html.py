
<py>

chainid_ = self.session.chainid

</py>

<section class="transactions">
	
	<ul class="actions collection clear">
		<li class="header"><span>Pending Transactions</span></li>
		<li class="right">
			<span class="button orange" data-event="{'action':'Xscro','event':'refresh','args':{}}">Refresh</span>
		</li>
	</ul>
			
	<section data-component="repeater" data-datasource="/api/<py>print(chainid_, file=stdout)</py>/open/transactions" data-enumerate='transactions' data-cache="0" data-sorton="!$time" data-id="uid" data-mode="none">
		
		<ul class="list grid bordered"></ul>
		
		<div class="template header">
			
			<div class="fullwidth">
				
				<span class="fullwidth">
					<span class="w100 column"></span>
					<span class="w250 column">Token</span>
					<span class="w250 column">Parent</span>
					<span class="w250 column">Recipient</span>
					<span class="wauto column">Comment</span>
					<span class="w100 column tright">Volume</span>
					<span class="w60 column"></span>
				</span>
			
			</div>
		
		</div>
		
		<div class="template item" data-itemclass="transaction__entry">
			
			<div class="fullwidth">
				
				<span class="fullwidth">
					<span class="w100 tright">%$time:epoch:dd-MMM-yyyy HH:mm%</span>
					<span class="w250">%uid%</span>
					<span class="w250">%id_parent%</span>
					<span class="w250">%id_recipient%</span>
					<span class="resizing">%additional%</span>
					<span class="w100 tright">%volume:fn:currency%</span>
					<span class="w60 tright">
						<span class="icon icon_accept" data-event="{'action':'Admin.Transactions','event':'ackTransaction','args':{'chainid':'<py>print(chainid_, file=stdout)</py>', 'token':'%uid%', 'code':1}}"></span>
						<span class="icon icon_cancel" data-event="{'action':'Admin.Transactions','event':'ackTransaction','args':{'chainid':'<py>print(chainid_, file=stdout)</py>', 'token':'%uid%', 'code':0}}"></span>
					</span>
				</span>
			
			</div>
		
		</div>

	</section>

</section>
