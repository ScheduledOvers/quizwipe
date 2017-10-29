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

function get_question() {
    $.ajax({
        "url": "/backend/question/new?sessionName=" + sessionname,
        success: function(data) {
            if (status == 0)
            {
                if (data["question"]["type"] == "list")
                {
                    question_count = data["questionCount"];
                    current_question = data["currentQuestion"];
                    question = data["question"];
                    qtext = question["question"];

                    $("body").html('<div class="container"><h1 id="question-text" class="grey-text text-lighten-3"></h1><table class="grey-text text-lighten-4" style="font-size: 2.3rem;"><tr><td id="list-item-0" class="indigo-text"></td><td id="list-item-1" class="indigo-text"></td></tr><tr><td id="list-item-2" class="indigo-text"></td><td id="list-item-3" class="indigo-text"></td></tr><tr><td id="list-item-4" class="indigo-text"></td><td id="list-item-5" class="indigo-text"></td></tr><tr><td id="list-item-6" class="indigo-text"></td><td id="list-item-7" class="indigo-text"></td></tr><tr><td id="list-item-8" class="indigo-text"></td><td id="list-item-9" class="indigo-text"></td></tr></table></div><div class="row"><div class="col s3 card blue" style="min-height: 47vh;"><h3 id="answer-1" class="grey-text text-lighten-2 center"></h3></div><div class="col s3 card orange" style="min-height: 47vh;"><h3 id="answer-2" class="grey-text text-lighten-2 center"></h3></div><div class="col s3 card green" style="min-height: 47vh;"><h3 id="answer-3" class="grey-text text-lighten-2 center"></h3></div><div class="col s3 card yellow" style="min-height: 47vh;"><h3 id="answer-4" class="center"></h3></div></div>');

                    $("#question-text").text(question["question"]);
                    for (var i = question["states"] - 1; i >= 0; i--) {
                        $("#list-item-" + i).text(question["list"][i]);
                    }

                    $("#answer-1").text(question["answer1"]);
                    $("#answer-2").text(question["answer2"]);
                    $("#answer-3").text(question["answer3"]);
                    $("#answer-4").text(question["answer4"]);

                    reveal_list(0);
                    setTimeout(get_results, 30000);
                }
                else if (data["question"]["type"] == "question")
                {
                    question_count = data["questionCount"];
                    current_question = data["currentQuestion"];
                    question = data["question"];
                    qtext = question["question"][question["question"].length - 1];

                    $("body").html('<div class="container"><h1 id="question-text" class="grey-text text-lighten-3"></h1><br><br><br><br><br><br></div><div class="row"><div class="col s3 card blue" style="min-height: 47vh;"><h3 id="answer-1" class="grey-text text-lighten-2 center"></h3></div><div class="col s3 card orange" style="min-height: 47vh;"><h3 id="answer-2" class="grey-text text-lighten-2 center"></h3></div><div class="col s3 card green" style="min-height: 47vh;"><h3 id="answer-3" class="grey-text text-lighten-2 center"></h3></div><div class="col s3 card yellow" style="min-height: 47vh;"><h3 id="answer-4" class="center"></h3></div></div>');

                    $("#question-text").text(question["question"][0]);

                    $("#answer-1").text(question["answer1"]);
                    $("#answer-2").text(question["answer2"]);
                    $("#answer-3").text(question["answer3"]);
                    $("#answer-4").text(question["answer4"]);

                    reveal_questionstages(0, question["stages"]);
                    setTimeout(get_results, 30000);
                }
            }
            else if (status == 2)
            {

            }
        }
    })
}

function get_results() {
    $.ajax({
        "url": "/backend/question/results?sessionName=" + sessionname,
        success: function(data) {
            if (data["status"] == 0)
            {
                out = '<div class="container"><h1 id="question-text" class="grey-text text-lighten-3">' + qtext + '</h1><h3>Correct answer: <span id="correct">' + question["answer" + question["solution"]] + '</span></h3><br><br><ul class="collection">'
                if (data["results"][0]["result"] > 0)
                {
                    out += '<li class="collection-item avatar"><img src="https://api.adorable.io/avatars/285/' + data["results"][0]["player"] + '.png" alt="" class="circle"><span class="title">' + data["results"][0]["player"] + '</span><p>Fastest Player</p></li>'
                    if (data["results"][1]["result"] > 0)
                    {
                        out += '<li class="collection-item avatar"><img src="https://api.adorable.io/avatars/285/' + data["results"][1]["player"] + '.png" alt="" class="circle"><span class="title">' + data["results"][1]["player"] + '</span><p>Second Fastest Player</p></li>'
                        if (data["results"][2]["result"] > 0)
                        {
                            out += '<li class="collection-item avatar"><img src="https://api.adorable.io/avatars/285/' + data["results"][2]["player"] + '.png" alt="" class="circle"><span class="title">' + data["results"][2]["player"] + '</span><p>Third Fastest Player</p></li>'
                        }
                    }
                }
                out += '</ul>'
                $("body").html(out);
            }
        }
    });
}

function reveal_list(listitem) {
    if ($("#list-item-" + listitem).text() !== "")
    {
        $("#list-item-" + listitem).removeClass("indigo-text");
        setTimeout(function(){ reveal_list(listitem + 1); }, 3000);
    }
}

function reveal_questionstages(stagenum, max_stages) {
    if (stagenum !== max_stages)
    {
        $("#question-text").text(question["question"][stagenum]);
        setTimeout(function(){ reveal_questionstages(stagenum + 1, max_stages); }, 9000);
    }
}

$(document).ready(function() {
    $('select').material_select();
    $("#data-title-sessionname").text(sessionname);
    $("#data-info-sessionname").text(sessionname);
});