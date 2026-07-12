function ver(q){
  var a=document.getElementById('fAntes'),d=document.getElementById('fDepois');
  if(q==='antes'&&!a.src){a.src=a.dataset.src}
  a.classList.toggle('hide',q!=='antes');d.classList.toggle('hide',q==='antes');
  document.getElementById('bAntes').classList.toggle('on',q==='antes');
  document.getElementById('bDepois').classList.toggle('on',q!=='antes');
  document.getElementById('urlLabel').textContent=(q==='antes'?a.dataset.src:d.src);
}
document.getElementById('bAntes').addEventListener('click',function(){ver('antes')});
document.getElementById('bDepois').addEventListener('click',function(){ver('depois')});
