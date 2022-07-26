function ready(fn) {
    if (document.readyState != 'loading'){
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}
function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
      if ((new Date().getTime() - start) > milliseconds){
        break;
      }
    }
  }
ready(function(){
    
    let $test = document.getElementById("text").innerHTML, $html = '', $i;
    let skip = 0;  
    for ($i = 0; $i < $test.length; $i++) {
        if ($test[$i] == "<"){
            $html += '<br>'
            skip = 3
            continue;
        }
        if (skip){
            skip -= 1
            continue;
        }
        $html += '<span style="animation: rickroll ' + $i + 's">' + ($test[$i]) + '</span>';
    }
    document.getElementById("text").innerHTML = $html;
    function addVanishingAnimation(){
        for (let i = 0; i < $test.length; i++) {
            $test[i].style.animation = 'vanishing 2s forwards';
        }
        $test[12].addEventListener('animationend', () => {
          document.getElementById("text").remove();
          let ricky = document.createElement('img');
          let main = document.getElementById('main');
          let rickWraper = document.getElementById('rick-wraper')
          ricky.id = "ricky";
          ricky.src = "/static/ricky.jpg";
          rickWraper.appendChild(ricky);
          let rickroll = document.createElement('h2')
          rickroll.innerText = "Never gonna give you up :D";
          rickroll.id = 'rickroll'
          main.appendChild(rickroll)
        });
    }
    $test = document.getElementById("text");
    $test = Array.from($test.children);
    $test[12].addEventListener('animationend', addVanishingAnimation);

    
    
});
