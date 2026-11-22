const dialog=document.querySelector('#applyDialog');
const uk=document.documentElement.lang==='uk';
const form=document.querySelector('#leadForm');const status=document.querySelector('.form-status');
if (!uk) {
  for (const button of document.querySelectorAll('button.js-open')) {
    const link = document.createElement('a');
    link.className = button.className.replace(/\bjs-open\b/, '').trim();
    link.href = 'https://www.paypal.com/ncp/payment/9NMLUDSDL2A7L';
    link.append(...button.childNodes);
    button.replaceWith(link);
  }
}
document.addEventListener('click',event=>{const trigger=event.target.closest('.js-open');if(!trigger)return;event.preventDefault();if(typeof dialog.showModal==='function'){if(!dialog.open)dialog.showModal()}else{dialog.setAttribute('open','')}});
document.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});

form.addEventListener('submit',async event=>{
  event.preventDefault();
  const submit=form.querySelector('button[type="submit"]');
  submit.disabled=true;
  status.textContent=uk?'Надсилаємо заявку…':'Sending your join request…';
  try{
    const payload=Object.fromEntries(new FormData(form));
    delete payload._subject;
    delete payload._captcha;
    payload.access_key='54d405a9-39f1-41cc-8263-276e0ebaf3c6';
    payload.subject='Ship Index Grow — course enrollment';
    payload.from_name='Ship Index Grow';
    payload.page=window.location.href;
    const response=await fetch('https://api.web3forms.com/submit',{
      method:'POST',
      headers:{'Content-Type':'application/json','Accept':'application/json'},
      body:JSON.stringify(payload)
    });
    const result=await response.json();
    if(!response.ok||result.success!==true&&result.success!=='true')throw new Error(result.message||'Request failed');
    form.reset();
    status.textContent=uk?'Заявку надіслано. Напишемо на твою пошту з датами та наступним кроком.':'Request sent. We’ll email you with the cohort dates and next step.';
  }catch(error){
    console.error('Join request failed',error);
    status.textContent=uk?'Не вдалося надіслати. Напиши на theolehhebel@gmail.com.':'Could not send right now. Email theolehhebel@gmail.com directly.';
  }finally{
    submit.disabled=false;
  }
});

// Preserve the current section when changing language. Links work without JavaScript.
document.querySelectorAll('.language-switch a').forEach(link=>link.addEventListener('click',()=>{if(window.location.hash)link.href+=window.location.hash}));
