/* Typography: e-Ukraine / e-Ukraine Head. Typeface by Dmytro Rastvortsev / Fedoriv Agency for Ukraine's digital-state identity. CC BY 4.0. Official reference: https://thedigital.gov.ua/fonts */
const typographyStyle=document.createElement('style');typographyStyle.textContent=`@font-face{font-family:'e-Ukraine';src:url('https://cdn.jsdelivr.net/gh/bennetfabian/e-Ukraine@main/e-Ukraine-Regular.otf') format('opentype');font-style:normal;font-weight:400;font-display:swap}@font-face{font-family:'e-Ukraine';src:url('https://cdn.jsdelivr.net/gh/bennetfabian/e-Ukraine@main/e-Ukraine-Medium.otf') format('opentype');font-style:normal;font-weight:500;font-display:swap}@font-face{font-family:'e-Ukraine';src:url('https://cdn.jsdelivr.net/gh/bennetfabian/e-Ukraine@main/e-Ukraine-Bold.otf') format('opentype');font-style:normal;font-weight:700;font-display:swap}@font-face{font-family:'e-Ukraine';src:url('https://cdn.jsdelivr.net/gh/bennetfabian/e-Ukraine@main/e-Ukraine-Bold.otf') format('opentype');font-style:normal;font-weight:800;font-display:swap}@font-face{font-family:'e-Ukraine Head';src:url('https://cdn.jsdelivr.net/gh/bennetfabian/e-Ukraine@main/e-UkraineHead-Bold.otf') format('opentype');font-style:normal;font-weight:700;font-display:swap}@font-face{font-family:'e-Ukraine Head';src:url('https://cdn.jsdelivr.net/gh/bennetfabian/e-Ukraine@main/e-UkraineHead-Bold.otf') format('opentype');font-style:normal;font-weight:800;font-display:swap}body,button,input,textarea,select{font-family:'e-Ukraine',Arial,Helvetica,sans-serif}.hero h1,.section h2,.final h2,.dialog-copy h2,.steps h3,.outcome article h3,.proof-grid h3,.faq-grid h3,.format-grid strong{font-family:'e-Ukraine Head','e-Ukraine',Arial,Helvetica,sans-serif}`;document.head.appendChild(typographyStyle);

const conversionStyle=document.createElement('style');conversionStyle.textContent=`.proof-grid a{position:relative;overflow:hidden}.project-logo-wrap{position:absolute;right:24px;top:24px;width:66px;height:66px;border:1px solid var(--line);border-radius:18px;background:#fff;display:grid;place-items:center;padding:8px;transition:transform .2s}.project-logo{display:block;width:100%;height:100%;object-fit:contain}.proof-grid a:hover .project-logo-wrap{transform:translateY(-2px) rotate(2deg)}.proof-grid a>span:first-child{max-width:calc(100% - 92px)}.dialog-copy{padding-bottom:18px}.dialog-offer{font-size:18px!important;line-height:1.45;margin:22px 0 0;max-width:560px}.dialog-offer strong{color:var(--blue)}.dialog-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}.dialog-meta span{border:1px solid #bbb;border-radius:999px;padding:8px 11px;font-size:11px;font-weight:800;letter-spacing:.06em}.dialog-proof{display:flex;flex-wrap:wrap;gap:10px 16px;padding:0 40px 34px;font-size:12px;font-weight:800}.dialog-proof a{color:inherit;text-decoration:none;border-bottom:1px solid #bbb}.dialog-proof a:hover{color:var(--blue);border-color:var(--blue)}.dialog-price-note{font-size:12px;color:var(--muted);margin:0}.footer-social{white-space:nowrap}@media(max-width:520px){.project-logo-wrap{right:18px;top:18px;width:56px;height:56px;border-radius:15px}.proof-grid a>span:first-child{max-width:calc(100% - 74px)}.dialog-meta{gap:6px}.dialog-meta span{font-size:10px}.dialog-proof{padding:0 22px 28px}}`;document.head.appendChild(conversionStyle);

const FOUNDING_PRICE='$490';
const ctas=[...document.querySelectorAll('.js-open')];
if(ctas[0])ctas[0].textContent='Join the course';
if(ctas[1])ctas[1].innerHTML='Join the course <span>↗</span>';
if(ctas[2])ctas[2].innerHTML='Join the founding cohort <span>↗</span>';

const heroMeta=[...document.querySelectorAll('.hero-meta span')];
['20 SEATS','6 LIVE WEEKS',`${FOUNDING_PRICE} FOUNDING PRICE`,'ONE PRODUCT PER STUDENT'].forEach((text,index)=>{if(heroMeta[index])heroMeta[index].textContent=text});

const proofLogos=[
  {host:'interfacereport.com',src:'https://raw.githubusercontent.com/olehhebel/interface-report-media/main/assets/interface-report-logo.png',alt:'Interface Report logo'},
  {host:'ridne.store',src:'https://raw.githubusercontent.com/olehhebel/ridne-marketplace/main/assets/ridne-logo-2026.webp',alt:'RIDNE logo'},
  {host:'superprompt.pro',src:'https://raw.githubusercontent.com/olehhebel/ai-superprompt-studio/index.html/assets/network/oleh-hebel-co-v2.png',alt:'Oleh Hebel & Co logo'}
];
document.querySelectorAll('.proof-grid a').forEach(card=>{const logo=proofLogos.find(item=>card.href.includes(item.host));if(!logo||card.querySelector('.project-logo-wrap'))return;const wrap=document.createElement('span');wrap.className='project-logo-wrap';wrap.innerHTML=`<img class="project-logo" src="${logo.src}" alt="${logo.alt}" loading="lazy" decoding="async">`;card.appendChild(wrap)});

