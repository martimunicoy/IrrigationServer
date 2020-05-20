var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$("#status_form").on('submit', function(event){
    event.preventDefault()
    console.log("Status submitted") // sanity check
    update_status()
});

$("#cycle_form").on('submit', function(event){
    event.preventDefault()
    console.log("Cycle submitted") // sanity check
    update_cycle()
});

function update_messages(messages){
    var content = "<div class='messagerow'> <p class='messages'>"
    var message_counter = 0
    $.each(messages, function (i, m){
        content = content + "<p>" +
            m.message + "</p>"
        message_counter = message_counter + 1
    });
    content = content + "</p> </div>"

    if (message_counter == 0){
        $("#ajax_messages_block").html('')
    }
    else{
        $("#ajax_messages_block").html(content)
    }
}

function update_status() {
    console.log("Updating status") // sanity check

    var running = document.getElementById('id_running').checked
    var current_slot = document.getElementById('id_current_slot').value

    $.ajax({
        url : "ajax/submit_status/", // the endpoint
        type : "POST", // http method
    headers:{
        "X-CSRFToken": csrftoken
    },
        data : { running : running,
                 current_slot: current_slot,
                  }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            //$('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("Success"); // another sanity check
            update_messages(json.messages);  // update messages
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function update_cycle() {
    console.log("Updating cycle") // sanity check

    var slot1_description = document.getElementById('id_slot1_description').value
    var slot1_active = document.getElementById('id_slot1_active').checked
    var slot1_time = document.getElementById('id_slot1_time').value

    var slot2_description = document.getElementById('id_slot2_description').value
    var slot2_active = document.getElementById('id_slot2_active').checked
    var slot2_time = document.getElementById('id_slot2_time').value

    var slot3_description = document.getElementById('id_slot3_description').value
    var slot3_active = document.getElementById('id_slot3_active').checked
    var slot3_time = document.getElementById('id_slot3_time').value

    var slot4_description = document.getElementById('id_slot4_description').value
    var slot4_active = document.getElementById('id_slot4_active').checked
    var slot4_time = document.getElementById('id_slot4_time').value

    var slot5_description = document.getElementById('id_slot5_description').value
    var slot5_active = document.getElementById('id_slot5_active').checked
    var slot5_time = document.getElementById('id_slot5_time').value

    var slot6_description = document.getElementById('id_slot6_description').value
    var slot6_active = document.getElementById('id_slot6_active').checked
    var slot6_time = document.getElementById('id_slot6_time').value

    $.ajax({
        url : "ajax/submit_cycle_settings/", // the endpoint
        type : "POST", // http method
    headers:{
        "X-CSRFToken": csrftoken
    },
        data : { slot1_description : slot1_description,
                 slot1_active : slot1_active,
                 slot1_time : slot1_time,
                 slot2_description : slot2_description,
                 slot2_active : slot2_active,
                 slot2_time : slot2_time,
                 slot3_description : slot3_description,
                 slot3_active : slot3_active,
                 slot3_time : slot3_time,
                 slot4_description : slot4_description,
                 slot4_active : slot4_active,
                 slot4_time : slot4_time,
                 slot5_description : slot5_description,
                 slot5_active : slot5_active,
                 slot5_time : slot5_time,
                 slot6_description : slot6_description,
                 slot6_active : slot6_active,
                 slot6_time : slot6_time,
                  }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            //$('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("Success"); // another sanity check
            update_messages(json.messages);  // update messages
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
