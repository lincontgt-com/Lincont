#!/usr/bin/env python3
# Genera las páginas de LINCONT. Para agregar un servicio nuevo: añade un dict a SERVICES.
import html, json, pathlib
ROOT = pathlib.Path(__file__).parent
WA = "50247379912"          # WhatsApp de contacto (confirmar)
EMAIL = "lincont.gt@gmail.com"
W3F = ""                    # clave de Web3Forms (se pega aquí; vacía = usa WhatsApp)  # correo (cambiar por el real)

SERVICES = [
 dict(slug="ingenieria-electrica", file="ingenieria-electrica.html", num="01",
      title="Ingeniería eléctrica", provider="Global EMC", dark=True,
      short="Servicios eléctricos para proyectos industriales, comerciales y corporativos."),
 dict(slug="furgones-y-estructuras", file="furgones-y-estructuras.html", num="02",
      title="Furgones y estructuras metálicas", provider="Furgoservi", dark=False, soon_provider=True,
      short="Fabricación y modificación de furgones, estructuras metálicas y soluciones personalizadas para proyectos empresariales."),
]
COMING = []

def head(title, desc, depth=""):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#F7F5F0">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_GT">
<link rel="icon" type="image/png" href="assets/lincont-isologo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<script>if(!matchMedia("(prefers-reduced-motion:reduce)").matches)document.documentElement.classList.add("js")</script>
</head>
<body>
<a class="skip" href="#main">Ir al contenido</a>
"""

def header(home):
    p = "" if home else "index.html"
    links = [("Inicio", f"{p}#inicio"), ("Servicios", f"{p}#servicios"), ("Cómo funciona", f"{p}#como-funciona"),
             ("Empresas y aliados", f"{p}#empresas"), ("Contacto", f"{p}#contacto")]
    nav = "".join(f'<a href="{h}"{" aria-current=page" if (home and n=="Inicio") else ""}>{n}</a>' for n, h in links)
    mob = "".join(f'<a href="{h}">{n}</a>' for n, h in links)
    return f"""<header>
 <div class="wrap nav">
  <a href="{p or '#inicio'}" aria-label="LINCONT, inicio"><img class="logo" src="assets/lincont-logo.png" alt="LINCONT" width="176" height="30"></a>
  <nav class="links" aria-label="Principal">{nav}</nav>
  <a class="btn filled" href="{p}#contacto">Hablemos <span aria-hidden="true">→</span></a>
  <button class="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="mobile"><span></span></button>
 </div>
</header>
<div class="mobile" id="mobile" role="dialog" aria-modal="true" aria-label="Menú">
 <div class="mtop"><img class="logo" src="assets/lincont-logo.png" alt="LINCONT"><button class="x" aria-label="Cerrar menú">×</button></div>
 <nav>{mob}</nav>
</div>
"""

FOOT = f"""<footer>
 <div class="wrap fgrid">
  <img src="assets/lincont-logo.png" alt="LINCONT" width="160" height="27">
  <p>Conectamos empresas especializadas con nuevas oportunidades de negocio.</p>
  <p class="r">Guatemala<br><small>© <span id="y">2026</span> LINCONT</small></p>
 </div>
