window.onload = function(){
	const kartyNarzedzi = [...document.getElementById("karty-narzedzi").children];
	const kartyZamowien = [...document.getElementById("zamowienia-krolewskie").children];
	const pomocnicy = [...document.getElementsByClassName("pomocnik")];
	const targowisko = [...document.getElementsByClassName("stanowisko-targ")];
	const szyby = [...document.getElementsByClassName("szyb")];
	const komnatyZakryte = [...document.getElementsByClassName("zakryte")];
	const komnatyOdkryte = [...document.getElementsByClassName("odkryte")];
	const zebralnia = document.getElementById("plac-zebralniczy");
	const karczma = document.getElementById("karczma");
	const kolejka = document.getElementById("droga-do-zamku");
	const glejty = document.querySelectorAll('#narzedzia-gracza > div .glejtkrolewski, #narzedzia-gracza > div .glejthandlowy');
	const koniecTury = document.getElementById("przycisk-konca-tury")
	const narzedziaGracza = document.getElementById("narzedzia-gracza").firstElementChild


	kolejka.addEventListener("click", jumpInQue);

	dropCardsAnime(kartyNarzedzi)
	dropCardsAnime(kartyZamowien)

	zebralnia.addEventListener("click", function(){
		beggaryAndInn(this);
	});

	karczma.addEventListener("click", function(){
		beggaryAndInn(this);
	});

	pomocnicy.forEach(function(pomocnik){
		pomocnik.addEventListener("click", toggleHelper);
	});

	targowisko.forEach(function(slotSoli){
		slotSoli.addEventListener("click", function(){
			buySellMarket(targowisko, targowisko.indexOf(this))
		});
	});

	szyby.forEach(function(szyb){
		szyb.addEventListener("click", function(){
			clickShaft(this, szyby.indexOf(this));
		});
	});

	komnatyZakryte.forEach(function(komnata){
		komnata.addEventListener("click", discoverChamber)
	});

	komnatyOdkryte.forEach(function(komnata){
		komnata.addEventListener("click", openModal)
	})

	glejty.forEach(function(glejt){
		console.log(glejt);
		if(!glejt.classList.contains("usedTool")){
			glejt.addEventListener("click", toggleTool);
		}
	})

	koniecTury.addEventListener("click", finishTurn)

	narzedziaGracza.addEventListener("mousemove", slideTools)



}
