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

function godzinka() {
  var g = new Date();
  var godzina = g.getHours();
  var minuta = g.getMinutes();
  var sekunda = g.getSeconds();

  if (godzina<10){
    godzina = "0"+godzina
  }
  if (minuta<10){
    minuta = "0"+minuta
  }
  if (sekunda<10){
    sekunda = "0"+sekunda
  }

  return godzina + ":"+minuta+":"+sekunda;

}

function feedback_info(x){
  if(x.log){
    var y = godzinka()
    let oknoDziennikGry = document.getElementById("okno-dziennik-gry");

    let wpis = document.createElement("div");
    wpis.classList.add("wpis");
    wpis.innerHTML += "<div class='czas'>"+y+"</div><div class='cialo'>"+x.log+"</div>";
    oknoDziennikGry.prepend(wpis);
  }
  if(x.oknoGracza){
    let oknoInfoGracza = document.getElementById("cialo-info-gracza");
    let playerTools = document.getElementById("narzedzia-gracza").firstElementChild;

    while(oknoInfoGracza.firstChild){
      oknoInfoGracza.removeChild(oknoInfoGracza.firstChild)
    }

    oknoInfoGracza.innerHTML = x.oknoGracza;
    playerTools.addEventListener("mousemove", slideTools);

    const glejty = document.querySelectorAll('#narzedzia-gracza > div .glejtkrolewski, .glejthandlowy');
    glejty.forEach(function(glejt){
  		console.log(glejt);
  		if(!glejt.classList.contains("uzyte-narzedzie")){
  			glejt.addEventListener("click", toggleNarzedzie);
  		}
  	});

  }
  if(x.alrt){
    if(x.alrt == 1){
    alert(x.log)
    }
    if(x.alrt == 2){
      alert("Wykorzystałeś już swoje akcje")
    }
    if(x.alrt == 3){
      alert("Korzystałeś już z tego budynku")
    }
    if(x.alrt == 4){
      alert("Bląd z synchronizacją danych")
    }
  }
}

function setEventListeners(){
  let przyciski = [...document.getElementsByClassName("przycisk")];
  let narzedzia = [...document.getElementsByClassName("narzedzie-modal")];
  let kostkiSoli = [...document.getElementsByClassName("solBox")];
  let kostkiWody = [...document.getElementsByClassName("wodaBox")];


  przyciski.forEach(function(przycisk){
    przycisk.addEventListener("click", executeModal);
  });
  narzedzia.forEach(function(narzedzie){
    narzedzie.addEventListener("click", toggleNarzedzie)
  });

  kostkiSoli.forEach(function(kostka){
    kostka.addEventListener("change", toggleGornik);
  });

  kostkiWody.forEach(function(woda){
    woda.addEventListener("change", pokazCeneWydobyciaWody)
  });

  document.addEventListener("click", function mod(e){
    const modal = document.getElementById("kopalnia-modal")
    if(e.target==modal){
      schowajModal("kopalnia-modal");
      window.removeEventListener("click", mod)
    }
  })


}

function pokazCeneWydobyciaWody(){
  let zaznaczone = document.querySelectorAll('.wodaBox[type="checkbox"]:checked').length;
  let cena = document.getElementById("koszt-wydobycia-wody");

  cena.style.backgroundPosition = (-33*zaznaczone)-841+"px";
}

function toggleNarzedzie(e){
  let klasy = e.currentTarget.classList;
  let aktywneNarzedzie = 'aktywne-modal';
  let chleb = 'prowiant';
  let czerpak = 'czerpak';

  if(klasy.contains("narzedzie-inwentarz")){
    aktywneNarzedzie = 'aktywne-inwentarz'
  }

  if(klasy.contains(aktywneNarzedzie)){
    klasy.remove(aktywneNarzedzie);
    globalObject.usunNarzedzie(e.currentTarget)
    if(klasy.contains("czerpak") || klasy.contains("prowiant")){
      e.currentTarget.firstElementChild.style.display = "none"
    };

  }else{
    klasy.add(aktywneNarzedzie);
    globalObject.dodajNarzedzie(e.currentTarget)
    if(klasy.contains("czerpak") || klasy.contains("prowiant")){
      let target = e.currentTarget.firstElementChild;
      target.style.display = "block";
      [...target.children].forEach(function(x){
        x.addEventListener("click", executeUkryte);
      })

    };
  }

  console.log(globalObject.aktywneNarzedzia.wartosci)

}