</footer>
<script>
const $=s=>document.querySelector(s);
const m=$('#mobile'),b=$('.burger');
function setMenu(o){{m.classList.toggle('open',o);b.setAttribute('aria-expanded',o);document.body.style.overflow=o?'hidden':'';}}
b.addEventListener('click',()=>setMenu(true));
$('.x').addEventListener('click',()=>setMenu(false));
m.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));
document.addEventListener('keydown',e=>{{if(e.key==='Escape')setMenu(false)}});
$('#y').textContent=new Date().getFullYear();
const fd=$('#fecha');if(fd)fd.min=new Date().toISOString().slice(0,10);
document.addEventListener('click',e=>{{
  const a=e.target.closest&&e.target.closest('a[href^="mailto:"]');
  if(!a||/Android|iPhone|iPad|Mobile/i.test(navigator.userAgent))return;
  e.preventDefault();
  const u=new URL(a.href);
  const q=new URLSearchParams({{view:'cm',fs:'1',to:u.pathname}});
  if(u.searchParams.get('subject'))q.set('su',u.searchParams.get('subject'));
  if(u.searchParams.get('body'))q.set('body',u.searchParams.get('body'));
  window.open('https://mail.google.com/mail/?'+q.toString(),'_blank');
}});
const KEY='{W3F}';
const f=$('form[data-wa]');
if(f)f.addEventListener('submit',e=>{{
  e.preventDefault();
  const rows=[];
  f.querySelectorAll('input,select,textarea').forEach(el=>{{
    const l=f.querySelector('label[for="'+el.id+'"]');
    if(l)rows.push([l.textContent,el.value.trim()||'-']);
  }});
  const text=[f.dataset.intro,''].concat(rows.map(r=>r[0]+': '+r[1])).join('\\n');
  const wa='https://wa.me/{WA}?text='+encodeURIComponent(text);
  const ok=$('.ok'),btn=f.querySelector('button[type=submit]');
  function show(h){{ok.classList.add('show');ok.innerHTML=h}}
  const mailto='mailto:{EMAIL}?subject='+encodeURIComponent(f.dataset.subject||'Solicitud de cita')+'&body='+encodeURIComponent(text);
  function viaWA(){{
    show('<strong>No pudimos enviar la solicitud desde aquí.</strong> Puedes enviarla por <a style="text-decoration:underline" href="'+mailto+'">correo</a> o por <a style="text-decoration:underline" href="'+wa+'" target="_blank" rel="noopener">WhatsApp</a>.');
  }}
  btn.disabled=true;
  const mail=f.querySelector('input[type=email]');
  let url,payload;
  if(KEY){{
    url='https://api.web3forms.com/submit';
    payload={{access_key:KEY,subject:f.dataset.subject||'Nueva solicitud desde la página de LINCONT',from_name:'Página de LINCONT',message:text}};
    rows.forEach(r=>payload[r[0]]=r[1]);
    if(mail&&mail.value)payload.email=mail.value;
  }}else{{
    url='https://formsubmit.co/ajax/{EMAIL}';
    payload={{_subject:f.dataset.subject||'Nueva solicitud desde la página de LINCONT',_template:'table',_captcha:'false'}};
    rows.forEach(r=>payload[r[0]]=r[1]);
    if(mail&&mail.value)payload._replyto=mail.value;
  }}
  fetch(url,{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify(payload)}})
   .then(r=>r.json()).then(j=>{{
     if(j.success===true||j.success==='true'){{f.reset();show('<strong>Solicitud enviada.</strong> Te escribiremos para confirmar tu cita. Si necesitas una respuesta rápida, <a style="text-decoration:underline" href="'+wa+'" target="_blank" rel="noopener">escríbenos por WhatsApp</a>.')}}
     else viaWA();
   }}).catch(viaWA).finally(()=>{{btn.disabled=false}});
}});
</script>
</body>
</html>
"""

MOTION_JS = r"""
(function(){
 var els=document.querySelectorAll('[data-count]');
 if(!els.length||!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
 function run(el){var t=+el.dataset.count,suf=el.dataset.suf||'',s=performance.now();(function f(n){var k=Math.min((n-s)/1600,1),e=1-Math.pow(1-k,3);el.textContent=Math.round(t*e)+suf;if(k<1)requestAnimationFrame(f)})(s)}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){run(e.target);io.unobserve(e.target)}})},{threshold:.6});
 els.forEach(function(el){io.observe(el)});
})();

(function(){
 var st=document.querySelector('.stage');if(!st)return;
 var NS='http://www.w3.org/2000/svg',svg=st.querySelector('.net'),c=st.querySelector('.bigc');
 function build(){
  var sr=st.getBoundingClientRect(),cr=c.getBoundingClientRect();if(!sr.width||!cr.width)return;
  svg.setAttribute('viewBox','0 0 '+sr.width+' '+sr.height);svg.innerHTML='';
  var cx=cr.left-sr.left+cr.width*.5,cy=cr.top-sr.top+cr.height*.5;
  st.querySelectorAll('.chip').forEach(function(ch,k){
   var r=ch.getBoundingClientRect(),x=r.left-sr.left+r.width/2,y=r.top-sr.top+r.height/2;
   var L=Math.hypot(cx-x,cy-y),d='M'+x+' '+y+' L'+cx+' '+cy;
   var p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('class','conn');p.style.setProperty('--L',L);p.style.setProperty('--k',k);svg.appendChild(p);
   var dot=document.createElementNS(NS,'circle');dot.setAttribute('r','3.5');dot.setAttribute('class','pulse');
   var am=document.createElementNS(NS,'animateMotion');am.setAttribute('path',d);am.setAttribute('dur',(3.2+k*.5)+'s');am.setAttribute('begin',(2.4+k*.6)+'s');am.setAttribute('repeatCount','indefinite');dot.appendChild(am);svg.appendChild(dot);
  });
 }
 addEventListener('load',build);addEventListener('resize',build);setTimeout(build,300);
 if(document.fonts&&document.fonts.ready)document.fonts.ready.then(build);
})();

