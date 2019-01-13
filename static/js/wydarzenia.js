

window.onload = function(){
	const kartyNarzedzi = [...document.getElementById("karty-narzedzi").children];
	const kartyZamowien = [...document.getElementById("zamowienia-krolewskie").children];
	const pomocnicy = [...document.getElementsByClassName("pomocnik")];
	const targowisko = [...document.getElementsByClassName("stanowisko-targ")];
	const szyby = [...document.getElementsByClassName("szyb")];
	const komnatyZakryte = [...document.getElementsByClassName("zakryte")];
	const komnatyOdkryte = [...document.getElementsByClassName("odkryte")];
	const beggary = document.getElementById("plac-zebralniczy");
	const ziphouse = document.getElementById("karczma");
	const kolejka = document.getElementById("droga-do-zamku");
	const glejty = document.querySelectorAll('#narzedzia-gracza > div .glejtkrolewski, .glejthandlowy');
	const endturnButton = document.getElementById("przycisk-konca-tury")
	let playerTools = document.getElementById("narzedzia-gracza").firstElementChild


	kolejka.addEventListener("click", wstawDoKolejki);

	zrzucanieKartNew(kartyNarzedzi)
	zrzucanieKartNew(kartyZamowien)

	beggary.addEventListener("click", function(){
		beggaryAndZiphouse(this);
		//animacjaMonetyNew(this);
	});

	ziphouse.addEventListener("click", function(){
		beggaryAndZiphouse(this);
	});

	pomocnicy.forEach(function(pomocnik){
		pomocnik.addEventListener("click", togglePomocnik);
	});

	targowisko.forEach(function(slotSoli){
		slotSoli.addEventListener("click", function(){
			buySellTarg(targowisko, targowisko.indexOf(this))
		});
	});

	szyby.forEach(function(szyb){
		szyb.addEventListener("click", function(){
			clickSzyb(this, szyby.indexOf(this));
		});
	});

	komnatyZakryte.forEach(function(komnata){
		komnata.addEventListener("click", odkryjKomnate)
	});

	komnatyOdkryte.forEach(function(komnata){
		komnata.addEventListener("click", otworzModal)
	})

	glejty.forEach(function(glejt){
		console.log(glejt);
		if(!glejt.classList.contains("usedTool")){
			glejt.addEventListener("click", toggleNarzedzie);
		}
	})

	endturnButton.addEventListener("click", zakonczTure)

	playerTools.addEventListener("mousemove", slideTools)



}
