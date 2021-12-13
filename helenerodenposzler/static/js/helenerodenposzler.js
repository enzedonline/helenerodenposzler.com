$(document).ready(function(){
    $('a[href^="http://"]').attr('target', '_blank');
    $('a[href^="http://"]').attr('rel', 'nofollow noopener');
    $('a[href^="https://"]').attr('target', '_blank');
    $('a[href^="https://"]').attr('rel', 'nofollow noopener');
    });  