(function(){
 var d=document,h=d.documentElement;
 if(!h.classList.contains('js'))return;
 var hd=d.querySelector('header'),st=d.querySelector('.stage'),hero=d.querySelector('.hero');
 var pr=d.createElement('div');pr.id='prog';d.body.appendChild(pr);
 function onS(){var y=window.scrollY,mx=h.scrollHeight-innerHeight;pr.style.transform='scaleX('+(mx>0?Math.min(y/mx,1):0)+')';hd.classList.toggle('sc',y>20);if(st)st.style.setProperty('--sy',y)}
 addEventListener('scroll',onS,{passive:true});onS();
 if(hero&&st&&matchMedia('(pointer:fine)').matches){
  hero.addEventListener('mousemove',function(e){var r=hero.getBoundingClientRect();st.style.setProperty('--mx',((e.clientX-r.left)/r.width-.5)*2);st.style.setProperty('--my',((e.clientY-r.top)/r.height-.5)*2)});
  hero.addEventListener('mouseleave',function(){st.style.setProperty('--mx',0);st.style.setProperty('--my',0)});
 }

 if(hero){hero.addEventListener('mousemove',function(e){var r=hero.getBoundingClientRect();hero.style.setProperty('--gx',(e.clientX-r.left)+'px');hero.style.setProperty('--gy',(e.clientY-r.top)+'px')})}
 var h1=d.querySelector('.hero h1');
 if(h1){var n=0;(function walk(node){Array.prototype.slice.call(node.childNodes).forEach(function(c){
  if(c.nodeType===3){var f=d.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(function(p){if(!p)return;
   if(/^\s+$/.test(p)){f.appendChild(d.createTextNode(' '))}else{var w=d.createElement('span');w.className='w';var i=d.createElement('i');i.style.setProperty('--i',n++);i.textContent=p;w.appendChild(i);f.appendChild(w)}});
   node.replaceChild(f,c)}
  else if(c.nodeType===1)walk(c)})})(h1);h1.classList.add('split')}
 var els=d.querySelectorAll('.top,.sec .wrap>*,.feat,.proj,.list li,.card,.step,.pgrid>div:first-child,.path>*,.agrid>div,.fcols>*,.cwrap>*,.phero .wrap>*,.more-note,.fgrid>*,.jcard,.jstep');
 var cnt=new Map();
 els.forEach(function(el){var k=el.parentNode,i=cnt.get(k)||0;cnt.set(k,i+1);el.style.setProperty('--d',Math.min(i,5));el.classList.add('r')});
 if(!('IntersectionObserver' in window)){els.forEach(function(el){el.classList.add('in')});return}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
 els.forEach(function(el){io.observe(el)});
})();
"""
FOOT = FOOT.replace("</script>\n</body>", "</script>\n<script>" + MOTION_JS + "</script>\n</body>")

def contact_bar():
    return f"""<section class="contact" id="contacto">
 <div class="wrap cwrap">
  <div><div class="eyebrow">Contacto</div><h2>Hablemos de nuevas oportunidades</h2><p>Estamos listos para ayudarte a encontrar el servicio o aliado que necesitas.</p></div>
  <div class="cta">
   <a class="btn filled" href="https://wa.me/{WA}?text=Hola%2C%20quiero%20hablar%20con%20LINCONT." target="_blank" rel="noopener">WhatsApp <span aria-hidden="true">→</span></a>
   <a class="btn light" href="mailto:{EMAIL}">{EMAIL} <span aria-hidden="true">→</span></a>
  </div>
 </div>
</section>
"""

def card(s):
    cls = {"ingenieria-electrica": "card emc", "furgones-y-estructuras": "card furgo"}.get(s["slug"], "card")
    motif = {"ingenieria-electrica": BOLT, "furgones-y-estructuras": VAN}.get(s["slug"], "").replace('class="motif bolt"', 'class="cm"').replace('class="motif van"', 'class="cm cmv"')
    tag = ""
    return f"""   <article class="{cls}">
    {motif}
    <div class="num">{s['num']}</div>
    {tag}
    <div class="prov">{html.escape(s['title'])}</div>
    <h3>{html.escape(s['provider'])}</h3>
    <p>{html.escape(s['short'])}</p>
    <a class="btn {'light' if cls != 'card' else 'ghost'}" href="{s['file']}">Conocer más <span aria-hidden="true">→</span></a>
   </article>"""

def soon(n, t):
    return f"""   <article class="card soon">
    <div class="num">{n}</div>
    <span class="tag">Próximamente</span>
    <h3>{html.escape(t)}</h3>
    <p>Nuevas empresas especializadas se incorporarán a LINCONT.</p>
   </article>"""

def index():
    items = ["Ingeniería eléctrica", "Furgones y estructuras metálicas", "Cierre de ventas", "Desarrollo de negocios", "Empresas especializadas", "Oportunidades reales"]
    ticker = '<div class="grp">' + "".join(f"<span>{t}</span>" for t in items) + "</div>"
    cards = "\n".join(card(s) for s in SERVICES) + "\n" + "\n".join(soon(n, t) for n, t in COMING)
    return head("LINCONT – Desarrollo de negocios",
                "LINCONT conecta empresas especializadas con nuevas oportunidades de negocio en Guatemala.") + header(True) + f"""<main id="main">

<section class="hero" id="inicio">
 <div class="bgword" aria-hidden="true">LINCONT</div>
 <div class="wrap hero-grid">
  <div>
   <div class="eyebrow">Desarrollo de negocios</div>
   <h1>Conectamos empresas especializadas con nuevas <em>oportunidades</em> de negocio.</h1>
   <p class="lead">Identificamos necesidades empresariales y facilitamos el contacto con proveedores especializados que pueden atenderlas.</p>
   <div class="cta">
    <a class="btn filled" href="#servicios">Necesito un servicio <span aria-hidden="true">→</span></a>
    <a class="btn ghost" href="trabaja-con-lincont.html">Quiero trabajar con LINCONT <span aria-hidden="true">→</span></a>
   </div>
  </div>
  <div class="stage" aria-hidden="true">
   <div class="shape s1"></div><div class="shape s2"></div><div class="shape s3"></div>
   <svg class="net"></svg>
   <img class="bigc" src="assets/lincont-c.svg" alt="">
   <div class="ring"></div><img class="seal" src="assets/lincont-isologo.svg" alt="">
   <span class="chip c1" style="--b:0s">Ingeniería eléctrica</span>
   <span class="chip c2" style="--b:-1.4s">Furgones y estructuras</span>
   <span class="chip c3" style="--b:-2.6s">Cierre de ventas</span>
   <span class="chip c4" style="--b:-3.8s">Desarrollo de negocios</span>
  </div>
  </div>
 </div>
 <div class="scrollcue" aria-hidden="true"><span>Desliza</span><i></i></div>
