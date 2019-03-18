
<py>

from dataobjects import *
from modules.helpers import *

payment_ = vars.payment

if (payment_ == None):
	payment_ = extdict({})

</py>

<section class="panel focus w600 blue">

	<div class="top">
		<span>Process Payment</span>
	</div>

	<div class="content">

		<h4>Payment Information</h4></li>

		<section class="grid_p clear">

			<aside>

				<span class="icon"></span>

			</aside>

			<section>

				<form id="payment__info" class="controldata">

					<ul class="fields">

						<li><span class="highlight"><pre><py>print(payment_.recipient.displayas, file=stdout)</py></pre></span></li>
						
						<li><span class="highlight"><pre><py>print(payment_.description, file=stdout)</py></pre></span></li>

						<li><span class="highlight">Amount: <strong class="right"><py>print(default("%f %s" % (payment_.amount, payment_.token.upper()), "--"), file=stdout)</py></strong></span></li>
						
						<li>Your available tokens are shown below</li>
						
						<section data-component="repeater" data-datasource="/api/tokens" data-enumerate='tokens' data-cache="0" data-sorton="!volume" data-id="uid" data-mode="none">
					
							<ul class="list grid bordered"></ul>
					
							<div class="template header">
						
								<div class="fullwidth">
									
									<span class="fullwidth">
										<span class="w50 column"></span>
										<span class="wauto column">Token</span>
										<span class="w100 column tright">Volume</span>
									</span>
								
								</div>

							</div>
					
							<div class="template item" data-itemclass="transaction__entry">
								
								<div class="fullwidth">
									
									<span class="fullwidth">
										<span class="w50 tright"><input name="tokenid" type="radio" value="%uid%"></input></span>
										<span class="resizing upper">%uid:concat:15%</span>
										<span class="w100 tright">%volume:fn:currency%</span>
									</span>
								
								</div>

							</div>
						
						</section>
			
						<li>Note your payment will not be finalizad until Confirmed</li>

						<li>Cancelling payment will return you to your e-shop</li>

					</ul>

				</form>

			</section>

		</section>

		<ul class="clear">
			<li class="action right">
				<span class="button orange upper" data-event="{'action':'Payments','event':'cancel','args':{}}">Cancel</span>
				<span class="button green upper" data-event="{'action':'Payments','event':'pay','args':{}}">Begin Payment</span>
			</li>
		</ul>

	</div>

	<div class="bottom">
		<span><py>print("%s:%s" % (self.session.id_session, payment_.transactionid), file=stdout)</py></span>
	</div>

</section>
