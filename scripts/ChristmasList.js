$(function() {
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
        .done(function( data ) { // check why I use done
//            alert( "Vote Cast!!! Count is : " + data['story']['vote_count'] );
//            $('.voteCount').text(data['story']['vote_count']);
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