</section>

<div class="ticker" aria-hidden="true"><div class="track">{ticker}{ticker}</div></div>

<section class="services" id="servicios">
 <div class="wrap">
  <div class="top">
   <div><div class="eyebrow">Servicios disponibles</div><h2>Servicios especializados</h2>
   <p>A través de nuestros aliados, ponemos a tu disposición empresas especializadas para atender distintas necesidades empresariales.</p></div>
  </div>
  <div class="grid">
{cards}
  </div>
  <p class="more-note">Pronto se incorporarán más empresas especializadas.</p>
 </div>
</section>

<section class="process" id="como-funciona">
 <div class="wrap pgrid">
  <div><div class="eyebrow">Cómo funciona</div><h2>Un proceso simple y directo</h2></div>
  <div class="step"><div class="n">01</div><h3>Identificamos</h3><p>Las necesidades de las empresas y las oportunidades del mercado.</p></div>
  <div class="step"><div class="n">02</div><h3>Conectamos</h3><p>A la empresa con el proveedor especializado.</p></div>
  <div class="step"><div class="n">03</div><h3>Coordinamos</h3><p>La cita entre ambas partes para que puedan avanzar.</p></div>
 </div>
</section>

<section class="paths">
 <div class="path dark" id="empresas">
  <div class="eyebrow">Para empresas</div>
  <h2>¿Necesitas un servicio especializado?</h2>
  <p>Encuentra proveedores con experiencia en distintos sectores. En LINCONT te ayudamos a conectar con la mejor opción.</p>
  <a class="btn light" href="#servicios">Ver servicios <span aria-hidden="true">→</span></a>
 </div>
 <div class="path light" id="proveedores">
  <div class="eyebrow">Trabaja con LINCONT</div>
  <h2>¿Quieres trabajar con LINCONT?</h2>
  <p>Cierre de ventas, desarrollo de negocios o sumarte como empresa aliada. Cuéntanos qué necesita tu empresa.</p>
  <a class="btn ghost" href="trabaja-con-lincont.html">Quiero trabajar con LINCONT <span aria-hidden="true">→</span></a>
 </div>
</section>

<section class="allies">
 <div class="wrap agrid">
  <div><div class="eyebrow">Nuestros aliados</div><h2>Empresas que generan nuevas oportunidades</h2></div>
  <div class="ally"><b>Global EMC</b><span>Ingeniería eléctrica</span></div>
  <div class="ally"><b>Furgoservi</b><span>Furgones y estructuras</span></div>
  <div class="ally more">Más aliados en camino. Juntos ampliamos las oportunidades.</div>
 </div>
</section>

{contact_bar()}
</main>
""" + FOOT

def form(default):
    prov = next((x["provider"] for x in SERVICES if x["title"] == default), "el proveedor")
    opts = "".join(f'<option{" selected" if x["title"]==default else ""}>{html.escape(x["title"])}</option>' for x in SERVICES) + "<option>Otro servicio</option>"
    return f"""<section class="formbox" id="formulario">
 <div class="wrap fcols">
  <div>
   <div class="eyebrow">Agenda tu cita</div>
   <h2>Agenda una cita con {html.escape(prov)}</h2>
   <p style="margin-top:16px;opacity:.78">Cuéntanos qué necesitas y elige la fecha y el horario que te convengan. LINCONT confirma la cita y te indica cuándo y cómo asistir.</p>
  </div>
  <form id="interes" data-wa data-subject="Nueva solicitud de cita desde la página de LINCONT" data-intro="Hola, quiero agendar una cita con LINCONT para conocer a {html.escape(prov)}.">
   <div class="f"><label for="nombre">Nombre completo</label><input id="nombre" name="nombre" required autocomplete="name"></div>
   <div class="f"><label for="empresa">Empresa</label><input id="empresa" name="empresa" required autocomplete="organization"></div>
   <div class="f"><label for="cargo">Cargo</label><input id="cargo" name="cargo" autocomplete="organization-title"></div>
   <div class="f"><label for="correo">Correo electrónico</label><input id="correo" name="correo" type="email" required autocomplete="email"></div>
   <div class="f"><label for="telefono">Teléfono / WhatsApp</label><input id="telefono" name="telefono" type="tel" required autocomplete="tel"></div>
   <div class="f"><label for="servicio">Tipo de servicio que necesita</label><select id="servicio" name="servicio">{opts}</select></div>
   <div class="f full"><label for="ubicacion">Ubicación del proyecto</label><input id="ubicacion" name="ubicacion"></div>
   <div class="f full"><label for="mensaje">Cuéntanos brevemente qué necesitas</label><textarea id="mensaje" name="mensaje" required></textarea></div>
   <div class="f"><label for="fecha">Fecha preferida para la cita</label><input id="fecha" name="fecha" type="date" required></div>
   <div class="f"><label for="horario">Hora exacta</label><input id="horario" name="horario" type="time" required></div>
   <div class="f full"><label for="modalidad">Modalidad</label><select id="modalidad" name="modalidad"><option>Llamada telefónica</option><option>Presencial</option></select></div>
   <div class="full"><button class="btn filled" type="submit">Agendar cita <span aria-hidden="true">→</span></button></div>
   <p class="priv">La información proporcionada será utilizada únicamente para coordinar esta cita.</p>
   <div class="ok" role="status"></div>
  </form>
 </div>
