
<py>

chainid_ = self.session.chainid

</py>

<header>
	<h2>Welcome</h2>
	<h1>Service Administration</h1>
</header>

<section class="" data-component="stepshow">

	<ul class="pips clear">
		
		<li class="pip selected"><span>Overview</span></li>
		<li class="pip"><span>Transactions</span></li>
		<li class="pip"><span>Pending</span></li>
		<li class="pip"><span>Wallets</span></li>
		<li class="action right">
			
			<span><form id="chain__selector" class="controldata">
				<div class="position_selector">
					<select name="chainid" data-selected="<py>print(chainid_, file=stdout)</py>" data-datasource="/api/admin/chains" data-event="{'action':'Admin', 'event':'switchChain','args':{}}" class="w300">
						<option disabled="disabled">Select Chain</option>
					</select><span class="form-icon icon icon-chevron-down" aria-hidden="true">&nbsp;</span>
				</div>
			</form></span>
			
			<span class="button red upper" data-event="{'action':'Admin.Security','event':'logout','args':{}}">Logout</span>
		</li>
	
	</ul>

	<ul class="steps">
		
		<li class="selected">
			<pyinclude>views/admin/__overview.html.py</pyinclude>
		</li>

		<li>
			<pyinclude>views/admin/__transactionlist.html.py</pyinclude>
		</li>

		<li>
			<pyinclude>views/admin/__pendinglist.html.py</pyinclude>
		</li>
			
		<li>
			<pyinclude>views/admin/__walletlist.html.py</pyinclude>
		</li>

	</ul>

</section>
