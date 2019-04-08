
<py>

from modules import *

application_ = ApplicationManager(self).get("xscro")
chains_ = []
chainid_ = None

if (application_ != None):
	chains_ = application_.chains
	if (len(chains_) > 0):
		chainid_ = chains_[0]

</py>

<section class="panel blue focus w500">

	<div class="top">
		<span>User Signup</span>
	</div>

	<div class="content">

		<section class="grid_p clear">

			<aside>

				<span class="icon company big"></span>

			</aside>

			<section>

				<h1>Welcome</h1>

				<p>Create a new wallet</p>

				<form id="user__info" class="controldata">

					<ul class="fields">

						<li>
							<div class=""><input name="walletid" type="text" class="w300" data-req="true" data-default="Wallet Address" value="Wallet Address" data-validator="anychar"></input><span class="field req">Wallet Address</span></div>
						</li>

						<li>
							<div class=""><input name="password" type="password" class="w300" data-req="true" data-default="Password" value="Password"></input><span class="field req">Password</span></div>
						</li>

						<li>
							<div class=""><input name="confirm_password" type="password" class="w300" data-req="true" data-default="Password" value="Password"></input><span class="field req">Password</span></div>
						</li>

						<li>

							<div class="fullwidth"><span class="field req">Chain</span><select name="chainid" class="w300">
								<option disabled="disabled">Select Chain</option>

<py>

for chain_ in chains_:
	if (chain_ == chainid_):
		print("""<option selected value="%s">%s</option>""" % (chain_, chain_), file=stdout)
	else:
		print("""<option value="%s">%s</option>""" % (chain_, chain_), file=stdout)

</py>

							</select><span class="form-icon icon icon-chevron-down" aria-hidden="true">&nbsp;</span></div>
						</li>

					</ul>

					<ul class="clear">
						<li class="action">
							<span class="button orange pagenav upper" data-url="/user">Login</span>
							<span class="button green upper" data-event="{'action':'User.Security','event':'newuser','args':{}}">Create Wallet</span>
						</li>
					</ul>

				</form>

			</section>

		</section>

	</div>

</section>