</section>
"""

def service_page(s, subtitle, provider_html, services_html, lead):
    return head(f"{s['title']} – LINCONT", s["short"]) + header(False) + f"""<main id="main">
<section class="phero">
 <div class="wrap">
  <p class="crumbs"><a href="index.html">Inicio</a> / <a href="index.html#servicios">Servicios</a> / {html.escape(s['title'])}</p>
  <div class="eyebrow">Servicios especializados</div>
  <h1>{html.escape(s['title'])}</h1>
  <p class="lead">{lead}</p>
 </div>
</section>
{provider_html}
{services_html}
{form(s['title'])}
{contact_bar()}
</main>
""" + FOOT

GLOBAL_SERVICES = [
 "Instalaciones eléctricas en baja y media tensión.",
 "Montaje, conexionado y armado de equipos eléctricos industriales.",
 "Diseño y montaje de subestaciones eléctricas de baja y media tensión.",
 "Ingeniería de diseño para instalaciones industriales, comerciales, residenciales y líneas de distribución.",
 "Estudios de iluminación para ambientes interiores y exteriores.",
 "Estudios de calidad de energía: voltajes, corrientes, potencia, factor de potencia y armónicos.",
 "Cálculo, diseño e instalación de sistemas de puesta a tierra y protección contra descargas atmosféricas.",
 "Automatización de plantas industriales: instrumentación, calibración, cableado y pruebas.",
 "Montaje de líneas eléctricas de media tensión (46 kV y 13.2 kV).",
 "Pruebas de diagnóstico y mantenimiento de equipos, como transformadores de potencia e interruptores.",
 "Cálculo, diseño e instalación de sistemas de refrigeración y aire acondicionado.",
 "Mantenimiento preventivo y correctivo de sistemas eléctricos.",
 "Proyectos llave en mano, desde la planificación hasta la puesta en marcha.",
]

def join_page():
    roles = [
     ("Cierre de ventas", "check", "Para empresas que ya tienen clientes interesados, pero pierden ventas antes de cerrar.",
      ["Atención a los clientes interesados", "Explicación clara de tu oferta", "Seguimiento hasta concretar la venta"]),
     ("Desarrollo de negocios", "layers", "Para empresas que quieren llegar a nuevos clientes y abrir nuevas oportunidades.",
      ["Identificación de oportunidades comerciales", "Contacto con quienes necesitan lo que ofreces", "Red de aliados como Global EMC y Furgoservi"]),
    ]
    cards = "".join(
      f'<article class="jcard r" style="--d:{i}"><div class="jic">{ico(ic)}</div><div class="jn">0{i+1}</div><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p>'
      f'<ul>{"".join("<li>"+html.escape(x)+"</li>" for x in bl)}</ul>'
      f'<button type="button" class="btn filled" data-rol="{html.escape(t)}">Quiero este servicio <span aria-hidden="true">→</span></button></article>'
      for i, (t, ic, d, bl) in enumerate(roles))
    opts = "".join(f"<option>{html.escape(t)}</option>" for t, _, _, _ in roles)
    hdr = header(False).replace("assets/lincont-logo.png", "assets/lincont-logo-negativo.png", 1)
    foot = FOOT.replace("assets/lincont-logo.png", "assets/lincont-logo-negativo.png", 1).replace("</footer>", "</footer></div>", 1)
    return head("Trabaja con LINCONT", "Contrata a LINCONT para cierre de ventas y desarrollo de negocios.") + '<div class="tp theme-join">' + hdr + f"""<main id="main">
<section class="jh">
 <div class="jbg" aria-hidden="true"><img src="assets/lincont-c.svg" alt=""><i></i><i></i><i></i></div>
 <div class="wrap jh-in">
  <p class="crumbs"><a href="index.html">Inicio</a> / Trabaja con LINCONT</p>
  <div class="eyebrow">Trabaja con LINCONT</div>
  <h1>Hagamos crecer<br>tu empresa.</h1>
  <p class="lead">Elige el servicio que necesitas. LINCONT te acompaña a cerrar más ventas y a encontrar nuevas oportunidades de negocio.</p>
  <a class="btn filled" href="#servicios">Ver servicios <span aria-hidden="true">↓</span></a>
 </div>
</section>
<section class="sec" id="servicios"><div class="wrap">
 <div class="jtitle r"><div class="eyebrow">Servicios</div><h2>¿Qué necesita tu empresa?</h2></div>
 <div class="jgrid">{cards}</div>
