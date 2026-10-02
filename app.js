const dialog=document.querySelector('#applyDialog');
const uk=document.documentElement.lang==='uk';
const form=document.querySelector('#leadForm');const status=document.querySelector('.form-status');
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
    payload._url=window.location.href;
    const response=await fetch('https://formsubmit.co/ajax/doctorgebel@gmail.com',{
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
    status.textContent=uk?'Не вдалося надіслати. Напиши на doctorgebel@gmail.com.':'Could not send right now. Email doctorgebel@gmail.com directly.';
  }finally{
    submit.disabled=false;
  }
});

// Preserve the current section when changing language. Links work without JavaScript.
document.querySelectorAll('.language-switch a').forEach(link=>link.addEventListener('click',()=>{if(window.location.hash)link.href+=window.location.hash}));
