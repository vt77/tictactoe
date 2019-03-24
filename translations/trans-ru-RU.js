
$( document ).ready(function() {
  // Handler for .ready() called.
  console.log("Переводим на русский");
  MessageStrings['NOT_YOUR_TURN'] = 'Сейчас на ваш ход';
  MessageStrings['ILLEGAL_MOVE'] = 'Неправильный ход';
  MessageStrings['TOP_SCORES']='Лучшие результаты';

 $("#youwin").text("Вы выиграли !");
 $("#youlose").text("Вы проиграли !");
 $("#draw").text("Ничья");
 $("#scorelbl").text('Счёт');

});
