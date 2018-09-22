$(document).ready(function () {
  $('img').each(function () {
    if($(this).attr('src')=="None") {
      $(this).attr('src', 'https://octodex.github.com/images/scubatocat.png');
    }
  });
});
