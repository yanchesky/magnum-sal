var globalObject = {

  aktywneNarzedzia: {
    obiekty: [],
    wartosci: []
  },

  dodajNarzedzie: function(e){
    this.aktywneNarzedzia.obiekty.push(e);
    this.aktywneNarzedzia.wartosci.push(e.getAttribute("value"));
    this.pokazUkryte(e, true)
  },

  usunNarzedzie: function(e){
    this.aktywneNarzedzia.obiekty.splice(this.aktywneNarzedzia.obiekty.indexOf(e), 1 );
    this.aktywneNarzedzia.wartosci.splice(this.aktywneNarzedzia.wartosci.indexOf(e.getAttribute("value")), 1 );
    this.pokazUkryte(e, false)

  },

  pokazUkryte: function(e, h){
    if(e.classList.contains("tool3") || e.classList.contains("tool4")){
      console.log("Zawiera tool3 lub tool4")
      for(let x of [...e.children]){
        if(h){
          x.style.display = "block";
          x.addEventListener("click", executeUkryte)
          e.removeEventListener("click", toggleNarzedzie)

        }else{
          x.style.display = "none";
        }
      }
    }
  },

  policzNarzedzie: function(szukaneNarzedzie){
    let i = 0;
    for(let narzedzie of this.aktywneNarzedzia.wartosci){
      if(narzedzie==szukaneNarzedzie){
        i++
      }
    }
    return i
  },

  zmeczZipka: function(e){
    let l = this.kostkiWody.children.length+e;

    console.log(l)

    for(var i=0;i<l;i++){
      this.gornicy[i].className += " zmeczony"
      console.log(this.gornicy)
    }
  },

  resetActiveTools: function(){
    for(var x of this.aktywneNarzedzia.obiekty){
      x.classList.remove("aktywne-modal")
      x.className += " uzyte-narzedzie"
    }
  },


  kopalnia: {

    wstawZipka: function(e){
      for(var x of e){
        this.gornicyHolder.appendChild(x)
        zipekIn([...this.gornicyHolder.children].slice(this.gornicy.length-1,this.gornicy.length), 0);
      }
    },
    usunZipka: function(e){
      let obecnyGracz = document.getElementById("imie-gracza");
      let id = obecnyGracz.firstElementChild.getAttribute("value");

      for(let x of [...this.gornicyHolder.children]){
        if(x.classList.contains(id) && x.classList.contains("zmeczony") == false){
          zipekOut(x);
          break
        }
      }

    },

    zmeczZipka: function(e,kilofy){
      let l = this.kostkiWody.children.length+e;

      let aktywniGornicy = document.querySelectorAll(".wymagany-gornik");
      aktywniGornicy.forEach(function(e){
        e.classList.remove("wymagany-gornik");
        console.log(e.classList)
      })

      let obecnyGracz = document.getElementById("imie-gracza");
      let id = obecnyGracz.firstElementChild.getAttribute("value");
      let i = 0;

      console.log(id)

      for(let x of this.gornicy){
        if(x.classList.contains(id) && !x.classList.contains("zmeczony")){
          x.classList.add("zmeczony")
          break
        }
      }

      for(let x of this.gornicy){
        if(i<l-kilofy-1 && x.classList.contains(id)){
          if(!x.classList.contains("zmeczony")){
            console.log("lista:",x.classList)
            console.log("i",i)
            x.classList.add("zmeczony")
            i++
          }
        }
      }
    },

    initialize: function(obj, ind){
      this.indeksKomnaty = ind;
      this.aktualnaKomnata = obj;

      [this.kostkiSoli, this.gornicyHolder, this.kostkiWody] =
         this.aktualnaKomnata.firstElementChild.children[1].children;

      this.gornicy = this.gornicyHolder.children
    }
  },

  modal: {

    aktywneNarzedzia: [],

    wstawZipka: function(e){
      for(var x of e){
        this.gornicyHolder.appendChild(x)
      }
      zipekIn([...this.gornicyHolder.children].slice(0,e.length), 0);
    },

    usunZipka: function(e){
      zipekOut(this.gornicyHolder.firstElementChild);

    },

    zmeczZipka: function(e,kilofy){
      let l = this.kostkiWody.length+e;

      let aktywniGornicy = document.querySelectorAll(".wymagany-gornik");
      aktywniGornicy.forEach(function(e){
        e.classList.remove("wymagany-gornik");
        console.log(e.classList)
      })



      this.gornicy[0].classList.add("zmeczony")
      console.log(this.gornicy)

      for(var i=1;i<l-kilofy;i++){
        this.gornicy[i].classList.add("zmeczony")
        console.log(this.gornicy)
      }
    },

    czytajZaznaczone: function(e){
      this.kostkiWody = [...document.getElementsByClassName("wodaBox")];
      return this.kostkiWody.length
    },

    initialize: function(obj, ind){
      this.indeksModala = ind;
      this.cialo = obj;

      this.kostkiSoli = [...document.getElementsByClassName("kostka-checkbox")];
      this.gornicyHolder = document.getElementById("gornicy-gracza-modal");
      this.gornicy = this.gornicyHolder.children;
      //this.gornicy = [...this.gornicy]
      this.kostkiWody = [...document.getElementsByClassName("wodaBox")];

    }
  }

}
