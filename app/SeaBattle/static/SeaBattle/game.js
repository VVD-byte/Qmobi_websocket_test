function printField(data, idtable, color){
    var table = document.getElementById(idtable);
    for (let i = 0; i<table.rows.length; i++){
        for (let j = 0; j<table.rows[i].cells.length; j++){
            table.rows[i].cells[j].bgColor = color[data[i][j]];
        };
    };
};

function writeMessage(message){
     var messageText = document.querySelector('#chat-message-textarea');
     messageText.value += (message + '\n')
}

function writeMove(move, color){
     var table = document.getElementById('rival');
     table.rows[move[0]].cells[move[1]].bgColor = color[move[2]];
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