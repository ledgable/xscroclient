
<py>

from dataobjects import *
from modules.helpers import *

payment_ = vars.payment

if (payment_ == None):
	payment_ = extdict({})

</py>

<section class="panel focus w600 blue">

	<div class="top">
		<span>Confirm Payment</span>
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
			
						<li><span class="highlight">Balance: <strong class="right"><py>print(default("%s %s" % (sanitize(payment_.balance), payment_.token.upper()), "--"), file=stdout)</py></strong></span></li>

						<li>After payment you will have</li>

						<li><span class="highlight">Balance: <strong class="right"><py>print(default("%s %s" % (sanitize(payment_.remaining), payment_.token.upper()), "--"), file=stdout)</py></strong></span></li>

						<li>Clicking "Confirm Payment" will finalize the payment process</li>

					</ul>

				</form>

			</section>

		</section>

		<ul class="clear">
			<li class="action right">
				<span class="button orange upper" data-event="{'action':'Payments','event':'cancel','args':{}}">Cancel</span>
				<span class="button green upper" data-event="{'action':'Payments','event':'confirm','args':{}}">Confirm Payment</span>
			</li>
		</ul>

	</div>

	<div class="bottom">
		<span><py>print("%s:%s" % (self.session.id_session, payment_.transactionid), file=stdout)</py></span>
	</div>

</section>
