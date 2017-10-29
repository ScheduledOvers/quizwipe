function new_session()
{
    if (($("#session_name").val() !== "") && ($("#client_name").val() !== ""))
    {
        $.ajax({
            url: "/backend/client/new?sessionName=" + $("#session_name").val() + "&clientName=" + $("#client_name").val(),
            success: function(data)
            {
                if (data["status"] == 0)
                {
                    window.location = "play?sessionName=" + $("#session_name").val() + "&clientName=" + $("#client_name").val();
                }
                else if (data["status"] == 1)
                {
                    alert("That session could not be found!\n\n(Error Code 1)");
                }
                else if (data["status"] == 2)
                {
                    alert("That player already exists!\n\n(Error Code 2)");
                }
            }
        });
    }
};

function contact_server(button)
{
    $.ajax({
        url: "/backend/client/answer?sessionName=" + sessionname + "&clientName=" + clientname + "&answer=" + button
    });
}

function heartbeat() {
    $.ajax({
        url: "/backend/client/heartbeat?sessionName=" + sessionname + "&clientName=" + clientname
    });
}

$(document).ready(function() {
    $('select').material_select();
    $("#data-title-clientname").text(clientname);
});