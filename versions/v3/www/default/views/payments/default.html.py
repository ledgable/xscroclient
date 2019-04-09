
<py>

from dataobjects import *
from modules.helpers import *

payment_ = vars.payment

if (payment_ == None):
	payment_ = extdict({})

</py>

<section class="panel focus w600 blue">

	<div class="top">
		<span>Process Payment : Login</span>
	</div>

	<div class="content">

		<h4>Payment Information</h4></li>

		<section class="grid_p clear">

			<aside>

				<span class="icon company big"></span>

			</aside>

			<section>

				<form id="wallet__info" class="controldata">

					<ul class="fields">

						<li><span class="highlight"><pre><py>print(payment_.recipient.displayas, file=stdout)</py></pre></span></li>

						<li><span class="highlight"><pre><py>print(payment_.description, file=stdout)</py></pre></span></li>

						<li><span class="highlight">To Pay: <strong class="right"><py>print(default("%s %s" % (sanitize(payment_.amount), payment_.token.upper()), "--"), file=stdout)</py></strong></span></li>

						<li>To begin a payment, please login to your wallet</li>

						<li>
							<div class="fullwidth"><input name="walletid" type="text" class="w100p" data-req="true" data-default="Wallet Address" value="<py>print(default(payment_.sender.walletid, "Wallet Address"), file=stdout)</py>" data-validator="anychar"></input><span class="field req">Wallet Address</span></div>
						</li>

						<li>
							<div class=""><input name="password" type="password" class="w300" data-req="true" data-default="Password" value="Password"></input><span class="field req">Password</span></div>
						</li>

						<li>Logging-in does not automatically confirm payment</li>
				
						<li>Cancelling payment will return you to your e-shop</li>

					</ul>

				</form>

			</section>

		</section>

		<ul class="clear">
			<li class="action right">
				<span class="button red upper" data-event="{'action':'Payments','event':'cancel','args':{}}">Cancel</span>
				<span class="button green upper" data-event="{'action':'Payments','event':'login','args':{'chainid':'<py>print(payment_.chainid, file=stdout)</py>'}}">Login</span>
			</li>
		</ul>

	</div>

	<div class="bottom">
		<span><py>print("%s:%s" % (self.session.id_session, payment_.transactionid), file=stdout)</py></span>
	</div>

</section>
