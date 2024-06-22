jQuery.noConflict();
jQuery(document).ready(function($) {
    function updateOptions() {
        var selectedDepart = $('#id_adress_depart').val();
        var selectedArrivee = $('#id_adress_arrivee').val();
        console.log(selectedDepart);
        console.log(selectedArrivee);

        // Show all options in both selects initially
        $('#id_adress_depart option, #id_adress_arrivee option, #id_arrets option').show();

        // Hide the selected arrivee in depart options
        if (selectedArrivee) {
            $('#id_adress_depart option').each(function() {
                if ($(this).val() === selectedArrivee) {
                    $(this).hide();
                }
            });
        }

        // Hide the selected depart in arrivee options
        if (selectedDepart) {
            $('#id_adress_arrivee option').each(function() {
                if ($(this).val() === selectedDepart) {
                    $(this).hide();
                }
            });
            
        }
        
    }

    // Update options when either select changes
    $('#id_adress_depart').change(function() {
        updateOptions();
    });

    $('#id_adress_arrivee').change(function() {
        updateOptions();
    });

    // Initial hiding of options on page load based on current selections
    updateOptions();
});