</div></section>
<section class="sec alt"><div class="wrap">
 <div class="jtitle r"><div class="eyebrow">Cómo trabajamos</div><h2>Tres pasos, sin complicaciones</h2></div>
 <div class="jsteps">
  <div class="jstep r" style="--d:0"><span>01</span><h3>Nos cuentas</h3><p>Completas el formulario con lo que tu empresa necesita.</p></div>
  <div class="jstep r" style="--d:1"><span>02</span><h3>Conversamos</h3><p>LINCONT te contacta para entender tu caso y acordar cómo trabajar.</p></div>
  <div class="jstep r" style="--d:2"><span>03</span><h3>Avanzamos</h3><p>Las condiciones se acuerdan por escrito antes de empezar.</p></div>
 </div>
</div></section>
<section class="formbox" id="formulario">
 <div class="wrap fcols">
  <div><div class="eyebrow">Solicitud de contacto</div><h2>Cuéntanos sobre tu empresa</h2>
  <p style="margin-top:16px;opacity:.78">Te respondemos para conversar y ver cómo podemos ayudarte.</p></div>
  <form id="unete" data-wa data-subject="Nueva solicitud de trabajo con LINCONT" data-intro="Hola, mi empresa quiere trabajar con LINCONT.">
   <div class="f"><label for="nombre">Nombre completo</label><input id="nombre" required autocomplete="name"></div>
   <div class="f"><label for="empresa">Empresa</label><input id="empresa" required autocomplete="organization"></div>
   <div class="f"><label for="telefono">Teléfono / WhatsApp</label><input id="telefono" type="tel" required autocomplete="tel"></div>
   <div class="f"><label for="correo">Correo electrónico</label><input id="correo" type="email" autocomplete="email"></div>
   <div class="f full"><label for="rol">Servicio que me interesa</label><select id="rol">{opts}</select></div>
   <div class="f full"><label for="mensaje">Cuéntanos brevemente qué necesitas</label><textarea id="mensaje" required></textarea></div>
   <div class="full"><button class="btn filled" type="submit">Enviar solicitud <span aria-hidden="true">→</span></button></div>
   <p class="priv">La información proporcionada será utilizada únicamente para gestionar esta solicitud.</p>
   <div class="ok" role="status"></div>
  </form>
 </div>
</section>
{contact_bar()}
</main>
<script>
document.querySelectorAll('[data-rol]').forEach(function(b){{b.addEventListener('click',function(){{var s=document.getElementById('rol');if(s)s.value=b.dataset.rol;document.getElementById('formulario').scrollIntoView({{behavior:'smooth'}})}})}});
</script>
""" + foot


def ico(name):
    P = {
     "bolt":'<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
     "check":'<path d="m9 11 3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
     "shield":'<path d="M12 2 4 5v6c0 5 3.5 9 8 11 4.5-2 8-6 8-11V5z"/><path d="m8.5 12 2.5 2.5L16 9.5"/>',
     "users":'<path d="M9 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/><path d="M2 21c0-4 3-6 7-6s7 2 7 6"/><path d="M17 4.5a3.5 3.5 0 0 1 0 6.5M18 15c3 .5 4 2.5 4 6"/>',
     "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
     "truck":'<path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>',
     "wrench":'<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
     "sliders":'<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
     "layers":'<path d="m12 2-10 5 10 5 10-5z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
    }
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true">{P[name]}</svg>'

BOLT = """<svg class="motif bolt" viewBox="0 0 400 520" aria-hidden="true"><path class="draw" d="M236 12 L84 290 H196 L156 508 L330 208 H214 Z"/><path class="draw d2" d="M236 12 L84 290 H196 L156 508 L330 208 H214 Z" transform="translate(14 10)"/></svg>"""
VAN = """<svg class="motif van" viewBox="0 0 640 300" aria-hidden="true">
<path class="draw" d="M24 52Q24 38 38 38H392Q406 38 406 52V208H24Z"/>
<path class="draw d2" d="M84 44V204M144 44V204M204 44V204M264 44V204M324 44V204"/>
<path class="draw" d="M412 208V90Q412 68 434 68H500Q516 68 528 82L574 132Q584 144 584 158V208Z"/>
<path class="draw d2" d="M440 88H494L540 134H440Z"/>
<path class="draw" d="M440 140V200M452 166H464"/>
<path class="draw" d="M402 96H414V120H402Z"/>
<path class="draw" d="M584 168H596V182H584Z"/>
<path class="draw" d="M16 208H596V224H16Z"/>
<path class="draw" d="M586 224H604Q610 224 610 218V212"/>
<path class="draw" d="M96 224A44 44 0 0 1 184 224M456 224A44 44 0 0 1 544 224"/>
<path class="draw d2" d="M24 176H34V192H24Z"/>
<g class="wheel" style="transform-origin:140px 238px"><circle class="tire" cx="140" cy="238" r="30"/><circle cx="140" cy="238" r="11"/><path d="M140 210V266M112 238H168M120 218L160 258M160 218L120 258"/></g><g class="wheel" style="transform-origin:500px 238px"><circle class="tire" cx="500" cy="238" r="30"/><circle cx="500" cy="238" r="11"/><path d="M500 210V266M472 238H528M480 218L520 258M520 218L480 258"/></g>
<path class="road" d="M0 276H640"/>
<path class="speed s1" d="M-30 110H-4"/><path class="speed s2" d="M-50 150H-14"/><path class="speed s3" d="M-24 190H-2"/>
</svg>"""

def provider_page(s, theme, hero, body):
    hdr = header(False).replace("assets/lincont-logo.png", "assets/lincont-logo-negativo.png", 1)
    foot = FOOT.replace("assets/lincont-logo.png", "assets/lincont-logo-negativo.png", 1).replace("</footer>", "</footer></div>", 1)
    return head(f"{s['title']} – LINCONT", s["short"]) + f'<div class="tp {theme}">' + hdr + f'<main id="main">\n{hero}\n{body}\n{form(s["title"])}\n{contact_bar()}\n</main>\n' + foot

def pv_hero(theme, motif, kicker, name, tagline, intro, site, stats=""):
    return f"""<section class="pv {theme}">
 {motif}
 <div class="wrap pv-in">
  <p class="crumbs"><a href="index.html">Inicio</a> / <a href="index.html#servicios">Servicios</a> / {html.escape(name)}</p>
  <div class="eyebrow">Aliado de LINCONT · {html.escape(kicker)}</div>
  <h1>{html.escape(name)}</h1>
  <p class="pv-tag">{html.escape(tagline)}</p>
  <p class="lead">{intro}</p>
  <div class="cta"><a class="btn filled" href="#formulario">Agendar cita <span aria-hidden="true">→</span></a>{site}</div>
  {stats}
 </div>
