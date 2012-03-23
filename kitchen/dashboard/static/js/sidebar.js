function setupClickHandlers() {
    /**
     * Assign click handlers to all sidebar entries.
     */
    $('.sidebar_link').click(function() { 
        var parameters = {};
        var active_buttons = $('.active .sidebar_link');
        if (active_buttons.index(this) > -1) {
            active_buttons = active_buttons.not(this);
        } else {
            //active_buttons.add(this);
            active_buttons = $.fn.add.call(active_buttons, this);
        }
        var changed_environment = false;
        var changed_virt_environment = false;
        // add already selected buttons to the params
        for (var i=0; i < active_buttons.length; i++) {
            var datatype = active_buttons[i].dataset['type'];
            var dataname = active_buttons[i].dataset['name'];
            if (datatype === 'env') {
                if (active_buttons[i] === this) {
                    parameters[datatype] = dataname;
                    changed_environment = true;
                } else if (!changed_environment) {
                    parameters[datatype] = dataname;
                }
            } else if (datatype === 'virt') {
                if (active_buttons[i] === this) {
                    parameters[datatype] = dataname;
                    changed_virt_environment = true;
                } else if (!changed_virt_environment) {
                    parameters[datatype] = dataname;
                }
            } else {
                if (datatype in parameters && datatype !== 'env') {
                    parameters[datatype] += ',' + dataname;
                } else {
                    parameters[datatype] = dataname;
                }
            }
        }
        
        var url = '?';
        for (var param in parameters) {
            url += param + '=' + parameters[param] + '&';
        }
        window.location = url.slice(0, -1); // remove trailing '&'
    });
}