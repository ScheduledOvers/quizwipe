function new_session()
{
    $.ajax({
        url: "/backend/session/new?name=" + $("#session_name").val()
    });
};

function get_player_list()
{
    $.ajax({
        url: "/backend/session/playerlist" + $.now()
    });
};