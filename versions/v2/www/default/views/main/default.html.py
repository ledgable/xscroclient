
<section class="inner">

	<header>
		<h1>XSCRO Datanode</h1>
		<h2>XSCRO is a Ledgable product released under the GPLv3 license</h2>
	</header>
	
	<p>For information regarding the license please see <a href="https://www.gnu.org/licenses/gpl-3.0.en.html" target="__blank" class="link">https://www.gnu.org/licenses/gpl-3.0.en.html</a></p>

	<h1>Overview</h1>

	<ul class="chains">

<py>
chains_ = self.chains()

if (chains_ != None):
	for chain_ in chains_:
		print("""<li class="pagenav upper" data-url="/chain/%s">%s</li>""" % (chain_, chain_))
</py>

	</ul>
	
	<pyinclude>views/__bits/appvars.html.py</pyinclude>

	<pyinclude>views/__bits/page/footer.html.py</pyinclude>

</section>
