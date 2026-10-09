const dialog=document.querySelector('#applyDialog');
const uk=document.documentElement.lang==='uk';
const form=document.querySelector('#leadForm');const status=document.querySelector('.form-status');
document.addEventListener('click',event=>{const trigger=event.target.closest('.js-open');if(!trigger)return;event.preventDefault();if(typeof dialog.showModal==='function'){if(!dialog.open)dialog.showModal()}else{dialog.setAttribute('open','')}});
document.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});

// Telegram relay (Google Apps Script web app, see tools/telegram-leads).
// Leave empty to send join requests by email only.
const TELEGRAM_RELAY_URL='';

async function postJson(url,payload,headers){
  const response=await fetch(url,{method:'POST',headers,body:JSON.stringify(payload)});
  return {response,result:await response.json().catch(()=>({}))};
}
async function sendLead(payload){
  if(TELEGRAM_RELAY_URL){
    try{
      // text/plain keeps this a simple request, which Apps Script accepts cross-origin.
      const {response,result}=await postJson(TELEGRAM_RELAY_URL,payload,{'Content-Type':'text/plain;charset=utf-8'});
      if(response.ok&&result.ok===true)return;
      throw new Error(result.error||'Telegram relay failed');
    }catch(error){
      console.warn('Telegram lead delivery failed, using email fallback',error);
    }
  }
  const {response,result}=await postJson('https://formsubmit.co/ajax/doctorgebel@gmail.com',payload,{'Content-Type':'application/json','Accept':'application/json'});
  if(!response.ok||result.success!==true&&result.success!=='true')throw new Error(result.message||'Request failed');
}

form.addEventListener('submit',async event=>{
  event.preventDefault();
  const submit=form.querySelector('button[type="submit"]');
  submit.disabled=true;
  status.textContent=uk?'Надсилаємо заявку…':'Sending your join request…';
  try{
    const payload=Object.fromEntries(new FormData(form));
    payload._url=window.location.href;
    await sendLead(payload);
    form.reset();
    status.textContent=uk?'Заявку надіслано. Напишемо на твою пошту з датами та наступним кроком.':'Request sent. We’ll email you with the cohort dates and next step.';
  }catch(error){
    console.error('Join request failed',error);
    status.textContent=uk?'Не вдалося надіслати. Напиши на doctorgebel@gmail.com.':'Could not send right now. Email doctorgebel@gmail.com directly.';
  }finally{
    submit.disabled=false;
  }
});

// Preserve the current section when changing language. Links work without JavaScript.
document.querySelectorAll('.language-switch a').forEach(link=>link.addEventListener('click',()=>{if(window.location.hash)link.href+=window.location.hash}));
