$(function() {
    $(".toggle-button").click(function(){
        $(this).toggleClass("toggle-button-selected");
        //$( "#target" ).submit();
        
        //Temp Code showing how to use AJAX to post without changing pages
        $.ajax({
            url: $(this).attr("action"),
            type: 'POST',
            data: $(this).serialize(),
            beforeSend: function() {
                $("#message").html("sending...");
            },
            success: function(data) {
                $("#message").hide();
                $("#response").html(data);
            }
        });
    });
    
    $("button#edit-item").click(function(){
        $( "#edit-description" ).val($(this).closest("tr").find('td:eq(0)').text());
        $( "#edit-link" ).val($(this).closest("tr").find('td:eq(1)').find("a").attr("href"));
        $( "#edit-form" ).dialog( "open" );
    });
    
    $("button#add-item").click(function(){
        $( "#add-description" ).val("");
        $( "#add-link" ).val("");
        $( "#add-form" ).dialog( "open" );
    });
      
    function saveItem() {
      var valid = true;
      return valid;
    }
    
    function deleteItem() {
      var valid = true;
      return valid;
    }

    $( "#edit-form" ).dialog({
      autoOpen: false,
      height: 300,
      width: 500,
      modal: true,
      buttons: {
        "Save Item": saveItem,
        "Delete Item": deleteItem,
        Cancel: function() {
          dialog.dialog( "close" );
        }
      },
      close: function() {

      }
    });
    
    $( "#add-form" ).dialog({
      autoOpen: false,
      height: 300,
      width: 500,
      modal: true,
      buttons: {
        "Save Item": saveItem,
        Cancel: function() {
          dialog.dialog( "close" );
        }
      },
      close: function() {
//        form[ 0 ].reset();
      }
    });

//    form = dialog.find( "form" ).on( "submit", function( event ) {
//      event.preventDefault();
 //     addUser();
 //   });


  });