function toggleGornik(){
  let zaznaczone = document.querySelectorAll('.solBox[type="checkbox"]:checked').length
  let woda = globalObject.modal.czytajZaznaczone("wodaBox");
  console.log(woda)
  let aktywniGornicy = document.querySelectorAll(".wymagany-gornik");
  aktywniGornicy.forEach(function(e){
    e.classList.remove("wymagany-gornik");
    console.log(e.classList)
  })

  let kilofy = globalObject.policzNarzedzie("kilof");

  let total = zaznaczone+woda-kilofy;

  if(zaznaczone>0 && total<=globalObject.modal.gornicy.length){
    for(var i=0;i<total;i++){
      console.log(i);
      globalObject.modal.gornicy[i].classList.add("wymagany-gornik")
    }
  } else if(total>globalObject.modal.gornicy.length){
   alert("Brak wystarczająco siły wydobywczej");
  }
}

function executeModal(e){
  let przyciski = document.getElementsByClassName("przycisk");
  let listaKostekModal = [];
  let listaKostekTarget = [];
  let narzedzia = [];
  let indeks = [...przyciski].indexOf(e.currentTarget);

  if(indeks===0){
    listaKostekModal = czytajZaznaczone("solBox");
    listaKostekKomnata = globalObject.kopalnia.kostkiSoli.children;
  };
  if(indeks===3){
    listaKostekModal = czytajZaznaczone("wodaBox");
    listaKostekKomnata = globalObject.kopalnia.kostkiWody.children;
  }
  console.log(globalObject.kopalnia.indeksKomnaty)

  $.getJSON("/modal",{
    a: indeks,
		b: JSON.stringify(listaKostekModal.wartosci),
		c: JSON.stringify(globalObject.aktywneNarzedzia.wartosci)
  }, function(data){

    feedback_info(data);

    let zipHolderModal = document.getElementById("gornicy-gracza-modal")

    if(data.wstawiam){
      let liny = globalObject.policzNarzedzie("lina")

      let obj = zipFunc()

      globalObject.kopalnia.wstawZipka(obj.kopalnia);

      globalObject.modal.wstawZipka(obj.modal);

      function zipFunc(){
        let x = [];
        let z = []

        for(var i=0;i<=liny;i++){
          let a = document.createElement("div")
          a.className = 'gornik';
          a.classList.add("pionek"+data.lpGracza);
          let b = a.cloneNode(true);
          x.push(a);
          z.push(b);
        }
        return {kopalnia:x,modal:z}
      }



    }

    if(data.zabieram){
      globalObject.kopalnia.usunZipka();
      globalObject.modal.usunZipka();
    }

    if(data.wydobywam){

      for(let x of listaKostekModal.obiekty){
        x.remove();
        klasa = x.getAttribute("value")
        for(let y of listaKostekKomnata){
          if(y.classList.contains("rd"+klasa)){
            y.remove()
            break
          }
        }
        pokazCeneWydobyciaWody()
      }
    }

    if(indeks===0){
      schowajModal("kopalnia-modal");
      let i=0;

      for(let j of globalObject.aktywneNarzedzia.wartosci){
        if(j=="kilof"){
          i++
        }
      }

      globalObject.modal.zmeczZipka(listaKostekModal.obiekty.length,i)
      globalObject.kopalnia.zmeczZipka(listaKostekModal.obiekty.length,i)
    }

    globalObject.resetActiveTools();

  });


  function czytajZaznaczone(e){
    let listaObiektow = [];
    let listaWartosci = [];
    let boksy = document.getElementsByClassName(e);
    [...boksy].forEach(function(element){
      if(element.checked){
        listaObiektow.push(element);
        listaWartosci.push(element.value);
      }
    });
    return {obiekty:listaObiektow, wartosci:listaWartosci}
  }

}

function uwidocznijModal(x){
  let modal = document.getElementById(x);
  modal.style.display = "block";
}

function schowajModal(x){
  let modal = document.getElementById(x);
  modal.style.display = "none";
}

function odkryjKomnate(e){
	let komnaty = document.getElementsByClassName("komnata");
	clickKomnata(e.target, [...komnaty].indexOf(e.currentTarget));
}

