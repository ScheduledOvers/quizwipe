function new_session()
{
    if ($("#session_name").val() !== "")
    {
        $.ajax({
            url: "/backend/session/new?sessionName=" + $("#session_name").val() + "&noquestions=" + $("#noquestions").val(),
            success: function(data)
            {
                if (data["status"] == 0)
                {
                    window.location = "/10ft/joining.html?sessionName=" + $("#session_name").val();
                }
            }
        });
    }
};

function get_player_list()
{
    $.ajax({
        url: "/backend/session/playerlist?sessionName=" + sessionname + "&" + $.now(),
        success: function(data)
        {
            data.sort();
            if (data != playerlist)
            {
                playerlist = data;
                out = "";
                for (player in data)
                {
                    out += "<div class=\"col s3\" style=\"text-align: center;\"><img src=\"https://api.adorable.io/avatars/285/" + playerlist[player] + ".png\" style=\"height: 4em; border-radius: 20%;\"><br><span class=\"title\">" + playerlist[player] + "<br><br></span></div>";
                }
                $("#playerdisplay").html(out);
            }
        }
    });
};

function reveal_list(listitem) {
    if ($("#list-item-" + listitem).text() !== "")
    {
        $("#list-item-" + listitem).removeClass("indigo-text");
        setTimeout(function(){ reveal_list(listitem + 1); }, 3000);
    }
}

$(document).ready(function() {
    $('select').material_select();
    $("#data-title-sessionname").text(sessionname);
    $("#data-info-sessionname").text(sessionname);
});