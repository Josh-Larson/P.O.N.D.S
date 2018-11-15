// ===========ANIMATION CODE===================
var west_ctrl_Animation;   //---onload:  west_ctrl_Animation=SVG.adopt(pipe)  ---
var east_ctrl_Animation;

//Handles the arrows moving around the pipe. 
function runArrows(ctrl) {
    var duration = 4000
        var rotateAngle = 360
        var pipe = window[ctrl + "_pipe"];
        var pathLength = pipe.getTotalLength() - 25
        var arrow2Offset = pipe.getTotalLength() * .33

        window[ctrl + "_Animation"].animate(duration).during(
            function (pos) //---setter--
            {
                var length = pathLength * pos
                var Pnt0 = pipe.getPointAtLength(length) //--start
                var Pnt1 = pipe.getPointAtLength(length + 20) //--mid---
                var Pnt2 = pipe.getPointAtLength(length + 40) //---end---
                var d = "M" + [Pnt0.x, Pnt0.y, Pnt1.x, Pnt1.y, Pnt2.x, Pnt2.y].toString()
                window[ctrl + "_arrowLine1"].setAttribute("d", d)

                if (length <= (pathLength - arrow2Offset)) {
                    var Pnt0 = pipe.getPointAtLength(length + arrow2Offset) //--start
                    var Pnt1 = pipe.getPointAtLength(length + 20 + arrow2Offset) //--mid---
                    var Pnt2 = pipe.getPointAtLength(length + 40 + arrow2Offset) //---end---
                    var d = "M" + [Pnt0.x, Pnt0.y, Pnt1.x, Pnt1.y, Pnt2.x, Pnt2.y].toString()
                    window[ctrl + "_arrowLine2"].setAttribute("d", d)
                }
                else if (length > (pathLength - arrow2Offset)) {
                    var myLength = length - arrow2Offset
                    var Pnt0 = pipe.getPointAtLength(myLength - arrow2Offset) //--start
                    var Pnt1 = pipe.getPointAtLength(myLength + 20 - arrow2Offset) //--mid---
                    var Pnt2 = pipe.getPointAtLength(myLength + 40 - arrow2Offset) //---end---
                    var d = "M" + [Pnt0.x, Pnt0.y, Pnt1.x, Pnt1.y, Pnt2.x, Pnt2.y].toString()
                    window[ctrl + "_arrowLine2"].setAttribute("d", d)
                }
            })
            .after(function () {
                runArrows(ctrl)
            })
    }

    function updateAnimation(status) {
        status["east_ctrl"] = status["pondPiEast"];
        status["west_ctrl"] = status["pondPiWest"];

        ["east_ctrl", "west_ctrl"].forEach((pond) => {
            switch (status[pond]) {
                case "True":
                    window[pond + "_Animation"].play()
                    document.getElementById(pond).innerHTML = "Stop Pump"
                    window[pond + "_shape4"].setAttribute("fill", "white")
                    window[pond + "_shape8"].setAttribute("fill", "white")
                    window[pond + "_shape10"].setAttribute("fill", "white")
                    window[pond + "_shape11"].setAttribute("fill", "white")
                    window[pond + "_pipe"].setAttribute("stroke", "#7CFC00")
                    break;
                default:
                    window[pond + "_Animation"].pause()
                    document.getElementById(pond).innerHTML = "Start Pump"
                    window[pond + "_shape4"].setAttribute("fill", "crimson")
                    window[pond + "_shape8"].setAttribute("fill", "crimson")
                    window[pond + "_shape10"].setAttribute("fill", "crimson")
                    window[pond + "_shape11"].setAttribute("fill", "crimson")
                    window[pond + "_pipe"].setAttribute("stroke", "#ff4500")
             }
        });
    }


document.addEventListener("onload", init(), false);
    function init() {
       west_ctrl_Animation = SVG.adopt(west_ctrl_pipe);
       east_ctrl_Animation = SVG.adopt(east_ctrl_pipe);
       for (const btn of document.getElementsByClassName("pausebtn")) {
            runArrows(btn.id);
        }
        updateAnimation({ "pondPiEast": "False", "pondPiWest": "False" });
    }
