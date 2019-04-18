
<py>

chainid_ = self.session.chainid

</py>

<section class="transactions">

	<ul class="actions collection clear">
		<li class="header"><span>Overview</span></li>
		<li class="right">
		</li>
	</ul>

	<h1>Balance</h1>

	<section data-component="repeater" data-datasource="/api/user/balance" data-enumerate='wallets' data-cache="0" data-sorton="balance" data-id="walletid" data-mode="none">

		<ul class="list grid bordered"></ul>

		<div class="template header">

			<div class="fullwidth">

				<span class="fullwidth">
					<span class="w100 column"></span>
					<span class="w250 column">Wallet</span>
					<span class="wauto column tright">Balance</span>
					<span class="w60 column"></span>
				</span>

			</div>

		</div>

		<div class="template item" data-itemclass="transaction__entry">

			<div class="fullwidth">

				<span class="fullwidth">
					<span class="w100 tright"></span>
					<span class="w250">%walletid%</span>
					<span class="resizing tright">%balance:fn:currency%</span>
					<span class="w60 column"></span>
				</span>

			</div>

		</div>

	</section>

</section>
