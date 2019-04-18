
<py>

chainid_ = self.session.chainid

</py>

<header>
	<h2>Welcome</h2>
	<h1>User Management</h1>
</header>

<section class="" data-component="stepshow">

	<ul class="pips clear">
		
		<li class="pip selected"><span>Overview</span></li>
		<li class="pip"><span>Transactions</span></li>
		<li class="action right">
			<span class="button orange" data-event="{'action':'User.Security','event':'showChangePassword','args':{}}">Change Password</span>
			<span class="button red upper" data-event="{'action':'User.Security','event':'logout','args':{}}">Logout</span>
		</li>
	
	</ul>

	<ul class="steps">
		
		<li class="selected">
			<pyinclude>views/user/__overview.html.py</pyinclude>
		</li>

		<li>
			<pyinclude>views/user/__transactionlist.html.py</pyinclude>
			
			<pyinclude>views/user/__pendinglist.html.py</pyinclude>
		</li>

	</ul>

</section>