const formatItems=[...document.querySelectorAll('.format-grid div')];
if(formatItems[0]){formatItems[0].querySelector('strong').textContent='20';formatItems[0].querySelector('span').textContent='founding cohort seats'}
if(formatItems[1]){formatItems[1].querySelector('strong').textContent='6';formatItems[1].querySelector('span').textContent='live working weeks'}
if(formatItems[2]){formatItems[2].querySelector('strong').textContent='20+';formatItems[2].querySelector('span').textContent='real products launched'}
const formatNote=document.querySelector('.format-note');if(formatNote)formatNote.textContent=`Twenty people enter with twenty different ideas. Each participant leaves with a live product, its own domain, search-ready structure and a concrete growth plan. Founding cohort: ${FOUNDING_PRICE} for the full six-week program.`;

const faqGrid=document.querySelector('.faq-grid');if(faqGrid&&!faqGrid.querySelector('[data-pricing-faq]')){const pricing=document.createElement('article');pricing.dataset.pricingFaq='true';pricing.innerHTML=`<h3>What does the founding cohort cost?</h3><p><strong>${FOUNDING_PRICE} total</strong> for six live weeks, product reviews, templates, SEO/GEO guidance and launch feedback. The first cohort is limited to 20 seats.</p>`;faqGrid.appendChild(pricing)}

const finalCopy=document.querySelector('.final>p:not(.eyebrow)');if(finalCopy)finalCopy.textContent=`20 seats. Six live weeks. One real launch per participant. Founding cohort price: ${FOUNDING_PRICE}.`;

const footer=document.querySelector('footer');if(footer&&!footer.querySelector('.footer-social')){const linkedin=document.createElement('a');linkedin.className='footer-link footer-social';linkedin.href='https://www.linkedin.com/in/olehhebel/';linkedin.target='_blank';linkedin.rel='noopener';linkedin.textContent='LinkedIn ↗';const copyright=footer.lastElementChild;if(copyright){footer.insertBefore(linkedin,copyright)}else{footer.appendChild(linkedin)}}

const dialog=document.querySelector('#applyDialog');
dialog.innerHTML=`
  <button class="dialog-close" type="button" aria-label="Close join form">×</button>
  <div class="dialog-copy">
    <p class="eyebrow">SHIP INDEX GROW · FOUNDING COHORT</p>
    <h2 id="dialogTitle">Ready to build something real?</h2>
    <p class="dialog-offer">Join the six-week Ship Index Grow cohort and take one real product from idea to launch — product strategy, UX, AI build, SEO/GEO, growth and automation. <strong>${FOUNDING_PRICE} total.</strong></p>
    <div class="dialog-meta" aria-label="Course details"><span>6 LIVE WEEKS</span><span>20 SEATS</span><span>YOUR PRODUCT GOES LIVE</span></div>
  </div>
  <form id="leadForm">
    <input type="hidden" name="_subject" value="SHIP INDEX GROW — NEW JOIN REQUEST">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="request_type" value="I want to join the Ship Index Grow founding cohort">
    <input type="hidden" name="course" value="Ship Index Grow — 6-week founding cohort">
    <input type="hidden" name="price" value="${FOUNDING_PRICE}">
    <label>Your name<input name="name" autocomplete="name" required placeholder="Your name"></label>
    <label>Your email<input name="email" type="email" autocomplete="email" required placeholder="you@example.com"></label>
    <button class="button" type="submit">I want to join <span>→</span></button>
    <p class="dialog-price-note">Two fields. No long application. You send the signal — I send the next step.</p>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
  <div class="dialog-proof"><span>BUILT IN PUBLIC:</span><a href="https://superprompt.pro/" target="_blank" rel="noopener">Oleh Hebel & Co ↗</a><a href="https://interfacereport.com/" target="_blank" rel="noopener">Interface Report ↗</a><a href="https://ridne.store/" target="_blank" rel="noopener">RIDNE ↗</a><a href="https://www.linkedin.com/in/olehhebel/" target="_blank" rel="noopener">LinkedIn ↗</a></div>`;

const form=document.querySelector('#leadForm');const status=document.querySelector('.form-status');
document.addEventListener('click',event=>{const trigger=event.target.closest('.js-open');if(!trigger)return;event.preventDefault();if(typeof dialog.showModal==='function'){if(!dialog.open)dialog.showModal()}else{dialog.setAttribute('open','')}});
document.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});

form.addEventListener('submit',async event=>{event.preventDefault();const submit=form.querySelector('button[type="submit"]');submit.disabled=true;status.textContent='Sending your join request…';try{const payload=Object.fromEntries(new FormData(form));const response=await fetch('https://formsubmit.co/ajax/doctorgebel@gmail.com',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(payload)});if(!response.ok)throw new Error('Request failed');form.reset();status.textContent='Request sent. I’ll email you with the cohort dates and next step.'}catch(error){status.textContent='Could not send right now. Email doctorgebel@gmail.com directly.'}finally{submit.disabled=false}});