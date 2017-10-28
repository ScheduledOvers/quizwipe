function new_session()
{
    $.ajax({
        url: "/backend/session/new?name=" + $("#session_name").val(),
        success: function(data)
        {
            if (data["status"] == 0)
            {
                window.location = "/joining.html?sessionname=" + $("#session_name").val() + "&noquestions=" + $("#noquestions").val();
            }
        }
    });
};

function get_player_list()
{
    $.ajax({
        url: "/backend/session/playerlist" + $.now()
    });
};

$(document).ready(function() {
    $('select').material_select();
});