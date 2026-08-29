function posalji() {
  ime=document.getElementById('nadimak').value;
  if (ime==""){
    el=document.getElementById('info_nadimak');
    el.style.display='';
    return;
  }
  poruka=document.getElementById('poruka').value;
  if (poruka!="")
    location.href=`/posalji/${ime}/${poruka}`;
}
