function new_session()
{
    $.ajax({
        url: "/backend/session/new?name=" + $("#session_name").val(),
    });
};