</section>"""

def emc_page():
    s = SERVICES[0]
    stats = """<dl class="stats">
   <div><dt data-count="7" data-suf="+">7+</dt><dd>años de experiencia</dd></div>
   <div><dt data-count="200" data-suf="+">200+</dt><dd>proyectos ejecutados</dd></div>
   <div><dt data-count="50" data-suf="+">50+</dt><dd>clientes satisfechos</dd></div>
   <div><dt>24/7</dt><dd>emergencias eléctricas en todo el país</dd></div>
  </dl>
  <p class="src">Cifras informadas por Global EMC.</p>"""
    hero = pv_hero("theme-emc", BOLT, "Ingeniería eléctrica", "Global EMC S.A.",
        "Servicios profesionales de ingeniería eléctrica",
        "Nace en 2017 para brindar servicios de ingeniería eléctrica. Planifica, desarrolla y ejecuta proyectos eléctricos industriales y comerciales, desde el diseño y montaje hasta la automatización de sistemas.",
        "", stats)
    feats = [("check","Proyectos llave en mano","Planificación, diseño, ejecución y puesta en marcha. Dimensionamiento, suministro y montaje de equipos y materiales."),
             ("shield","Ingeniería de calidad","Trabajo bajo normas y estándares locales e internacionales."),
             ("users","Equipo especializado","Talento humano capacitado, con amplio conocimiento en la rama eléctrica."),
             ("clock","Disponibilidad 24/7","Capacidad de cubrir emergencias eléctricas en todo el país.")]
    fh = "".join(f'<article class="feat">{ico(i)}<h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></article>' for i, t, d in feats)
    svc = "".join(f"<li>{html.escape(x)}</li>" for x in [
     "Instalaciones eléctricas en baja y media tensión.",
     "Montaje, conexionado y armado de equipos eléctricos industriales.",
     "Diseño y montaje de subestaciones eléctricas de baja y media tensión.",
     "Ingeniería de diseño para instalaciones industriales, comerciales, residenciales y líneas de distribución.",
     "Estudios de iluminación para ambientes interiores y exteriores.",
     "Estudios de calidad de energía: voltajes, corrientes, factor de potencia y armónicos.",
     "Diseño e instalación de sistemas de puesta a tierra y protección contra descargas atmosféricas.",
     "Automatización de plantas industriales: instrumentación, calibración, cableado y pruebas.",
     "Montaje de líneas eléctricas de media tensión (46 kV y 13.2 kV).",
     "Pruebas de diagnóstico y mantenimiento de equipos, como transformadores de potencia e interruptores.",
     "Diseño e instalación de sistemas de refrigeración y aire acondicionado.",
     "Mantenimiento preventivo y correctivo de sistemas eléctricos."])
    projs = [("Industria de gaseosas","Subestación de 5 MVA","Montaje de subestación de 5 MVA (46 kV / 13.2 kV): transformador principal, equipos de subestación, celda de media tensión y tableros principales 480 V / 120 V."),
      ("Industria del arroz","Subestación de 2 MVA","Suministro de equipos, montaje y puesta en marcha: transformadores secos, celda de media tensión, generador de emergencia, transferencias y tableros de 480 V."),
      ("Telecomunicaciones","Montaje de data center","Suministro de materiales y mano de obra: 2 transformadores de 3 MVA, ducto barra de 3,000 A, tren de celdas de media tensión de 4 módulos, gabinetes de 480 V / 3,000 A y sistemas críticos (UPS)."),
      ("Industria de snacks","Línea de producción de snacks de maíz","Proyecto llave en mano: tableros, canalización con tubería especial para ambientes corrosivos, cableado de potencia y control, y conexionado de PLC (Point I/O)."),
      ("Agroindustria","Automatización de silos de maíz","Suministro y programación de PLC Allen Bradley y variadores para motores de 40 a 50 HP, y puesta en marcha de sistema Wonderware.")]
    ph = "".join(f'<article class="proj"><span class="tagl">{html.escape(a)}</span><h3>{html.escape(b)}</h3><p>{html.escape(c)}</p></article>' for a, b, c in projs)
    body = f"""<section class="sec alt"><div class="wrap"><div class="eyebrow">Por qué Global EMC</div><h2 style="margin-bottom:34px">Experiencia técnica de punta a punta</h2><div class="feats">{fh}</div></div></section>
