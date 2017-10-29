function new_session()
{
    $.ajax({
        url: "/backend/session/new?name=" + $("#session_name").val() + "&noquestions=" + $("#noquestions").val(),
        success: function(data)
        {
            if (data["status"] == 0)
            {
                window.location = "/10ft/joining.html?sessionname=" + $("#session_name").val();
            }
        }
    });
};

function get_player_list()
{
    $.ajax({
        url: "/backend/session/playerlist?sessionname=" + sessionname + "&" + $.now()
    });
};

$(document).ready(function() {
    $('select').material_select();
    $("#data-title-sessionname").text(sessionname);
    $("#data-info-sessionname").text(sessionname);
});