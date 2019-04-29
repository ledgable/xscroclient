
// Register and load the widget

function xscro_load_widget() {
	register_widget('xscro_buttonwidget');
}

add_action('widgets_init', 'xscro_load_widget');

// Creating the widget

class xscro_buttonwidget extends WP_Widget {
	
	function __construct() {
		
		parent::__construct(
							// Base ID of your widget
							'xscro_buttonwidget',
							
							// Widget name will appear in UI
							__('XSCRO Button Widget', 'xscro_widget_domain'),
							
							// Widget description
							array('description' => __('Widget for XSCRO payment button', 'xscro_widget_domain'), )
							);
		
	}
	
	// Creating widget front-end
	
	public function widget($args, $instance) {
		
		$fields = array("serverurl", "chainid", "recipientwallet", "recipientdisplay", "currency", "description", "amount", "callbacksuccess", "callbackfailure", "callbackcancel");
		$vars = array();

		foreach($fields as $field) {
			$vars[$field] = apply_filters('widget_'.$field, $instance[$field] );
		}
		
		// $title = apply_filters('widget_title', $instance['title'] );

		// before and after widget arguments are defined by themes
		echo $args['before_widget'];
		
		// This is where you run the code and display the output
		
		echo ("<form>");
		
		foreach($fields as $field) {
			if (!empty($vars[$field]))
				echo $field . '=' . $vars[$field];
		}
		
		echo ("</form>");
		
		echo $args['after_widget'];
		
	}
	
	// Widget Backend
	public function form($instance) {

		$fields = array("serverurl", "chainid", "recipientwallet", "recipientdisplay", "currency", "description", "amount", "callbacksuccess", "callbackfailure", "callbackcancel");
		
		$vars = array();

		foreach($fields as $field) {
		
			if (isset($instance[$field])) {
				$vars[$field] = $instance[$field];
			} else {
				$vars[$field] = __($field, 'xscro_widget_domain');
			}
			
			// Widget admin form
			
			echo "<p>";
			echo "<label for='" . $this->get_field_id($field) . "'>" . _e($field) . "</label>";
			echo "<input class='widefat' name='" . $field . "' type='text' value='" . esc_attr($vars[$field]) . "' />";
			echo "</p>";
			
		}
		
	}
	
	// Updating widget replacing old instances with new
	public function update( $new_instance, $old_instance ) {
		
		$instance = array();
		$fields = array("serverurl", "chainid", "recipientwallet", "recipientdisplay", "currency", "description", "amount", "callbacksuccess", "callbackfailure", "callbackcancel");
		
		foreach($fields as $field) {
			$instance[$field] = ( ! empty( $new_instance[$field] ) ) ? strip_tags($new_instance[$field]) : '';
		}

		return $instance;
	}
	
} // Class wpb_widget ends here