<section class="sec"><div class="wrap"><div class="eyebrow">Servicios</div><h2 style="margin-bottom:34px">Lo que ofrece Global EMC</h2><ul class="list">{svc}</ul></div></section>
<section class="sec alt"><div class="wrap"><div class="eyebrow">Proyectos relevantes</div><h2 style="margin-bottom:12px">Obras que respaldan su trabajo</h2><p style="opacity:.78;margin-bottom:34px">Proyectos informados por Global EMC.</p><div class="projs">{ph}</div>
<p class="note">LINCONT no ejecuta estos servicios. Los presta directamente Global EMC; LINCONT coordina la cita entre ambas partes.</p></div></section>"""
    return provider_page(s, "theme-emc", hero, body)

def furgo_page():
    s = SERVICES[1]
    hero = pv_hero("theme-furgo", VAN, "Furgones y estructuras metálicas", "Furgoservi",
        "Fabricación, reparación y modificación de furgones",
        "Soluciones en furgones, estructuras metálicas y trabajos personalizados para proyectos empresariales.", "")
    items = [("truck","Fabricación","Furgones hechos para las necesidades de tu negocio."),("wrench","Reparación","Reparación de furgones."),("sliders","Modificación","Modificación de furgones existentes."),("layers","Estructuras metálicas","Estructuras y soluciones personalizadas para proyectos empresariales.")]
    fh = "".join(f'<article class="feat">{ico(i)}<h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></article>' for i, t, d in items)
    body = f"""<section class="sec alt"><div class="wrap"><div class="eyebrow">Nuestros servicios</div><h2 style="margin-bottom:34px">Lo que hace Furgoservi</h2><div class="feats">{fh}</div>
<p class="note">Furgoservi se incorpora a la oferta de LINCONT. Si necesitas este servicio, agenda una cita y la coordinamos.</p></div></section>"""
    return provider_page(s, "theme-furgo", hero, body)

def pages():
    out = {"index.html": index()}
    g = SERVICES[0]
    prov = """<section class="sec alt"><div class="wrap two">
 <div><div class="eyebrow">Sobre el proveedor</div><h2>Global EMC</h2></div>
 <div>
  <p>Global EMC S.A. es una empresa de servicios profesionales de ingeniería eléctrica. Se fundó en 2017 y se especializa en planificar, desarrollar y ejecutar proyectos eléctricos industriales y comerciales.</p>
  <p>Atiende industrias, comercios, constructoras y desarrolladoras, y su sede está en la Ciudad de Guatemala.</p>
  <p class="note">LINCONT no ejecuta estos servicios. Los presta directamente Global EMC; LINCONT coordina la cita entre ambas partes.</p>
 </div></div></section>"""
    svc = '<section class="sec"><div class="wrap"><div class="eyebrow">Servicios</div><h2 style="margin-bottom:34px">Lo que ofrece Global EMC</h2><ul class="list">' + "".join(f"<li>{html.escape(x)}</li>" for x in GLOBAL_SERVICES) + "</ul></div></section>"
    out[g["file"]] = service_page(g, "", prov, svc, "Servicios especializados para proyectos empresariales, prestados por nuestro aliado Global EMC.")
    f = SERVICES[1]
    prov2 = """<section class="sec alt"><div class="wrap two">
 <div><div class="eyebrow">Sobre el proveedor</div><h2>Furgoservi</h2></div>
 <div>
  <p>Furgoservi se incorporará como parte de la oferta de LINCONT. Está orientada a la fabricación y modificación de furgones, estructuras metálicas y soluciones personalizadas para proyectos empresariales.</p>
  <p class="note">La información detallada de este proveedor se publicará próximamente. Si ya necesitas este servicio, déjanos tus datos y te contactamos.</p>
 </div></div></section>"""
    out[f["file"]] = service_page(f, "", prov2, "", "Fabricación y modificación de furgones, estructuras metálicas y soluciones personalizadas para proyectos empresariales.")
    out[SERVICES[0]["file"]] = emc_page()
    out[SERVICES[1]["file"]] = furgo_page()
    out["trabaja-con-lincont.html"] = join_page()
    return out

if __name__ == "__main__":
    for name, content in pages().items():
        (ROOT / name).write_text(content, encoding="utf-8")
        print("escrito", name)