function otworzModal(e){
	let komnaty = document.getElementsByClassName("komnata");
	let indeks = [...komnaty].indexOf(e.currentTarget);
	console.log("Indeks: ", indeks)

	globalObject.kopalnia.initialize(e.currentTarget, indeks)

	renderModal(indeks)
}

function slideTools(e){
  if(e.currentTarget.children.length > 4){
    const szerNarz = e.currentTarget.children.length*60;
    const szerOkn = 230;
    let pozycjaMyszki = $(window).width()-e.clientX-35;
    let procentOkna = -(pozycjaMyszki/szerOkn)+1
    e.target.parentNode.style.right = (szerNarz-szerOkn)*procentOkna+"px"
  }
}

function beggaryAndZiphouse(dane){
	console.log("beggaryAndZiphouse executed")
	console.log(dane.id)
	$.getJSON("/"+dane.id,{a:dane.id}, function(data){
		feedback_info(data);
    if(data.zipek){
      przesunGorneInfo("wykupieni-gornicy", data.zipek);
    }

	});

}

function togglePomocnik(e){
  let stanowiska = [...document.getElementsByClassName("pomocnik")];
  let indeks = stanowiska.indexOf(e.currentTarget);

  $.getJSON("/helper",{a:indeks},function(data){
    if(data.oknoGracza){
      feedback_info(data)
    }
    if(data.wstawiam){
      console.log(e.target.parentNode)
      togglePomocnikAnimation(e.target.parentNode, data.gracz);
    }
  });
}

function drawToolCard(dane){
  console.log("drawToolCard executed")
  let a = document.getElementsByClassName('narzedzie-klikalne')
  let x = [...a].indexOf(dane.currentTarget);
  let index = a.length-x-1

  let kliknietaKarta = dane.currentTarget
  console.log(kliknietaKarta)
	$.getJSON("/karty-narzedzi",{a:index}, function(data){
		feedback_info(data);
    if(data.narzedzie){
      puffCard(kliknietaKarta)
      if(data.narzedzie!="puste"){
        revealNewCard(data.narzedzie, "zakryta", "narzedzie-klikalne");
        moveRestCards(x, a, "-104");
      }else{
        moveRestCards(x-1, a, "-104")
      }
    }
	});

}

function buySellTarg(targowisko, indeks){

	$.getJSON("/targ", {
	a: indeks,
	b: JSON.stringify(globalObject.aktywneNarzedzia.wartosci),
	},
	function(data){
      feedback_info(data);

			if(data.zmiennaJSON != null){
        let target = targowisko[data.zmiennaJSON]
        if(target.firstElementChild.classList.contains("wykupione")){
          target.firstElementChild.classList.remove("wykupione");
        }else{
          target.firstElementChild.classList.add("wykupione")
        }
      }
			if(data.kolejka==true){
				spadajacyZipekWSzybie($('.queueTwo .zipster').get(-1));
			}
		}
	);
}

function clickSzyb(target, indeks){

  $.getJSON('/shaftHolder',{a:indeks}, function(data){
    feedback_info(data);

    var holder = target.firstElementChild;
    let obecnyGracz = document.getElementById("imie-gracza");
    let id = obecnyGracz.firstElementChild.getAttribute("value");
    console.log([...holder.children])
    if(!data.zabiera && !data.alrt == 1){
      stworzZipka(holder, id)
      console.log("Wstawiony")
    }
    if(data.zabiera){
      console.log("Zabrany", id);
      [...holder.children].forEach(function(child){
        if(child.classList.contains(id)){
          zipekOut(child)

        }
      })
    }



  });
}

function stworzZipka(target, pionek){
  let a = document.createElement("div")
  a.className = 'gornik'
  a.classList.add(pionek)
  target.append(a)
  zipekIn([target.lastElementChild],0);
}

