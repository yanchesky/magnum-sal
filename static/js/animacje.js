anime.easings['easeOutBounce'] = function(t) {
  if ((t/=1) < (1/2.75)) {
				return 1*(7.5625*t*t);
			} else if (t < (2/2.75)) {
				return 1*(7.5625*(t-=(1.5/2.75))*t + .75);
			} else if (t < (2.5/2.75)) {
				return 1*(7.5625*(t-=(2.25/2.75))*t + .9375);
			} else {
				return 1*(7.5625*(t-=(2.625/2.75))*t + .984375);
			}
}


function minerInAnime(target, delay){
  for(var x of target){
    x.style.visibility = 'hidden';
  };
  anime({
    targets: target,
    translateY: {value:[-50,0],easing:"easeOutBounce"},
    duration: 600,
    delay: function(t,i,tt){return delay + (tt-i)*100},
    loop: false,
    autoplay: true,
    begin: function(){
      for(var x of target){
        x.style.visibility = 'visible'
      }
    },
    complete: function(){
      for(var x of target){
        x.style.transform = ""
      }
    }
  })
}

function minerOutAnime(target){
  anime({
    targets: target,
    translateY: "+=70",
    easing: "easeInCubic",
    duration: 300,
    loop: false,
    autoplay: true,
    complete: function(){target.remove()}
  })
}

function revealMineTileAnime(target){
  anime({
    targets: target,
    rotateY: 0,
    loop: false,
    //duration: 1600,
    autoplay: true
  })
}

function toggleHelperAnime(dane, koord){
  anime({
    targets: dane,
    backgroundPosition: koord+7+'px',
    easing: 'easeOutElastic',
    duration: 800,
    loop: false,
    autoplay: true,
  });
}

function coinAnime(obj){
  let powiekszenieMonety = obj.children[1]
  let obrotMonety = obj.children[1].firstElementChild

  var temp1 = anime({
    targets: obrotMonety,
    rotateY: "+=720",
    duration: 1200,
    easing: "linear",
    loop: false,
    autoplay: true,
  });

  var temp2 = anime({
    targets: powiekszenieMonety,
    scale:3,
    opacity:0,
    duration:1000,
    easing: "linear",
    loop: false,
    autoplay: true,
    complete: function(){
      powiekszenieMonety.style.transform = "scale(0)";
      console.log("Powiększone")
    }
  })
}

function showCoinAnime(obj){

  anime({
    targets: obj,
    scale: 1,
    elasticity: 500,
    loop: false,
    autoplay: true
  })
}

function dropCardsAnime(obj){
	anime({
  	targets: obj,
    scale: [3,1],
  	opacity: [0,1],
  	rotate: {
  		duration: 700,
  		easing: "easeOutSine",
  		value: function() {return Math.random()*6-3}
  	},
  	easing: 'easeOutCubic',
  	duration: 500,
    loop: false,
    delay: function(el, i, l) {
      return i * 150;
    },
    complete: function(){
      if(obj[0].classList.contains("karta-narzedzie")){
        dealToolCardsAnime(obj);
      }else{
        dealRoyalOrdersAnime(obj);
      }


    }
  });
}

function dealToolCardsAnime(obj){

    var narzedziaDoRozdania = obj.slice(-3)
    var narzedziaDoObrotu = []
    for(var x of narzedziaDoRozdania){
      let el = x;
      el.classList.add("narzedzie-klikalne")
      narzedziaDoObrotu.push(x.firstElementChild);
    }
    //var zamowieniaDoRozdania = kartyZamowien.slice(-4)

		anime({
			targets: narzedziaDoRozdania,
			delay:function(target, index, totalTargets){return (totalTargets-index) * 200},
			left: function(target, index, totalTargets){return -104 - index*104},
			easing: 'easeOutExpo',
			duration: 800,
			loop: false,
			autoplay: true,
      begin: function(){
        revealCardsAnime(narzedziaDoObrotu)
      }

		});
    /*
		var rozdanieZamowien = anime({
		targets: zamowieniaDoRozdania,
		delay:function(target, index, totalTargets){return (totalTargets-index) * 100},
		top: 33,
		left: function(target, index, totalTargets){return -70+(totalTargets-index)*104},

		easing: 'easeOutExpo',
		duration: 800,
		loop: false,
		autoplay: true

	});*/
}

function dealRoyalOrdersAnime(obj){

  var zamowieniaDoRozdania = obj.slice(-4)
  var zamowieniaDoObrotu = []
  for(var x of zamowieniaDoRozdania){
    let el = x
    el.classList.add("order-odkryty");
    zamowieniaDoObrotu.push(x.firstElementChild);
  }

  anime({
  targets: zamowieniaDoRozdania,
  delay:function(target, index, totalTargets){return (totalTargets-index) * 100},
  top: 33,
  left: function(target, index, totalTargets){return -25+(totalTargets-index)*104},

  easing: 'easeOutExpo',
  duration: 800,
  loop: false,
  autoplay: true,
  complete: function(){
    revealCardsAnime(zamowieniaDoObrotu);
  }

  });

}

function revealCardsAnime(obj){
	obj.reverse()

    anime({
    	targets: obj,
    	delay:function(target,indeks,totalTargets){return -600 + (indeks * 170)},
    	rotateY:{value:[180,0],easing:"easeInQuart"},
    	duration: 800,
    	loop: false,
    	autoplay: true,
      complete: function(){
        a = document.getElementsByClassName('narzedzie-klikalne');
        Array.from(a).forEach(function(tool){
      		tool.addEventListener("click", drawToolCard);
      	});
      }

    })
  };

function puffCard(dane){
  dane.classList.add("puffing");
  anime({
    targets: dane,
    scale: 3,
    opacity: 0,
    easing: 'easeOutExpo',
    duration: 800,
    loop: false,
    autoplay: true,
    complete: function(){
      dane.remove()
    }
  });
}

function revealNewCard(dane=null, karty, aktywne, delay=0){
  let pozostaleKarty = document.getElementsByClassName(karty)
  let kartaDoOdwrotu;
  if(pozostaleKarty.length > 0){
    kartaDoOdwrotu = [...pozostaleKarty][pozostaleKarty.length-1];
    kartaDoOdwrotu.classList.remove(karty);
    kartaDoOdwrotu.classList.add(aktywne);
    if(dane){
      kartaDoOdwrotu.addEventListener("click", drawToolCard)
      kartaDoOdwrotu = kartaDoOdwrotu.firstElementChild;
      kartaDoOdwrotu.children[1]
        .classList.add(dane);
    }else{
      console.log(kartaDoOdwrotu.firstElementChild);
      kartaDoOdwrotu = kartaDoOdwrotu.firstElementChild

    }

    anime({
      targets: kartaDoOdwrotu,
      easing: "easeOutQuart",
      rotateY:{value:[180,0],easing:"easeOutQuart"},
      duration: 800,
      delay: delay,
      loop: false,
      autplay: true,
    })

  }
}

function moveRestCards(dane, karty, move){
  let kartyDoPrzesuniecia = karty;
  kartyDoPrzesuniecia = [...kartyDoPrzesuniecia].slice(0,dane+1);

  anime({
    targets: kartyDoPrzesuniecia,
    easing: "easeOutQuart",
    left: "+="+move,
    duration: 800,
    loop: false,
    autplay: true,
  })

}

function moveUp(dane){
  anime({
    targets: dane,
    easing: "easeOutQuart",
    top: 33,
    duration: 800,
    loop: false,
    autoplay: true,
  })
}
