var PROSPECTOR_CSRF=(document.querySelector('meta[name="prospector-csrf"]')||{}).content||'';
var _fetch=window.fetch.bind(window); window.fetch=function(u,o){o=o||{};var m=(o.method||'GET').toUpperCase();if(!['GET','HEAD'].includes(m)){o.headers=new Headers(o.headers||{});o.headers.set('X-CSRF-Token',PROSPECTOR_CSRF)}return _fetch(u,o)};
function action(code, event, el){
 code=(code||'').replace(/return false;?/g,'').trim();
 var m;
 if((m=code.match(/^setView\(['"]([^'"]+)['"]\)/))) return setView(m[1]);
 if((m=code.match(/^abrirEdit\(['"]([^'"]+)['"]\)/))) return abrirEdit(m[1]);
 if((m=code.match(/^deletar\(['"]([^'"]+)['"]\)/))) return deletar(m[1]);
 if((m=code.match(/^ordenar\(['"]([^'"]+)['"]\)/))) return ordenar(m[1]);
 if((m=code.match(/^irPag\(([-0-9]+)\)/))) return irPag(Number(m[1]));
 if(/^mudaPorPag\(this.value\)/.test(code)) return mudaPorPag(el.value);
 if(/^salvarEdit\(\)/.test(code)) return salvarEdit();
 if(/^salvarCfg\(\)/.test(code)) return salvarCfg();
 if(/^salvarHG\(\)/.test(code)) return salvarHG();
 if(/^fecharEdit\(\)/.test(code)) return fecharEdit();
 if(/^fecharDoc\(\)/.test(code)) return fecharDoc();
 if(/^printDoc\(\)/.test(code)) return printDoc();
 if((m=code.match(/^abrirContrato\(['"]([^'"]+)['"],['"]([^'"]*)['"]\)/))) return abrirContrato(m[1],m[2]);
 if((m=code.match(/^cmpSel=['"]([^'"]+)['"];render\(\)/))) {cmpSel=m[1];return render()}
 if((m=code.match(/^salvarOv\(['"]([^'"]+)['"],\{contratoStatus:this.value\}/))) return salvarOv(m[1],{contratoStatus:el.value});
 if((m=code.match(/^salvarOv\(['"]([^'"]+)['"],\{pago:this.checked\?1:0\}/))) return salvarOv(m[1],{pago:el.checked?1:0});
 if(/^dragIni\(event/.test(code)){m=code.match(/dragIni\(event,['"]([^'"]+)['"]\)/);return dragIni(event,m&&m[1]);}
 if(/^dragFim\(event/.test(code)) return dragFim(event);
 if(/^dragSobre\(event/.test(code)) return dragSobre(event);
 if(/^dragSai\(event/.test(code)) return dragSai(event);
 if((m=code.match(/^solta\(event,['"]([^'"]+)['"]\)/))) return solta(event,m[1]);
}
document.addEventListener('click',function(e){var el=e.target.closest('[data-onclick]');if(el){e.preventDefault();action(el.getAttribute('data-onclick'),e,el)}});
document.addEventListener('change',function(e){var el=e.target.closest('[data-onchange]');if(el)action(el.getAttribute('data-onchange'),e,el)});
['dragstart','dragend','dragover','dragleave','drop'].forEach(function(type){document.addEventListener(type,function(e){var el=e.target.closest('[data-on'+type+']');if(el)action(el.getAttribute('data-on'+type),e,el)})});
function esc(v){return v==null?v:String(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;')}
function urlSegura(v){if(!v)return null;try{var u=new URL(v);return(u.protocol==='http:'||u.protocol==='https:')?u.href:null}catch(e){return null}}
function normalizaLead(l){var n={};Object.keys(l||{}).forEach(function(k){n[k]=l[k]});['nome','nicho','cidade','email','telefone','whatsapp','motivo','obs','dataProposta','contratoEm','docCliente','endCliente'].forEach(function(k){if(n[k]!=null)n[k]=esc(n[k])});n.slug=/^[a-z0-9-]{1,80}$/.test(n.slug||'')?n.slug:'';n.siteAntigo=urlSegura(n.siteAntigo);n.urlNova=urlSegura(n.urlNova);return n}
var D=JSON.parse(document.getElementById('dados').textContent);D.leads=(D.leads||[]).map(normalizaLead);
var OV=JSON.parse(localStorage.getItem('prospector_ov')||'{}');
var MODE='file';
function aplicaOv(arr){return arr.filter(function(l){return !(OV[l.slug]&&OV[l.slug]._del)}).map(function(l){return Object.assign({},l,OV[l.slug]||{})})}
var leads=aplicaOv(D.leads||[]);
if(Object.keys(OV).length)document.getElementById('limpar-ov')&&(document.getElementById('limpar-ov').style.display='inline-block');
fetch('/api/leads',{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){MODE='db';leads=j;fetch('/api/config',{cache:'no-store'}).then(function(r){return r.json()}).then(function(c){CFG=(c&&c.contratante!==undefined)?c.contratante:c;HG=(c&&c.hostgator)||{};if(view==='config')render()});var m=document.getElementById('modo');m.textContent='banco conectado';m.className='modo db';m.title='Alterações salvas no prospector.db';var lb=document.getElementById('limpar-ov');if(lb)lb.style.display='none';render()}).catch(function(){});
var CORES={novo:'var(--novo)',redesenhado:'var(--rede)','publicado-local':'var(--pub)',publicado:'var(--pub)','proposta-rascunho':'var(--prop)',proposta:'var(--prop)',respondeu:'var(--resp)',negociacao:'var(--resp)',fechado:'var(--fech)',perdido:'var(--cinza)',descartado:'var(--cinza)'};
var NOMES={novo:'Novo',redesenhado:'Redesenhado','publicado-local':'Preview local',publicado:'Publicado','proposta-rascunho':'Proposta em rascunho',proposta:'Proposta enviada',respondeu:'Respondeu',negociacao:'Negociação',fechado:'Fechado',perdido:'Perdido',descartado:'Descartado'};
var ORDEM=['novo','redesenhado','publicado-local','publicado','proposta-rascunho','proposta','respondeu','negociacao','fechado','perdido'];
var view='geral',busca='',sortCol='nome',sortAsc=true,pag=1,porPag='auto';
function pagSize(){if(porPag!=='auto')return porPag;var v=document.getElementById('view');var h=v?v.clientHeight:600;return Math.max(4,Math.floor((h-165)/59))}
document.getElementById('upd').textContent='atualizado em '+(D.atualizado||'—');
function dias(iso){if(!iso)return 0;return Math.floor((Date.now()-new Date(iso+'T12:00:00'))/864e5)}
function ativos(){return fil().filter(function(l){return l.status!=='descartado'})}
function fil(){var b=busca.toLowerCase();return leads.filter(function(l){return !b||((l.nome||'')+(l.nicho||'')+(l.cidade||'')+(l.status||'')).toLowerCase().indexOf(b)>=0})}
function recarrega(){return fetch('/api/leads',{cache:'no-store'}).then(function(r){return r.json()}).then(function(j){leads=j;render()})}
function salvarOv(slug,ch){
 if(MODE==='db'){fetch('/api/leads/'+encodeURIComponent(slug),{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(ch)}).then(recarrega);return}
 OV[slug]=Object.assign(OV[slug]||{},ch);localStorage.setItem('prospector_ov',JSON.stringify(OV));leads=aplicaOv(D.leads||[]);render()}
function deletar(slug){if(!confirm('Excluir este lead do painel?'))return;
 if(MODE==='db'){fetch('/api/leads/'+encodeURIComponent(slug),{method:'DELETE'}).then(recarrega);return}
 OV[slug]=Object.assign(OV[slug]||{},{_del:true});localStorage.setItem('prospector_ov',JSON.stringify(OV));leads=aplicaOv(D.leads||[]);render()}
var CFG={};
var editSlug=null;
function abrirEdit(slug){editSlug=slug;var l=leads.filter(function(x){return x.slug===slug})[0]||{};
 document.getElementById('m-titulo').textContent='Editar — '+(l.nome||slug);
 document.getElementById('m-status').innerHTML=Object.keys(NOMES).map(function(st){return '<option value="'+st+'"'+(l.status===st?' selected':'')+'>'+NOMES[st]+'</option>'}).join('');
 ['nome','email','telefone','whatsapp','cidade','nicho','valor','dataProposta','urlNova','obs','manutencao','contratoEm','docCliente','endCliente'].forEach(function(k){document.getElementById('m-'+k).value=l[k]==null?'':l[k]});
 document.getElementById('m-pago').value=l.pago?1:0;document.getElementById('m-contratoStatus').value=l.contratoStatus||'pendente';
 document.getElementById('modal-bg').classList.add('aberto')}
function fecharEdit(){document.getElementById('modal-bg').classList.remove('aberto');editSlug=null}
function salvarEdit(){if(!editSlug)return;var ch={};
 ['nome','email','telefone','whatsapp','cidade','nicho','urlNova','obs','dataProposta','docCliente','endCliente'].forEach(function(k){ch[k]=document.getElementById('m-'+k).value||null});
 ch.status=document.getElementById('m-status').value;
 var v=document.getElementById('m-valor').value;ch.valor=v===''?null:parseFloat(v);
 var mn=document.getElementById('m-manutencao').value;ch.manutencao=mn===''?null:parseFloat(mn);
 ch.pago=parseInt(document.getElementById('m-pago').value);ch.contratoStatus=document.getElementById('m-contratoStatus').value;
 var slug=editSlug;fecharEdit();salvarOv(slug,ch)}
function setView(v){view=v;render()}
function nav(){
 var fu=fil().filter(function(l){return l.status==='proposta'&&dias(l.dataProposta)>=4});
 var fechadosN=fil().filter(function(l){return l.status==='fechado'}).length;
 var itens=[['geral','Visão geral',null],['pipeline','Pipeline',ativos().length],['clientes','Clientes',fil().length],['sites','Sites',fil().filter(function(l){return['redesenhado','publicado-local','publicado','proposta','respondeu','fechado'].indexOf(l.status)>=0}).length],['comparador','Comparador',fil().filter(function(l){return l.slug&&['redesenhado','publicado-local','publicado','proposta','respondeu','fechado'].indexOf(l.status)>=0}).length],['followup','Follow-ups',fu.length],['contratos','Contratos',fechadosN],['financeiro','Financeiro',null],['config','Configurações',null]];
 document.getElementById('nav').innerHTML=itens.map(function(i){return '<button class="'+(view===i[0]?'on':'')+'" data-onclick="setView(\''+i[0]+'\')">'+i[1]+(i[2]!==null?'<span class="qt">'+i[2]+'</span>':'')+'</button>'}).join('');
 document.getElementById('titulo').textContent=itens.filter(function(i){return i[0]===view})[0][1];
}
function pillStatus(s){return '<span class="pill" style="background:color-mix(in srgb,'+CORES[s]+' 18%,white);color:'+CORES[s]+'">'+NOMES[s]+'</span>'}
function acoes(l){var a=[];
 if(l.siteAntigo)a.push('<a href="'+l.siteAntigo+'" target="_blank">antigo</a>');
 if(l.slug&&['redesenhado','publicado','proposta','respondeu','fechado'].indexOf(l.status)>=0){a.push('<a href="sites/'+l.slug+'/'+l.slug+'.html" target="_blank">página</a>');a.push('<a href="sites/'+l.slug+'/'+l.slug+'-editor.html" target="_blank">editar site</a>')}
 if(l.urlNova)a.push('<a href="'+l.urlNova+'" target="_blank">no ar ↗</a>');
 if(l.whatsapp)a.push('<a href="https://wa.me/'+l.whatsapp+'" target="_blank">whatsapp</a>');
 if(l.email&&l.email.indexOf('@')>0)a.push('<a href="mailto:'+l.email+'">e-mail</a>');
 a.push('<a href="#" data-onclick="abrirEdit(\''+l.slug+'\');return false">✎ dados</a>');
 a.push('<a href="#" class="del" data-onclick="deletar(\''+l.slug+'\');return false">✕ excluir</a>');
 return '<div class="acoes">'+a.join('')+'</div>'}

function card(l){var f=l.status==='proposta'&&dias(l.dataProposta)>=4?'<span class="tag fup">follow-up '+dias(l.dataProposta)+'d</span>':'';
 return '<div class="card" draggable="true" data-ondragstart="dragIni(event,\''+l.slug+'\')" data-ondragend="dragFim(event)" style="--cor:'+CORES[l.status]+'"><div class="nm">'+l.nome+f+'</div><div class="mt">'+(l.nota?'★ '+l.nota+' ('+l.avaliacoes+')':'')+(l.cidade?' · '+l.cidade:'')+'</div>'+(l.motivo?'<div class="motivo">'+l.motivo+'</div>':'')+(l.obs?'<div class="mt">'+l.obs+'</div>':'')+(l.valor?'<div class="valor">R$ '+l.valor.toLocaleString('pt-BR')+(l.manutencao?' <span style="color:var(--muted);font-weight:600;font-size:11px">+ R$ '+l.manutencao.toLocaleString('pt-BR')+'/mês</span>':'')+'</div>':'')+acoes(l)+'</div>'}
function vGeral(){
 var ls=fil(),at=ativos();
 var props=ls.filter(function(l){return l.status==='proposta'});
 var fu=props.filter(function(l){return dias(l.dataProposta)>=4});
 var fech=ls.filter(function(l){return l.status==='fechado'});
 var receita=fech.reduce(function(a,l){return a+(l.valor||0)},0);
 var pot=at.length*700;
 var html='<div class="stats">'+[['Leads ativos',at.length,''],['Propostas na rua',props.length,''],['Follow-ups pendentes',fu.length,'ambar'],['Fechados',fech.length,'verde'],['Receita fechada','R$ '+receita.toLocaleString('pt-BR'),'verde'],['Potencial (R$700/página)','R$ '+pot.toLocaleString('pt-BR'),'laranja']].map(function(s){return '<div class="stat '+s[2]+'"><div class="n">'+s[1]+'</div><div class="l">'+s[0]+'</div></div>'}).join('')+'</div>';
 var max=Math.max.apply(null,ORDEM.map(function(s){return ls.filter(function(l){return l.status===s}).length}).concat([1]));
 html+='<div class="painel funil"><h2>Funil do pipeline</h2>'+ORDEM.map(function(s){var n=ls.filter(function(l){return l.status===s}).length;return '<div class="linha"><span>'+NOMES[s]+'</span><div class="barra"><div class="fill" style="width:'+(n/max*100)+'%;background:'+CORES[s]+'"></div></div><b>'+n+'</b></div>'}).join('')+'</div>';
 html+='<div class="painel"><h2>Follow-ups pendentes (4+ dias sem resposta)</h2>'+(fu.length?fu.map(function(l){return '<div class="fup-item"><b>'+l.nome+'</b><span class="dias">'+dias(l.dataProposta)+' dias</span><span style="color:var(--muted);font-size:12px">proposta em '+l.dataProposta+'</span>'+(l.whatsapp?'<a style="margin-left:auto;font-size:12px;font-weight:700;color:var(--accent-2)" href="https://wa.me/'+l.whatsapp+'" target="_blank">chamar no WhatsApp →</a>':'')+'</div>'}).join(''):'<div class="vazio">Nenhum follow-up pendente. 👌</div>')+'</div>';
 return html}
function vPipeline(){var por={};fil().forEach(function(l){(por[l.status]=por[l.status]||[]).push(l)});
 return '<p class="dica-drag">Arraste um card para mudar o status — os automáticos (redesenhado, publicado, proposta) o plugin move sozinho; use o arrasto principalmente para <b>Respondeu</b> e <b>Fechado</b>.</p><div class="board">'+ORDEM.concat(['descartado']).map(function(s){var arr=por[s]||[];return '<div class="col" data-st="'+s+'" data-ondragover="dragSobre(event)" data-ondragleave="dragSai(event)" data-ondrop="solta(event,\''+s+'\')"><h3>'+NOMES[s]+'<span>'+arr.length+'</span></h3><div class="cards">'+(arr.length?arr.map(card).join(''):'<div class="vazio">solte aqui</div>')+'</div></div>'}).join('')+'</div>'}
function vClientes(){var ls=fil().slice().sort(function(a,b){var x=a[sortCol]||'',y=b[sortCol]||'';return(x<y?-1:x>y?1:0)*(sortAsc?1:-1)});
 var pp=pagSize();var total=ls.length,paginas=Math.max(1,Math.ceil(total/pp));if(pag>paginas)pag=paginas;
 var ini=(pag-1)*pp,fim=Math.min(ini+pp,total);ls=ls.slice(ini,fim);
 return '<div class="painel tab"><div class="twrap"><table><thead><tr>'+[['nome','Cliente'],['nota','Nota'],['avaliacoes','Aval.'],['cidade','Cidade'],['status','Status'],['valor','Valor'],['x','Contato / páginas']].map(function(c){return '<th data-onclick="ordenar(\''+c[0]+'\')">'+c[1]+(sortCol===c[0]?(sortAsc?' ↑':' ↓'):'')+'</th>'}).join('')+'</tr></thead><tbody>'+ls.map(function(l){return '<tr><td><b>'+l.nome+'</b><div style="color:var(--muted);font-size:11.5px">'+(l.email||'sem e-mail')+'</div></td><td>'+(l.nota?'★ '+l.nota:'—')+'</td><td>'+(l.avaliacoes||'—')+'</td><td>'+(l.cidade||'—')+'</td><td>'+pillStatus(l.status)+'</td><td>'+(l.valor?'R$ '+l.valor.toLocaleString('pt-BR'):'—')+'</td><td>'+acoes(l)+'</td></tr>'}).join('')+'</tbody></table></div><div class="pagin"><span class="info">Mostrando '+(total?ini+1:0)+'–'+fim+' de '+total+' clientes</span><select data-onchange="mudaPorPag(this.value)"><option value="auto"'+(porPag==='auto'?' selected':'')+'>Auto ('+pp+' / página)</option>'+[10,25,50].map(function(n){return '<option value="'+n+'"'+(porPag===n?' selected':'')+'>'+n+' / página</option>'}).join('')+'</select><button data-onclick="irPag('+(pag-1)+')"'+(pag<=1?' disabled':'')+'>‹</button>'+Array.apply(null,{length:paginas}).map(function(_,i){return '<button class="'+(pag===i+1?'on':'')+'" data-onclick="irPag('+(i+1)+')">'+(i+1)+'</button>'}).join('')+'<button data-onclick="irPag('+(pag+1)+')"'+(pag>=paginas?' disabled':'')+'>›</button></div></div>'}
function irPag(n){pag=n;render()}
function mudaPorPag(v){porPag=v==='auto'?'auto':parseInt(v);pag=1;render()}
function vSites(){var ls=fil().filter(function(l){return['redesenhado','publicado-local','publicado','proposta','respondeu','fechado'].indexOf(l.status)>=0});
 return ls.length?'<div class="sites-grid">'+ls.map(function(l){
  var pg='sites/'+l.slug+'/'+l.slug+'.html';
  var prim=l.urlNova?'<a class="prim" href="'+l.urlNova+'" target="_blank">Ver no ar ↗</a>':'<a class="prim" href="'+pg+'" target="_blank">Ver página</a>';
  var ic=[];
  if(l.siteAntigo)ic.push('<a href="'+l.siteAntigo+'" target="_blank" title="site antigo do cliente">antigo</a>');
  if(l.urlNova)ic.push('<a href="'+pg+'" target="_blank" title="versão local">local</a>');
  if(l.whatsapp)ic.push('<a href="https://wa.me/'+l.whatsapp+'" target="_blank">whatsapp</a>');
  if(l.email&&l.email.indexOf('@')>0)ic.push('<a href="mailto:'+l.email+'">e-mail</a>');
  ic.push('<a href="#" data-onclick="abrirEdit(\''+l.slug+'\');return false">✎ dados</a>');
  ic.push('<a href="#" class="del" data-onclick="deletar(\''+l.slug+'\');return false">✕</a>');
  return '<div class="site-card"><div class="prev"><iframe src="'+pg+'" loading="lazy"></iframe></div><div class="info"><div class="s-head"><span class="s-nm">'+l.nome+'</span>'+pillStatus(l.status)+'</div><div class="s-sub">'+[l.nicho,l.cidade,(l.nota?'★ '+l.nota+' ('+l.avaliacoes+')':null)].filter(Boolean).join(' · ')+'</div><div class="s-main">'+prim+'<a class="sec" href="sites/'+l.slug+'/'+l.slug+'-editor.html" target="_blank">Editar site</a></div><div class="s-icons">'+ic.join('')+'</div></div></div>'
 }).join('')+'</div>':'<div class="painel vazio">Nenhum site redesenhado ainda — rode $redesenhar.</div>'}
function vFollowup(){var fu=fil().filter(function(l){return l.status==='proposta'&&dias(l.dataProposta)>=4});
 return '<div class="painel"><h2>Propostas aguardando follow-up</h2>'+(fu.length?fu.map(card).join(''):'<div class="vazio">Nenhum follow-up pendente.</div>')+'</div>'}
function abrirContrato(slug,nome){document.getElementById('doc-titulo').textContent='Contrato — '+nome;document.getElementById('doc-frame').src='sites/'+slug+'/contrato-'+slug+'.html';document.getElementById('doc-bg').classList.add('aberto')}
function fecharDoc(){document.getElementById('doc-bg').classList.remove('aberto');document.getElementById('doc-frame').src='about:blank'}
function printDoc(){var f=document.getElementById('doc-frame');try{f.contentWindow.focus();f.contentWindow.print()}catch(e){window.open(f.src,'_blank');alert('Abri o contrato em nova aba — use Ctrl+P para imprimir/salvar PDF.')}}
function pillCt(st){st=st||'pendente';return '<span class="pill ct-'+st+'">'+st.charAt(0).toUpperCase()+st.slice(1)+'</span>'}
function vContratos(){var ls=fil().filter(function(l){return l.status==='fechado'});
 if(!ls.length)return '<div class="painel vazio">Nenhum cliente fechado ainda. Quando fechar, arraste o card pra "Fechado" e use $contrato [cliente].</div>';
 return '<div class="painel" style="overflow-x:auto"><table><thead><tr><th>Cliente</th><th>Valor</th><th>Manutenção</th><th>Contrato</th><th>Data</th><th>Pago</th><th>Ações</th></tr></thead><tbody>'+ls.map(function(l){
  var doc='sites/'+l.slug+'/contrato-'+l.slug+'.html';
  var acao=(l.contratoStatus&&l.contratoStatus!=='pendente')?'<a href="#" class="btn-ct ver" data-onclick="abrirContrato(\''+l.slug+'\',\''+l.nome.replace(/'/g,'')+'\');return false" title="abrir a folha do contrato aqui no painel">👁 Ver contrato</a><a href="sites/'+l.slug+'/contrato-'+l.slug+'.docx" download class="btn-ct baixar" title="baixa o Word travado que vai pro cliente">⬇ Baixar .docx</a>'+(l.contratoStatus==='assinado'?'<a href="sites/'+l.slug+'/contrato-'+l.slug+'-assinado.docx" download class="btn-ct ass">✓ Assinado</a>':'')+'':'<span style="color:var(--muted);font-size:12px">use $contrato no Codex</span>';
  return '<tr><td><b>'+l.nome+'</b></td><td>'+(l.valor?'R$ '+l.valor.toLocaleString('pt-BR'):'—')+'</td><td>'+(l.manutencao?'R$ '+l.manutencao.toLocaleString('pt-BR')+'/mês':'—')+'</td><td><select class="mini" data-onchange="salvarOv(\''+l.slug+'\',{contratoStatus:this.value})">'+['pendente','enviado','assinado'].map(function(cs){return '<option value="'+cs+'"'+((l.contratoStatus||'pendente')===cs?' selected':'')+'>'+cs+'</option>'}).join('')+'</select></td><td>'+(l.contratoEm||'—')+'</td><td><input type="checkbox" class="fin-check" '+(l.pago?'checked':'')+' data-onchange="salvarOv(\''+l.slug+'\',{pago:this.checked?1:0})"></td><td>'+acao+'</td></tr>'
 }).join('')+'</tbody></table></div>'}
function vFinanceiro(){var ls=fil().filter(function(l){return l.status==='fechado'});
 var recebido=ls.filter(function(l){return l.pago}).reduce(function(a,l){return a+(l.valor||0)},0);
 var areceber=ls.filter(function(l){return !l.pago}).reduce(function(a,l){return a+(l.valor||0)},0);
 var mrr=ls.reduce(function(a,l){return a+(l.manutencao||0)},0);
 var fmt=function(n){return 'R$ '+n.toLocaleString('pt-BR')};
 var html='<div class="stats">'+[['Recebido',fmt(recebido),'verde'],['A receber',fmt(areceber),'ambar'],['Manutenções (MRR)',fmt(mrr)+'/mês','laranja'],['Projeção 12 meses',fmt(recebido+areceber+mrr*12),'verde']].map(function(x){return '<div class="stat '+x[2]+'"><div class="n">'+x[1]+'</div><div class="l">'+x[0]+'</div></div>'}).join('')+'</div>';
 html+='<div class="painel" style="overflow-x:auto"><h2>Fechamentos</h2>'+(ls.length?'<table><thead><tr><th>Cliente</th><th>Valor</th><th>Pago</th><th>Manutenção/mês</th><th>Contrato</th></tr></thead><tbody>'+ls.map(function(l){return '<tr><td><b>'+l.nome+'</b></td><td>'+(l.valor?fmt(l.valor):'—')+'</td><td><input type="checkbox" class="fin-check" '+(l.pago?'checked':'')+' data-onchange="salvarOv(\''+l.slug+'\',{pago:this.checked?1:0})"></td><td>'+(l.manutencao?fmt(l.manutencao):'—')+'</td><td>'+pillCt(l.contratoStatus)+'</td></tr>'}).join('')+'</tbody></table>':'<div class="vazio">Sem fechamentos ainda — a projeção começa no primeiro card arrastado pra Fechado.</div>')+'</div>';
 html+='<div class="painel"><h2>Como o financeiro se alimenta</h2><p style="font-size:13px;color:var(--muted);margin:0">Valor e manutenção entram quando você fecha (drag no kanban ou ✎ dados). "Pago" você marca aqui com um clique. O contrato muda pra "enviado" quando o Codex gera via $contrato — e pra "assinado" quando você marcar.</p></div>';
 return html}
var CFG_CAMPOS=[['nome','Nome completo / razão social'],['cpfCnpj','CPF ou CNPJ'],['endereco','Endereço (rua, nº, bairro)'],['cidadeUf','Cidade/UF'],['email','E-mail'],['whatsapp','WhatsApp (55DDDnúmero)']];
function vConfig(){
 var db=MODE==='db';
 var campos=CFG_CAMPOS.map(function(c){return '<div><label style="display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin:12px 0 4px">'+c[1]+'</label><input id="cfg-'+c[0]+'" value="'+((CFG[c[0]]||'').replace(/"/g,'&quot;'))+'" '+(db?'':'disabled')+' style="width:100%;border:1px solid var(--line);border-radius:9px;padding:9px 11px;font-size:13.5px;font-family:var(--sans);color:var(--ink);background:var(--surface)"></div>'}).join('');
 return '<div class="painel" style="max-width:640px"><h2>Meus dados — quem assina os contratos</h2><p style="font-size:13px;color:var(--muted);margin:0 0 6px">Preencha uma vez e todo contrato gerado pelo $contrato já sai com os seus dados de CONTRATADO(A) completos. Fica salvo no prospector-config.json, no seu computador.</p>'+campos+'<div style="margin-top:18px;display:flex;gap:10px;align-items:center"><button '+(db?'':'disabled')+' data-onclick="salvarCfg()" style="border:0;border-radius:10px;padding:11px 22px;font-size:13.5px;font-weight:700;cursor:pointer;background:var(--accent);color:#fff">Salvar meus dados</button><span id="cfg-ok" style="color:var(--ok);font-weight:700;font-size:13px;display:none">salvo ✓</span>'+(db?'':'<span style="color:var(--warn);font-size:12.5px;font-weight:600">abra pelo iniciar-dashboard.bat para editar — ou dite os dados pro Codex no /setup</span>')+'</div></div>'+
 '<div class="painel" style="max-width:640px"><h2>Hospedagem SFTP opcional</h2><p style="font-size:13px;color:var(--muted);margin:0 0 6px">O dashboard salva apenas dados n\u00e3o secretos. A autentica\u00e7\u00e3o usa uma chave SSH protegida pelo sistema; nunca cole senha aqui.</p>'+[['usuario','Usu\u00e1rio SFTP','text'],['dominio','Dom\u00ednio principal','text'],['servidor','Servidor SFTP','text'],['porta','Porta (padr\u00e3o: 22)','number'],['pastaBase','Pasta remota base','text'],['chaveSsh','Caminho da chave p\u00fablica/privada protegida','text']].map(function(c){return '<div><label style="display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin:12px 0 4px">'+c[1]+'</label><input id="hg-'+c[0]+'" type="'+c[2]+'" value="'+((HG[c[0]]||'').toString().replace(/"/g,'&quot;'))+'" '+(db?'':'disabled')+' style="width:100%;border:1px solid var(--line);border-radius:9px;padding:9px 11px;font-size:14px;font-family:var(--sans);background:'+(db?'var(--white)':'#f0ede4')+'"></div>'}).join('')+'<div style="margin-top:18px;display:flex;gap:10px;align-items:center"><button '+(db?'':'disabled')+' data-onclick="salvarHG()" style="border:0;border-radius:10px;padding:11px 22px;font-size:13.5px;font-weight:700;cursor:pointer;background:var(--accent);color:#fff">Salvar configura\u00e7\u00e3o</button><span id="hg-ok" style="color:var(--ok);font-weight:700;font-size:13px;display:none">salvo \u2713</span></div></div>'+
 '<div class="painel" style="max-width:640px"><h2>E os dados do cliente?</h2><p style="font-size:13px;color:var(--muted);margin:0">CPF/CNPJ e endereço do cliente entram quando ele fechar: peça pelo WhatsApp e (1) cole a resposta pro Codex no $contrato — ele extrai e salva sozinho — ou (2) preencha no ✎ dados do card. O que faltar sai como "preencher" na minuta.</p></div>'}
function salvarCfg(){var body={};CFG_CAMPOS.forEach(function(c){body[c[0]]=document.getElementById('cfg-'+c[0]).value||''});
 fetch('/api/config',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({contratante:body})}).then(function(){CFG=body;var ok=document.getElementById('cfg-ok');ok.style.display='inline';setTimeout(function(){ok.style.display='none'},2000)})}
function salvarHG(){var body={};['usuario','dominio','servidor','porta','pastaBase','chaveSsh'].forEach(function(k){var el=document.getElementById('hg-'+k);if(el)body[k]=el.value||''});
 fetch('/api/config',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({hostgator:body})}).then(function(){Object.keys(body).forEach(function(k){HG[k]=body[k]});var ok=document.getElementById('hg-ok');ok.style.display='inline';setTimeout(function(){ok.style.display='none';render()},1200)})}
function ordenar(c){if(c==='x')return;if(sortCol===c)sortAsc=!sortAsc;else{sortCol=c;sortAsc=true}pag=1;render()}
var cmpSel=null;var HG={};
function vComparador(){var ls=fil().filter(function(l){return l.slug&&['redesenhado','publicado-local','publicado','proposta','respondeu','fechado'].indexOf(l.status)>=0});
 if(!ls.length)return '<div class="painel"><div class="vazio">Sem sites redesenhados ainda — use $redesenhar e o antes/depois aparece aqui.</div></div>';
 if(!cmpSel||!ls.some(function(l){return l.slug===cmpSel}))cmpSel=ls[0].slug;
 var l=ls.filter(function(x){return x.slug===cmpSel})[0];
 var antiga=l.siteAntigo?((l.siteAntigo.indexOf('http')===0?l.siteAntigo:'https://'+l.siteAntigo)):null;
 var nova='sites/'+l.slug+'/'+l.slug+'.html';
 return '<div class="cmp-tabs">'+ls.map(function(x){return '<button class="'+(x.slug===cmpSel?'on':'')+'" data-onclick="cmpSel=\''+x.slug+'\';render()">'+x.nome+'</button>'}).join('')+'</div>'
 +'<div class="cmp-grid"><div class="cmp-col"><div class="cab antes">Antes — site atual'+(antiga?' · <a href="'+antiga+'" target="_blank" style="color:inherit">abrir ↗</a>':'')+'</div>'+(antiga?'<iframe src="'+antiga+'" loading="lazy"></iframe>':'<div class="vazio" style="padding:30px">Sem URL do site antigo registrada.</div>')+'</div>'
 +'<div class="cmp-col"><div class="cab depois">Depois — nova versão · <a href="'+nova+'" target="_blank" style="color:inherit">abrir ↗</a></div><iframe src="'+nova+'"></iframe></div></div>'
 +'<div style="font-size:11.5px;color:var(--muted);margin-top:8px">Alguns sites antigos bloqueiam visualização embutida — se o lado "Antes" ficar em branco, use o link "abrir ↗".</div>'}
function render(){nav();document.getElementById('view').innerHTML={geral:vGeral,pipeline:vPipeline,clientes:vClientes,sites:vSites,comparador:vComparador,followup:vFollowup,contratos:vContratos,financeiro:vFinanceiro,config:vConfig}[view]()}
var dragSlug=null;
function dragIni(e,slug){dragSlug=slug;e.target.classList.add('arrastando');e.dataTransfer.effectAllowed='move'}
function dragFim(e){e.target.classList.remove('arrastando')}
function dragSobre(e){e.preventDefault();e.dataTransfer.dropEffect='move';e.currentTarget.classList.add('alvo')}
function dragSai(e){e.currentTarget.classList.remove('alvo')}
function solta(e,st){e.preventDefault();e.currentTarget.classList.remove('alvo');if(!dragSlug)return;
 var ch={status:st};
 if(st==='fechado'){var v=prompt('Fechou! Valor cobrado (R$):','700');if(v!==null&&v!==''&&!isNaN(parseFloat(v)))ch.valor=parseFloat(v)}
 if(st==='proposta'&&!leads.filter(function(l){return l.slug===dragSlug})[0].dataProposta)ch.dataProposta=new Date().toISOString().slice(0,10);
 salvarOv(dragSlug,ch);dragSlug=null}
document.getElementById('busca').addEventListener('input',function(){busca=this.value;pag=1;render()});
var rsz;window.addEventListener('resize',function(){clearTimeout(rsz);rsz=setTimeout(render,150)});
render();
