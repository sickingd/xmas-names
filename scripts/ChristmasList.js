$(function() {
    var old_edit_description;
    
    $( document ).ready(function() {
        //To correctly set the is_fulfilled toggle state, read elements with ID's set to True 
        //and change the toggle class
        $('*[id*="True"]').each(function() {
            $(this).toggleClass("toggle-button-selected")
        });
        
    });
    
    $(".toggle-button").click(function(){
        $(this).toggleClass("toggle-button-selected");
        var fulfilled;
        if ($(this).attr("class") == "toggle-button toggle-button-selected") {
            fulfilled = "True";
        } else {
            fulfilled = "False";
        }
        description = $(this).closest("tr").find('td:eq(0)').text();
        person_name = document.getElementById('person-name').textContent;
        assigned_person_name = $(this).closest('table').attr('id');
       
        $.ajax({
            type: "POST",
            url: "/fulfilled",
            dataType: 'json',
            data: JSON.stringify({ "fulfilled": fulfilled,
                                   "description": description,
                                   "person_name": person_name,
                                   "assigned_person_name": assigned_person_name})
        })
    });
    
    $("button#edit-item").click(function(){
        old_edit_description = $(this).closest("tr").find('td:eq(0)').text();
        $( "#edit-description" ).val(old_edit_description);
        $( "#edit-link" ).val($(this).closest("tr").find('td:eq(1)').find("a").attr("href"));
        $( "#edit-form" ).dialog( "open" );
    });
    
    $("button#add-item").click(function(){
        $( "#add-description" ).val("");
        $( "#add-link" ).val("");
        $( "#add-form" ).dialog( "open" );
    });
    
      
    function saveItem() {
        //alert("New Description is: " + $( "#edit-description" ).val() + " and link is: " + $( "#edit-link" ).val());

        data = JSON.stringify({ "person_name": document.getElementById('person-name').textContent,
                                "old_description": old_edit_description,
                                "new_description": $( "#edit-description" ).val(),
                                "new_link": $( "#edit-link" ).val()})      
        $.post( "/edit_item", data, 
            function(data,status){
                reloadPage(data)
        });
        
        $( "#edit-form" ).dialog( "close" );
    }
    
    function addNewItem() {
        //alert("New Description is: " + $( "#add-description" ).val() + " and link is: " + $( "#add-link" ).val());
        
        // In order to use ajax, a callback function for reload needs to be specified
//        $.ajax({
//            type: "POST",
//            url: "/add_item",
//            dataType: 'json',
//            data: JSON.stringify({ "person_name": document.getElementById('person-name').textContent,
//                                   "new_description": $( "#add-description" ).val(),
//                                   "new_link": $( "#add-link" ).val()})
//        })        

        data = JSON.stringify({ "person_name": document.getElementById('person-name').textContent,
                                "new_description": $( "#add-description" ).val(),
                                "new_link": $( "#add-link" ).val()})       
        $.post( "/add_item", data, 
            function(data,status){
                reloadPage(data)
        });    
        
        $( "#add-form" ).dialog( "close" );
    }    
    
    function reloadPage(data){
        document.location.reload();
    }
    
    function deleteItem() {
        //alert("Deleting: " + $( "#edit-description" ).val());
      
        data = JSON.stringify({ "person_name": document.getElementById('person-name').textContent,
                                "description": $( "#edit-description" ).val()})
        $.post( "/delete_item", data, 
            function(data,status){
                reloadPage(data)
        });   
        
        $( "#edit-form" ).dialog( "close" );
    }

    $( "#edit-form" ).dialog({
      autoOpen: false,
      height: 'auto',
      width: 'auto',
      fluid: true,
      modal: true,
      buttons: {
        "Save Item": saveItem,
        "Delete Item": deleteItem,
        Cancel: function() {
          $( "#edit-form" ).dialog( "close" );
        }
      },
      close: function() {
         //location_var = $(location).attr('href');
         //alert(location_var);
         //window.location.replace(location_var);
      }
    });
    
    $( "#add-form" ).dialog({
      autoOpen: false,
      height: 'auto',
      width: 'auto',
      fluid: true,
      modal: true,
      buttons: {
        "Save Item": addNewItem,
        Cancel: function() {
          $( "#add-form" ).dialog( "close" );
        }
      },
      close: function() {
          //document.location.reload(true);
      }
    });
    
    // catch dialog if opened within a viewport smaller than the dialog width
    $(document).on("dialogopen", ".ui-dialog", function (event, ui) {
        fluidDialog();
    });
    
    // Credit to: http://stackoverflow.com/questions/16471890
    function fluidDialog() {
        var $visible = $(".ui-dialog:visible");
        // each open dialog
        $visible.each(function () {
            var $this = $(this);
            var dialog = $this.find(".ui-dialog-content").data("ui-dialog");
            // if fluid option == true
            if (dialog.options.fluid) {
                var wWidth = $(window).width();
                // check window width against dialog width
                if (wWidth > 786)  {
                    // 700px is the max needed
                    $this.css("width", "700px");
                } else {
                    // For responsive design, max out at 90% for smaller width devices
                    $this.css("width", "90%");
                }
                //reposition dialog
                dialog.option("position", dialog.options.position);
            }
        });

    }



  });
