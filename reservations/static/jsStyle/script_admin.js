
// jQuery.noConflict();
// jQuery(document).ready(function($) {
//     function updateSingleSelectOptions(selectedValues, targetSelect) {
//        console.log(targetSelect);
//         console.log(selectedValues);
//         $(targetSelect + ' option').each(function() {
//             if (selectedValues.includes($(this).val())) {
//                 $(this).hide();
//             } else {
//                 $(this).show();
//             }
//         });
//     }

//     function updateMultipleSelectOptions(selectedValues, targetSelect) {
//         $(targetSelect + ' option').each(function() {
//             if (selectedValues.includes($(this).val())) {
//                 $(this).hide();
//             } else {
//                 $(this).show();
//             }
//         });
//     }

//     function updateAllOptions() {
//         var selectedDepart = $('#id_adress_depart').val();
//         var selectedArrivee = $('#id_adress_arrivee').val();
//         var selectedArrets = $('#id_arrets').val() || [];

//         // Combine selected values from depart and arrivee
//         var selectedValues = [];
//         if (selectedDepart) selectedValues.push(selectedDepart);
//         if (selectedArrivee) selectedValues.push(selectedArrivee);

//         updateSingleSelectOptions(selectedArrets, '#id_adress_depart');
//         updateSingleSelectOptions(selectedArrets, '#id_adress_arrivee');
//         updateMultipleSelectOptions(selectedValues, '#id_arrets');
//     }

//     $('#id_arrets').change(function() {
//         updateAllOptions();
//     });

//     $('#id_adress_depart').change(function() {
//         updateAllOptions();
//     });

//     $('#id_adress_arrivee').change(function() {
//         updateAllOptions();
//     });

//     // Initial hiding of options on page load based on current selections
//     updateAllOptions();
// });

// // un peu 
// jQuery.noConflict();
// jQuery(document).ready(function($) {
//     function updateOptions() {
//         // Récupère les valeurs sélectionnées
//         var selectedDepart = $('#id_adress_depart').val();
//         var selectedArrivee = $('#id_adress_arrivee').val();
//         var selectedArrets = $('#id_arrets').val(); // Notez que ceci récupère un tableau de valeurs sélectionnées

//         // Affiche toutes les options au début
//         $('#id_adress_depart option, #id_adress_arrivee option, #id_arrets option').show();

//         // Cache les options sélectionnées dans les autres listes déroulantes
//         if (selectedDepart) {
//             $('#id_arrets option[value="' + selectedDepart + '"]').hide();
//         }
//         if (selectedArrivee) {
//             $('#id_arrets option[value="' + selectedArrivee + '"]').hide();
//         }
//         if (selectedArrets && selectedArrets.length > 0) {
//             selectedArrets.forEach(function(arret) {
//                 $('#id_adress_depart option[value="' + arret + '"]').hide();
//                 $('#id_adress_arrivee option[value="' + arret + '"]').hide();
//                 // Cache également les autres options d'arrets pour éviter les doublons
//                 $('#id_arrets option[value="' + arret + '"]').hide();
//             });
//         }
//     }

//     // Met à jour les options lors des changements de sélection
//     $('#id_adress_depart').change(updateOptions);
//     $('#id_adress_arrivee').change(updateOptions);
//     $('#id_arrets').change(updateOptions);

//     // Met à jour les options au chargement initial de la page
//     updateOptions();
// });
// depart et arrivee
jQuery.noConflict();
jQuery(document).ready(function($) {
    function updateOptions() {
        var selectedDepart = $('#id_adress_depart').val();
        var selectedArrivee = $('#id_adress_arrivee').val();
        var selectedDepartPosition = $('#id_adress_depart option:selected').index();
        var selectedArriveePosition = $('#id_adress_arrivee option:selected').index();
        console.log(selectedDepartPosition);
        console.log(selectedArriveePosition);

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
        // var departOrder = $('#id_adress_depart option:selected').data('ordre');
        // var arriveeOrder = $('#id_adress_arrivee option:selected').data('ordre');

        if (Math.abs(selectedDepartPosition - selectedArriveePosition) == 1) {
            $('#id_arrets option').each(function() {
               
                    $(this).hide();
                
            });
        };
        if (Math.abs(selectedDepartPosition - selectedArriveePosition) > 1) {
            var maxPosition = Math.max(selectedDepartPosition, selectedArriveePosition);
            var minPosition = Math.min(selectedDepartPosition, selectedArriveePosition);
            $('#id_arrets option').each(function() {
                if (($(this).val() >= maxPosition) || ($(this).val() <= minPosition)) {
                    $(this).hide();
                }
               
            });
        };

        

        // if (selectedDepart && selectedArrivee) {
        //     console.log(selectedDepart ,selectedArrivee )
        //     $('#id_arrets option').each(function() {
        //         console.log("arrets activer")
        //         console.log($(this).val())



        //         if (($(this).text() === selectedDepart) || ($(this).text() === selectedArrivee)) {
        //             $(this).hide();
        //         }
        //     });
        // }

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

