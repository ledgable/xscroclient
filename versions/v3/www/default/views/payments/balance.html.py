
<py>

from dataobjects import *
from modules.helpers import *

payment_ = vars.payment

if (payment_ == None):
	payment_ = extdict({})

mode_ = "blue"

amount_ = payment_.default("amount", 0.0)
balance_ = payment_.default("balance", 0.0)

if (amount_ > balance_):
	mode_ = "red"

</py>

<section class="panel focus w600 <py>print(mode_, file=stdout)</py>">

	<div class="top">
		<span>Process Payment</span>
	</div>

	<div class="content">

		<h4>Payment Information</h4></li>

		<section class="grid_p clear">

			<aside>

				<span class="icon company big"></span>

			</aside>

			<section>

				<form id="payment__info" class="controldata">

					<ul class="fields">

						<li><span class="highlight"><pre><py>print(payment_.recipient.displayas, file=stdout)</py></pre></span></li>
						
						<li><span class="highlight"><pre><py>print(payment_.description, file=stdout)</py></pre></span></li>

						<li><span class="highlight">To Pay: <strong class="right"><py>print(default("%s %s" % (sanitize(payment_.amount), payment_.token.upper()), "--"), file=stdout)</py></strong></span></li>

<py>
if (amount_ > balance_):
	print("""<li>You have insufficient funds available</li>""", file=stdout)
</py>
	
						<li><span class="highlight">Balance: <strong class="right"><py>print(default("%s %s" % (sanitize(payment_.balance), payment_.token.upper()), "--"), file=stdout)</py></strong></span></li>

						<li>Note your payment will not be finalizad until Confirmed</li>

						<li>Cancelling payment will return you to your e-shop</li>

					</ul>

				</form>

			</section>

		</section>

		<ul class="clear">
			<li class="action right">
				<span class="button orange upper" data-event="{'action':'Payments','event':'cancel','args':{}}">Cancel</span>

<py>
if (amount_ > balance_):
	print("""<span class="button red upper">Begin Payment</span>""", file=stdout)
else:
	print("""<span class="button green upper" data-event="{'action':'Payments','event':'pay','args':{}}">Begin Payment</span>""", file=stdout)
</py>
			</li>
		</ul>

	</div>

	<div class="bottom">
		<span><py>print("%s:%s" % (self.session.id_session, payment_.transactionid), file=stdout)</py></span>
	</div>

</section>
