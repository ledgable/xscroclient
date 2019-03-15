
<py>

chainid_ = self.session.chainid

</py>

<section class="transactions">
	
	<ul class="actions collection clear">
		<li class="header"><span>Wallets</span></li>
		<li class="right">
			<span class="button orange" data-event="{'action':'Admin.Wallets','event':'showAddWallets','args':{'uid':'<py>print(chainid_, file=stdout)</py>'}}">Add Wallets</span>
		</li>
	</ul>

	<section data-component="repeater" data-datasource="/api/admin/<py>print(chainid_, file=stdout)</py>/wallets" data-enumerate="wallets" data-cache="0" data-sorton="!$time" data-id="uid" data-mode="none">
	
		<ul class="list"></ul>

		<div class="template item" data-itemclass="wallet__entry">
			<span class="icon"></span>
			<span class="info fullwidth">
				<span class="balance fullwidth">%balance:fn:currency%</span>
				<span class="address fullwidth">%uid:concat:7%</span>
			</span>
		</div>

	</section>

</section>