function clickKomnata(target, indeks){

  $.getJSON('/roomHolder',{a:indeks},function(data){

    feedback_info(data);

    if(data.odkrywam){
      const komnata = target.parentNode.parentNode;

      komnata.classList.remove("zakryte");
      komnata.classList.add("odkryte");


      let kafelek = target.nextElementSibling;
      kafelek.classList.add(data.tlo)

      var kostkiSoli = document.createElement("div");
      kostkiSoli.className = "matsy-kopalnia"

      for(var i in data.kostkiSoli){
        for(var j = 0; j<data.kostkiSoli[i];j++){
          kostkiSoli.innerHTML += "<div class=\"kostka-soli rd"+i+"\"></div>"
        }
      }

      var zipHolder = document.createElement("div");
      zipHolder.className = "gornicy-kopalnia"
      zipHolder.innerHTML = "<div class=\"gornik pionek"+data.lpGracza+"\"></div>"

      var woda = document.createElement("div");
      woda.className = "woda-kopalnia"

      for(var i=0;i<data.woda;i++){
        woda.innerHTML += "<div class=\"kostka-soli rd3\"></div>"
      }

      console.log(data.kostkiSoli);

      kafelek.appendChild(kostkiSoli);
      kafelek.appendChild(zipHolder);
      kafelek.appendChild(woda);

      zipekIn([zipHolder],1500);
      odkryjKafelek(target.parentNode);
      target.parentNode.parentNode.removeEventListener("click", odkryjKomnate)
      target.parentNode.parentNode.addEventListener("click", otworzModal)

    }


  })
}

function renderModal(indeks){

  console.log("Indeks w render modal:", indeks)
  $.getJSON("/render_modal",{a:indeks}, function(data){
    //console.log(data.modal)
    uwidocznijModal('kopalnia-modal');

  	var okn = document.getElementById('cialo-modal-kopalnia');

    while(okn.firstChild){
      okn.removeChild(okn.firstChild)
    }


    let zaznaczoneKostki = []
  	let zaznaczonaWoda = 1

    let cialko = document.createElement("div");
    cialko.id = "wnetrze-modal-kopalnia";
    cialko.innerHTML = data.modal;

    okn.appendChild(cialko);

    setEventListeners();

    globalObject.modal.initialize(cialko, indeks);



  })

}

function executeUkryte(e){
  const aktualnaKomnata = globalObject.kopalnia.aktualnaKomnata;
  const komnaty = globalObject.kopalnia.aktualnaKomnata.parentNode;
  const odkryteKomnaty = [...komnaty.getElementsByClassName("odkryte")];
  const wszystkieKomnaty = [...komnaty.children];
  const indeksKomnaty = wszystkieKomnaty.indexOf(aktualnaKomnata);
  console.log(e);
  //e.target.style.display = "none"
  e.target.parentNode.classList.remove("activeTool");
  e.target.parentNode.classList.add("uzyte-narzedzie");

  $.getJSON('/miscTool',{a:e.currentTarget.id}, function(data){
    if(data.czerpak){

      const wodaKomnata = aktualnaKomnata.querySelector(".rd3")
      const wodaModal = document.querySelector("#wydobycie-wody-modal .kostka-checkbox")
      const narzedzia = document.querySelectorAll(".narzedzie-inwentarz.czerpak, .narzedzie-modal.czerpak")

      wodaKomnata.remove();
      wodaModal.remove();

      let woda = document.createElement("div");
      woda.className = "kostka-soli rd3";


      if(data.czerpak == "moveForward"){
        if(indeksKomnaty<odkryteKomnaty.length-1){
          console.log("Można przesunac dalej");
          const holderWoda = wszystkieKomnaty[indeksKomnaty+1].querySelector(".woda-kopalnia");
          holderWoda.append(woda);
        }
      }
      if(data.czerpak == "moveBackward"){
        const holderWoda = wszystkieKomnaty[indeksKomnaty-1].querySelector(".woda-kopalnia");
        holderWoda.append(woda);
      }

      for(let narzedzie of narzedzia){
        if (!narzedzie.classList.contains("uzyte-narzedzie")){
          narzedzie.classList.add("uzyte-narzedzie");
          break;
        }
      }
    }

    if(data.chleb){
      let obecnyGracz = document.getElementById("imie-gracza");
      let id = obecnyGracz.firstElementChild.getAttribute("value");
      const narzedzia = document.querySelectorAll(".narzedzie-inwentarz.prowiant, .narzedzie-modal.prowiant")

      const zmeczeni = [...aktualnaKomnata.querySelectorAll(".zmeczony")];
      const zmeczeniModal = [...document.querySelectorAll("#gornicy-gracza-modal .zmeczony")];

      zmeczeni.reverse();
      zmeczeniModal.reverse();

      let i = 0;
      for(let zmeczony of zmeczeniModal){
        if(i < 2 && zmeczony.classList.contains(id)){
          zmeczony.classList.remove("zmeczony")
          i++
        }
      }

      i = 0;
      for(let zmeczony of zmeczeni){
        if(zmeczony.classList.contains(id) && i < 2){
          zmeczony.classList.remove("zmeczony")
          i++
        }
      }

      for(let narzedzie of narzedzia){
        narzedzie.classList.add("uzyte-narzedzie")
      }
    }

  });
}

