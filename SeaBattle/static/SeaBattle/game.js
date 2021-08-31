function printField(data, idtable, color){
    var table = document.getElementById(idtable);
    for (let i = 0; i<table.rows.length; i++){
        for (let j = 0; j<table.rows[i].cells.length; j++){
            table.rows[i].cells[j].bgColor = color[data[i][j]];
        };
    };
};

function writeField(data){
     if (data[0] != false && data[1] != false){
        input_move_disable_unable();
        rewriteStyleTable('rival', 'tdr');
        rewriteStyleTable('you', '');
     }
}

function input_move_disable_unable(){
    var input_batton = document.querySelector('#input_move');
    if (input_batton.disabled == true){
        input_batton.disabled = false;
    }
    else {
        input_batton.disabled = true;
    }
}

function rewriteStyleTable(idtable, tag){
    var table = document.getElementById(idtable);
    console.log(table, idtable);
    for (let i = 0; i<table.rows.length; i++){
        for (let j = 0; j<table.rows[i].cells.length; j++){
            table.rows[i].cells[j].classList.value=tag
        };
    };
}

function writeMessage(message){
     var messageText = document.querySelector('#chat-message-textarea');
     messageText.value += (message + '\n')
}

function writeMove(move, color){
    if (move[3] == user_id){
        var table = document.getElementById('rival');
        table.rows[move[0]].cells[move[1]].bgColor = color[move[2]];
        RivalField[move[0]][move[1]] = move[2];
    }
    else{
        var table = document.getElementById('you');
        table.rows[move[0]].cells[move[1]].bgColor = color[move[2]];
        YouField[move[0]][move[1]] = move[2];
    }
}

$(function(){
        $('.td').click(function(){
            if (YouField[$(this).closest('tr').index()][$(this).index()] == 0){
                YouField[$(this).closest('tr').index()][$(this).index()] = 3;
                this.bgColor = color[3];
            }
            else if (YouField[$(this).closest('tr').index()][$(this).index()] == 3){
                YouField[$(this).closest('tr').index()][$(this).index()] = 0;
                this.bgColor = color[0];
            }
        });
    });

function tdr(){
    $('.tdr').click(function(){
        if (move == null){
            if (RivalField[$(this).closest('tr').index()][$(this).index()] == 0){
                RivalField[$(this).closest('tr').index()][$(this).index()] = 3;
                this.bgColor = color[3];
                move = [$(this).closest('tr').index(), $(this).index()]
            }
        }
        else if ([$(this).closest('tr').index(), $(this).index()].join() == move.join()){
            RivalField[$(this).closest('tr').index()][$(this).index()] = 0;
            this.bgColor = color[0];
            move = null;
        }
       });
};
