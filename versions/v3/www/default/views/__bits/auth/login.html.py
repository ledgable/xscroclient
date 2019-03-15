
<section class="panel focus w500">

	<div class="top">
		<span>Login</span>
	</div>

	<div class="content">

		<form id="user__info" class="controldata">

			<ul class="fields">

				<li>
					<div class=""><input name="username" type="text" class="w300" data-req="true" data-default="Username" value="Username" data-validator="username"></input><span class="field req">Username</span></div>
				</li>

				<li>
					<div class=""><input name="password" type="password" class="w300" data-req="true" data-default="Password" value="Password"></input><span class="field req">Password</span></div>
				</li>

			</ul>

			<ul class="clear">
				<li class="action">
					<span class="button green upper" data-event="{'action':'Security.User','event':'login','args':{}}">Login</span>
				</li>
			</ul>

		</form>

	</div>

</section>