function wstawDoKolejki(e){
  const narzedzia = globalObject.aktywneNarzedzia;
  const stanowiskaKolejki = [...document.getElementsByClassName("kolejka-do-zamku")];
  console.log(narzedzia)
  $.getJSON("/queue", {a:JSON.stringify(narzedzia.wartosci)}, function(data){
    feedback_info(data);
    if(data.lpGracza){
      let holder;
      if(data.glejt){
        holder = stanowiskaKolejki[0];
        for(let x of narzedzia.obiekty){
          if(x.getAttribute("value") == "glejtkrolewski"){
            console.log("Wygaszam")
            x.classList.remove("aktywne-inwentarz")
            x.classList.add("uzyte-narzedzie")
            x.removeEventListener("click", toggleNarzedzie);

            globalObject.usunNarzedzie(x)

          }
        }

      }else{
        holder = stanowiskaKolejki[1];
      }
      const pionek = 'pionek'+data.lpGracza;
      stworzZipka(holder, pionek)
    }



  })
}

function zrealizujZamowienie(e){
  var zamowieniaModal = [...document.querySelectorAll("#wnetrze-modal-zamowienia .karta-zamowienie")];
  var zamowieniaBoard = [...document.getElementsByClassName("order-odkryty")]

  var absIndeks = zamowieniaModal.indexOf(e.currentTarget)
  var indeks = zamowieniaModal.length-absIndeks-1;

  $.getJSON("/zamowieniaKrolewskie", {a:indeks},function(data){
    if(data.realizujeZamowienie){
      feedback_info(data);
      zamowieniaModal[absIndeks].remove();
      puffCard(zamowieniaBoard[absIndeks]);

      let cialko = document.getElementById("wnetrze-modal-zamowienia")
      let nowaKarta = document.createElement("div");
      nowaKarta.className = "karta-zamowienie";
      nowaKarta.innerHTML += data.nowaKarta;
      nowaKarta.addEventListener("click", zrealizujZamowienie);
      cialko.prepend(nowaKarta);

      moveRestCards(absIndeks, zamowieniaBoard, "-104")

      let kartyZamowien = document.querySelectorAll(".order-zakryty");
      let wierzchniaKarta = kartyZamowien[kartyZamowien.length-1]
      wierzchniaKarta.innerHTML = data.nowaKarta;

      revealNewCard(null, "order-zakryty", "order-odkryty", 800);
      moveUp(wierzchniaKarta);

      przesunGorneInfo("zrealizowane-zamowienia", data.zrealizowanychZamowien);



      if(data.doRealizacji == 0){
        schowajModal("zamowienia-modal");
      }
    }else{
      feedback_info(data);
      schowajModal("zamowienia-modal")
    }

  })


}

function zakonczTure(e){
  $.getJSON("/endturn",{},function(data){
    schowajModal("kopalnia-modal");
    const kolejka = document.getElementById("droga-do-zamku")
    kolejka.innerHTML = data.que;

		feedback_info(data);

    if(data.realizujeZamowienie){
      uwidocznijModal("zamowienia-modal");
      let zamowienia = [...document.querySelectorAll("#wnetrze-modal-zamowienia .karta-zamowienie")];
      zamowienia.forEach(function(zamowienie){
        zamowienie.addEventListener("click", zrealizujZamowienie)
      })
    }

    if(data.odpoczywa){
      let pion = "pionek"+data.odpoczywa
      let wszyscyZmeczeni = [...document.getElementsByClassName("zmeczony")]
      for(let x of wszyscyZmeczeni){
        if(x.classList.contains(pion)){
          x.classList.remove("zmeczony")
        }
      }
    }
  })
}

function przesunGorneInfo(idElementu, indeks){
  let pozycje = document.getElementById(idElementu)
  pozycje = [...pozycje.children]

  if(indeks < pozycje.length){
    pozycje[indeks].classList.add("highlighted")
  }
  pozycje[indeks-1].classList.remove("highlighted")
}
