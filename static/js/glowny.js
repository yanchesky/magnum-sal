function actionTime() {
  const g = new Date();
  let godzina = g.getHours();
  let minuta = g.getMinutes();
  let sekunda = g.getSeconds();

  if (godzina<10){
    godzina = "0"+godzina
  }
  if (minuta<10){
    minuta = "0"+minuta
  }
  if (sekunda<10){
    sekunda = "0"+sekunda
  }

  return godzina +":"+ minuta +":"+ sekunda;
}

function gameLog(x){
  if(x.log){
    const obecnyCzas = actionTime()
    const oknoDziennikGry = document.getElementById("okno-dziennik-gry");

    let wpis = document.createElement("div");
    wpis.classList.add("wpis");
    wpis.innerHTML += "<div class='czas'>"+obecnyCzas+"</div><div class='cialo'>"+x.log+"</div>";
    oknoDziennikGry.prepend(wpis);
  }
  if(x.oknoGracza){
    const oknoInfoGracza = document.getElementById("cialo-info-gracza");
    const narzedziaGracza = document.getElementById("narzedzia-gracza").firstElementChild;

    while(oknoInfoGracza.firstChild){
      oknoInfoGracza.removeChild(oknoInfoGracza.firstChild)
    }

    oknoInfoGracza.innerHTML = x.oknoGracza;
    narzedziaGracza.addEventListener("mousemove", slideTools);

    const glejty = document.querySelectorAll('#narzedzia-gracza > div .glejtkrolewski, #narzedzia-gracza > div .glejthandlowy');
    glejty.forEach(function(glejt){
  		console.log(glejt);
  		if(!glejt.classList.contains("uzyte-narzedzie")){
  			glejt.addEventListener("click", toggleTool);
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
  const przyciski = [...document.getElementsByClassName("przycisk")];
  const narzedzia = [...document.getElementsByClassName("narzedzie-modal")];
  const kostkiSoli = [...document.getElementsByClassName("solBox")];
  const kostkiWody = [...document.getElementsByClassName("wodaBox")];
  const przyciskZamkniecia = document.getElementById("zamknij-button")


  przyciski.forEach(function(przycisk){
    przycisk.addEventListener("click", executeModal);
  });
  narzedzia.forEach(function(narzedzie){
    narzedzie.addEventListener("click", toggleTool)
  });

  kostkiSoli.forEach(function(kostka){
    kostka.addEventListener("change", toggleMiner);
  });

  kostkiWody.forEach(function(woda){
    woda.addEventListener("change", showWaterPumpPrice)
  });

  przyciskZamkniecia.addEventListener("click", function(){hideModal("kopalnia-modal")});

  document.addEventListener("click", function mod(e){
    const modal = document.getElementById("kopalnia-modal")
    if(e.target==modal){
      hideModal("kopalnia-modal");
      window.removeEventListener("click", mod)
    }
  })


}

function showWaterPumpPrice(){
  let zaznaczone = document.querySelectorAll('.wodaBox[type="checkbox"]:checked').length;
  let cena = document.getElementById("koszt-wydobycia-wody");

  cena.style.backgroundPosition = (-33*zaznaczone)-841+"px";
}

function toggleTool(e){
  let klasy = e.currentTarget.classList;
  let aktywneNarzedzie = 'aktywne-modal';
  const chleb = 'prowiant';
  const czerpak = 'czerpak';

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
      [...target.children].forEach(function(schowaneNarzedzia){
        schowaneNarzedzia.addEventListener("click", executeHidden);
      })

    };
  }

  console.log(globalObject.aktywneNarzedzia.wartosci)

}

function toggleMiner(){
  const zaznaczone = document.querySelectorAll('.solBox[type="checkbox"]:checked').length
  const woda = globalObject.modal.czytajZaznaczone("wodaBox");
  const aktywniGornicy = document.querySelectorAll(".wymagany-gornik");
  aktywniGornicy.forEach(function(e){
    e.classList.remove("wymagany-gornik");
  })

  const kilofy = globalObject.policzNarzedzie("kilof");
  const total = zaznaczone+woda-kilofy;

  if(zaznaczone>0 && total<=globalObject.modal.gornicy.length){
    for(let i=0;i<total;i++){
      console.log(i);
      globalObject.modal.gornicy[i].classList.add("wymagany-gornik")
    }
  } else if(total>globalObject.modal.gornicy.length){
   alert("Nie wystarczająco siły wydobywczej. Wstaw górnika lub użyj kilofa");
  }
}

function executeModal(e){
  const przyciski = [...document.getElementsByClassName("przycisk")];
  let listaKostekModal = [];
  let listaKostekTarget = [];
  let narzedzia = [];
  const indeks = przyciski.indexOf(e.currentTarget);

  if(indeks===0){
    listaKostekModal = czytajZaznaczone("solBox");
    listaKostekKomnata = globalObject.kopalnia.kostkiSoli.children;
  };
  if(indeks===3){
    listaKostekModal = czytajZaznaczone("wodaBox");
    listaKostekKomnata = globalObject.kopalnia.kostkiWody.children;
  }

  $.getJSON("/modal",{
    a: indeks,
		b: JSON.stringify(listaKostekModal.wartosci),
		c: JSON.stringify(globalObject.aktywneNarzedzia.wartosci)
  }, function(data){

    gameLog(data);

    if(data.wstawiam){
      const liny = globalObject.policzNarzedzie("lina")

      const obj = zipFunc()

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
        const klasa = x.getAttribute("value")
        for(let kostka of listaKostekKomnata){
          if(kostka.classList.contains("rd"+klasa)){
            kostka.remove()
            break
          }
        }
        showWaterPumpPrice()
      }

      globalObject.modal.zmeczZipka(listaKostekModal.obiekty.length,i)
      globalObject.kopalnia.zmeczZipka(listaKostekModal.obiekty.length,i)

    }

    if(indeks===0){
      hideModal("kopalnia-modal");
      let i=0;

      for(let narzedzie of globalObject.aktywneNarzedzia.wartosci){
        if(narzedzie==="kilof"){
          i++
        }
      }
    }

    globalObject.resetActiveTools();

  });


  function czytajZaznaczone(e){
    let listaObiektow = [];
    let listaWartosci = [];
    const boksy = [...document.getElementsByClassName(e)];
    boksy.forEach(function(element){
      if(element.checked){
        listaObiektow.push(element);
        listaWartosci.push(element.value);
      }
    });
    return {obiekty:listaObiektow, wartosci:listaWartosci}
  }

}

function showModal(x){
  const modal = document.getElementById(x);
  modal.style.display = "block";
}

function hideModal(x){
  const modal = document.getElementById(x);
  modal.style.display = "none";
}

function discoverChamber(e){
	const komnaty = [...document.getElementsByClassName("komnata")];
	clickRoom(e.target, komnaty.indexOf(e.currentTarget));
}

function openModal(e){
	const komnaty = [...document.getElementsByClassName("komnata")];
	const indeks = komnaty.indexOf(e.currentTarget);
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

function beggaryAndInn(dane){
	console.log(dane.id)
	$.getJSON("/"+dane.id,{a:dane.id}, function(data){
		gameLog(data);
    if(data.zipek){
      updateUpperInfo("wykupieni-gornicy", data.zipek);
    }

	});

}

function toggleHelper(e){
  const stanowiska = [...document.getElementsByClassName("pomocnik")];
  const indeks = stanowiska.indexOf(e.currentTarget);

  $.getJSON("/pomocnik",{a:indeks},function(data){
    gameLog(data)
    if(data.wstawiam){
      console.log(e.target.parentNode)
      toggleHelperAnime(e.target.parentNode, data.gracz);
    }
  });
}

function drawToolCard(dane){
  const narzedzia = document.getElementsByClassName('narzedzie-klikalne');
  const indeksKlikniecia = [...narzedzia].indexOf(dane.currentTarget);
  const indeksKarty = narzedzia.length-indeksKlikniecia-1;
  const kliknietaKarta = dane.currentTarget;

	$.getJSON("/karty-narzedzi",{a:indeksKarty}, function(data){
		gameLog(data);
    if(data.narzedzie){
      puffCard(kliknietaKarta);
      if(data.narzedzie!="puste"){
        revealNewCard(data.narzedzie, "zakryta", "narzedzie-klikalne");
        moveRestCards(indeksKlikniecia, narzedzia, "-104");
      }else{
        moveRestCards(indeksKlikniecia-1, narzedzia, "-104")
      }
    }
	});

}

function buySellMarket(targowisko, indeks){

	$.getJSON("/targ", {
	a: indeks,
	b: JSON.stringify(globalObject.aktywneNarzedzia.wartosci),
	},
	function(data){
      gameLog(data);
			if(data.zmiennaJSON){
        const target = targowisko[data.zmiennaJSON]
        if(target.firstElementChild.classList.contains("wykupione")){
          target.firstElementChild.classList.remove("wykupione");
        }else{
          target.firstElementChild.classList.add("wykupione")
        }
      }
		}
	);
}

function clickShaft(target, indeks){

  $.getJSON('/szyb',{a:indeks}, function(data){
    gameLog(data);

    const holder = target.firstElementChild;
    const obecnyGracz = document.getElementById("imie-gracza");
    const id = obecnyGracz.firstElementChild.getAttribute("value");
    if(!data.zabiera && !data.alrt == 1){
      createMiner(holder, id)
    }
    if(data.zabiera){
      [...holder.children].forEach(function(child){
        if(child.classList.contains(id)){
          minerOutAnime(child)
        }
      })
    }

  });
}

function createMiner(target, pionek){
  const a = document.createElement("div")
  a.className = 'gornik'
  a.classList.add(pionek)
  target.append(a)
  minerInAnime([target.lastElementChild],0);
}

function clickRoom(target, indeks){

  $.getJSON('/komnata',{a:indeks},function(data){

    gameLog(data);

    if(data.odkrywam){
      target.parentNode.classList.add("flip");
      const komnata = target.parentNode.parentNode;

      komnata.classList.remove("zakryte");
      komnata.classList.add("odkryte");


      const kafelek = target.nextElementSibling;
      kafelek.classList.add(data.tlo)

      const kostkiSoli = document.createElement("div");
      kostkiSoli.className = "matsy-kopalnia"

      for(var i in data.kostkiSoli){
        for(let j = 0; j<data.kostkiSoli[i];j++){
          kostkiSoli.innerHTML += "<div class=\"kostka-soli rd"+i+"\"></div>"
        }
      }

      const zipHolder = document.createElement("div");
      zipHolder.className = "gornicy-kopalnia"
      zipHolder.innerHTML = "<div class=\"gornik pionek"+data.lpGracza+"\"></div>"

      const woda = document.createElement("div");
      woda.className = "woda-kopalnia"

      for(var i=0;i<data.woda;i++){
        woda.innerHTML += "<div class=\"kostka-soli rd3\"></div>"
      }

      kafelek.appendChild(kostkiSoli);
      kafelek.appendChild(zipHolder);
      kafelek.appendChild(woda);

      minerInAnime([zipHolder],1500);
      //revealMineTileAnime(target.parentNode);
      target.parentNode.parentNode.removeEventListener("click", discoverChamber)
      target.parentNode.parentNode.addEventListener("click", openModal)

    }
  })
}

function renderModal(indeks){

  $.getJSON("/renderuj-modal",{a:indeks}, function(data){
    showModal('kopalnia-modal');

  	const okn = document.getElementById('cialo-modal-kopalnia');

    while(okn.firstChild){
      okn.removeChild(okn.firstChild)
    }

    let zaznaczoneKostki = []
  	let zaznaczonaWoda = 1

    const cialko = document.createElement("div");
    cialko.id = "wnetrze-modal-kopalnia";
    cialko.innerHTML = data.modal;

    okn.appendChild(cialko);

    setEventListeners();

    globalObject.modal.initialize(cialko, indeks);
  })

}

function executeHidden(e){
  const aktualnaKomnata = globalObject.kopalnia.aktualnaKomnata;
  const komnaty = globalObject.kopalnia.aktualnaKomnata.parentNode;
  const odkryteKomnaty = [...komnaty.getElementsByClassName("odkryte")];
  const wszystkieKomnaty = [...komnaty.children];
  const indeksKomnaty = wszystkieKomnaty.indexOf(aktualnaKomnata);
  console.log(e);
  //e.target.style.display = "none"
  e.target.parentNode.classList.remove("activeTool");
  e.target.parentNode.classList.add("uzyte-narzedzie");

  $.getJSON('/narzedzia-inne',{a:e.currentTarget.id}, function(data){
    if(data.czerpak){

      const wodaKomnata = aktualnaKomnata.querySelector(".rd3")
      const wodaModal = document.querySelector("#wydobycie-wody-modal .kostka-checkbox")
      const narzedzia = document.querySelectorAll(".narzedzie-inwentarz.czerpak, .narzedzie-modal.czerpak")

      wodaKomnata.remove();
      wodaModal.remove();

      const woda = document.createElement("div");
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
      const obecnyGracz = document.getElementById("imie-gracza");
      const id = obecnyGracz.firstElementChild.getAttribute("value");
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

function jumpInQue(e){
  const narzedzia = globalObject.aktywneNarzedzia;
  const stanowiskaKolejki = [...document.getElementsByClassName("kolejka-do-zamku")];
  console.log(narzedzia)
  $.getJSON("/droga-do-zamku", {a:JSON.stringify(narzedzia.wartosci)}, function(data){
    gameLog(data);
    if(data.lpGracza){
      let holder;
      if(data.glejt){
        holder = stanowiskaKolejki[0];
        for(let x of narzedzia.obiekty){
          if(x.getAttribute("value") == "glejtkrolewski"){
            console.log("Wygaszam")
            x.classList.remove("aktywne-inwentarz")
            x.classList.add("uzyte-narzedzie")
            x.removeEventListener("click", toggleTool);

            globalObject.usunNarzedzie(x)

          }
        }

      }else{
        holder = stanowiskaKolejki[1];
      }
      const pionek = 'pionek'+data.lpGracza;
      createMiner(holder, pionek)
    }



  })
}

function completeRoyalOrder(e){
  let zamowieniaModal = [...document.querySelectorAll("#wnetrze-modal-zamowienia .karta-zamowienie")];
  let zamowieniaBoard = [...document.getElementsByClassName("order-odkryty")]

  const absIndeks = zamowieniaModal.indexOf(e.currentTarget)
  const indeks = zamowieniaModal.length-absIndeks-1;

  $.getJSON("/zamowienia-krolewskie", {a:indeks},function(data){
    if(data.realizujeZamowienie){
      gameLog(data);
      zamowieniaModal[absIndeks].remove();
      puffCard(zamowieniaBoard[absIndeks]);

      const cialko = document.getElementById("wnetrze-modal-zamowienia")
      const nowaKarta = document.createElement("div");
      nowaKarta.className = "karta-zamowienie";
      nowaKarta.innerHTML += data.nowaKarta;
      nowaKarta.addEventListener("click", completeRoyalOrder);
      cialko.prepend(nowaKarta);

      moveRestCards(absIndeks, zamowieniaBoard, "-104")

      const kartyZamowien = document.querySelectorAll(".order-zakryty");
      const wierzchniaKarta = kartyZamowien[kartyZamowien.length-1]
      wierzchniaKarta.innerHTML = data.nowaKarta;

      revealNewCard(null, "order-zakryty", "order-odkryty", 800);
      moveUp(wierzchniaKarta);

      updateUpperInfo("zrealizowane-zamowienia", data.zrealizowanychZamowien);



      if(data.doRealizacji == 0){
        hideModal("zamowienia-modal");
      }
    }else{
      gameLog(data);
      hideModal("zamowienia-modal")
    }

  })


}

function finishTurn(e){
  $.getJSON("/koniec-tury",{},function(data){
    hideModal("kopalnia-modal");
    const kolejka = document.getElementById("droga-do-zamku")
    kolejka.innerHTML = data.que;

		gameLog(data);

    if(data.realizujeZamowienie){
      showModal("zamowienia-modal");
      const zamowienia = [...document.querySelectorAll("#wnetrze-modal-zamowienia .karta-zamowienie")];
      zamowienia.forEach(function(zamowienie){
        zamowienie.addEventListener("click", completeRoyalOrder)
      })
    }

    if(data.odpoczywa){
      const pion = "pionek"+data.odpoczywa
      const wszyscyZmeczeni = [...document.getElementsByClassName("zmeczony")]
      for(let x of wszyscyZmeczeni){
        if(x.classList.contains(pion)){
          x.classList.remove("zmeczony")
        }
      }
    }
  })
}

function updateUpperInfo(idElementu, indeks){
  let pozycje = document.getElementById(idElementu)
  pozycje = [...pozycje.children]

  if(indeks < pozycje.length){
    pozycje[indeks].classList.add("highlighted")
  }
  pozycje[indeks-1].classList.remove("highlighted")
}
