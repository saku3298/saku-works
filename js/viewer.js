/* SAKU作品集 マンガリーダー（全作品共通） */
(function(){
 const viewer=document.querySelector('.viewer');
 if(!viewer) return;
 let originals=[...viewer.querySelectorAll('.manga-page')];
 if(!originals.length) return;
 const counter=document.getElementById('counter');
 const topBtn=document.getElementById('top');
 const prevBtn=document.getElementById('prev');
 const nextBtn=document.getElementById('next');
 const endSlide=document.createElement('div');
 endSlide.className='reader-slide end';endSlide.dataset.start=String(originals.length);endSlide.dataset.end=String(originals.length);
 endSlide.appendChild(document.getElementById('end-template').content.cloneNode(true));
 let slides=[],index=0,currentPage=0,landscape=false;
 let startX=0,startY=0,dx=0,dragging=false,axis=null,animating=false;

 function isLandscape(){return window.innerWidth > window.innerHeight;}
 function build(){
  currentPage=slides[index]?Number(slides[index].dataset.start||0):currentPage;
  viewer.innerHTML='';slides=[];landscape=isLandscape();
  if(landscape){
   const makeBlank=()=>{const blank=document.createElement('div');blank.className='manga-page blank-page';blank.setAttribute('aria-hidden','true');return blank;};
   const addSpread=(rightPage,leftPage,start,end)=>{const slide=document.createElement('div');slide.className='reader-slide spread';slide.dataset.start=String(start);slide.dataset.end=String(end);slide.appendChild(rightPage);slide.appendChild(leftPage);viewer.appendChild(slide);slides.push(slide);};
   addSpread(makeBlank(),originals[0],0,0);
   let i=1;
   for(;i+1<originals.length;i+=2) addSpread(originals[i],originals[i+1],i,i+1);
   if(i<originals.length) addSpread(originals[i],makeBlank(),i,i);
   viewer.appendChild(endSlide);slides.push(endSlide);
   index=slides.findIndex(slide=>{const start=Number(slide.dataset.start),end=Number(slide.dataset.end);return currentPage>=start&&currentPage<=end;});
   if(index<0) index=0;
  }else{
   originals.forEach((page,i)=>{const slide=document.createElement('div');slide.className='reader-slide single';slide.dataset.start=String(i);slide.appendChild(page);viewer.appendChild(slide);slides.push(slide);});
   viewer.appendChild(endSlide);slides.push(endSlide);
   index=Math.min(currentPage,slides.length-1);
  }
  prepare();
 }
 function updateCounter(){
  const start=Number(slides[index]?.dataset.start||0);currentPage=start;
  const end=Number(slides[index]?.dataset.end||start);
  const total=originals.length,isEnd=start>=total;
  if(counter)counter.textContent=isEnd?'おわり':((landscape&&end>start)?(start+1)+'-'+(end+1):(start+1))+' / '+total;
  const fill=document.getElementById('progress-fill');
  if(fill)fill.style.width=(isEnd?100:(end+1)/total*100)+'%';
 }
 function fitPortraitHeight(){
  if(landscape)return;
  const s=slides[index];if(!s)return;
  const img=s.querySelector('img');
  const apply=()=>{viewer.style.height=s.offsetHeight+'px';};
  if(img&&img.complete)requestAnimationFrame(apply);
  else if(img)img.addEventListener('load',()=>requestAnimationFrame(apply),{once:true});
  else requestAnimationFrame(apply);
 }
 function prepare(){
  slides.forEach((s,i)=>{s.classList.remove('is-active','is-next','is-prev');s.style.transition='none';s.style.transform='translateX(0)';
   if(i===index)s.classList.add('is-active');
   else if(i===index+1){s.classList.add('is-next');s.style.transform='translateX(-100%)';}
   else if(i===index-1){s.classList.add('is-prev');s.style.transform='translateX(100%)';}
  });
  if(landscape)viewer.style.height='calc(100dvh - 42px)';
  else{viewer.style.height='auto';fitPortraitHeight();}
  updateCounter();
 }
 function animateTo(newIndex,dir){
  if(animating||newIndex<0||newIndex>=slides.length)return;
  animating=true;const cur=slides[index],other=slides[newIndex];
  cur.style.transition='transform .20s ease';other.style.transition='transform .20s ease';
  if(dir==='next'){cur.style.transform='translateX(100%)';other.style.transform='translateX(0)';}
  else{cur.style.transform='translateX(-100%)';other.style.transform='translateX(0)';}
  setTimeout(()=>{index=newIndex;animating=false;prepare();},210);
 }
 function snap(){
  const cur=slides[index],n=slides[index+1],p=slides[index-1];
  [cur,n,p].forEach(x=>{if(x)x.style.transition='transform .15s ease';});
  if(cur)cur.style.transform='translateX(0)';
  if(n)n.style.transform='translateX(-100%)';
  if(p)p.style.transform='translateX(100%)';
  setTimeout(prepare,160);
 }
 viewer.addEventListener('touchstart',e=>{
  if(animating||e.touches.length!==1)return;
  const t=e.touches[0];startX=t.clientX;startY=t.clientY;dx=0;dragging=true;axis=null;
  [slides[index],slides[index+1],slides[index-1]].forEach(x=>{if(x)x.style.transition='none';});
 },{passive:true});
 viewer.addEventListener('touchmove',e=>{
  if(!dragging||e.touches.length!==1)return;
  const t=e.touches[0];let mx=t.clientX-startX,my=t.clientY-startY;
  if(axis===null){if(Math.abs(mx)<8&&Math.abs(my)<8)return;axis=Math.abs(mx)>Math.abs(my)?'x':'y';}
  if(axis!=='x')return;
  e.preventDefault();dx=mx;
  const cur=slides[index],n=slides[index+1],p=slides[index-1],w=viewer.clientWidth||1;
  if(dx>0){if(index>=slides.length-1)dx*=0.25;cur.style.transform=`translateX(${dx}px)`;if(n)n.style.transform=`translateX(${-w+dx}px)`;}
  else{if(index<=0)dx*=0.25;cur.style.transform=`translateX(${dx}px)`;if(p)p.style.transform=`translateX(${w+dx}px)`;}
 },{passive:false});
 viewer.addEventListener('touchend',()=>{
  if(!dragging)return;dragging=false;
  if(axis!=='x'){prepare();return;}
  const threshold=Math.min(90,(viewer.clientWidth||1)*0.16);
  if(dx>threshold&&index<slides.length-1)animateTo(index+1,'next');
  else if(dx<-threshold&&index>0)animateTo(index-1,'prev');
  else snap();
 },{passive:true});
 let wheelLock=false;
 viewer.addEventListener('wheel',e=>{
  if(wheelLock)return;
  const amount=Math.abs(e.deltaX)>Math.abs(e.deltaY)?e.deltaX:e.deltaY;
  if(Math.abs(amount)<20)return;
  e.preventDefault();wheelLock=true;
  if(amount<0&&index<slides.length-1)animateTo(index+1,'next');
  else if(amount>0&&index>0)animateTo(index-1,'prev');
  setTimeout(()=>wheelLock=false,280);
 },{passive:false});
 if(prevBtn)prevBtn.onclick=()=>animateTo(index+1,'next');
 if(nextBtn)nextBtn.onclick=()=>animateTo(index-1,'prev');
 if(topBtn)topBtn.onclick=()=>{currentPage=0;index=0;prepare();window.scrollTo({top:0,behavior:'smooth'});};
 const restartBtn=endSlide.querySelector('#restart');
 if(restartBtn)restartBtn.onclick=()=>{if(topBtn)topBtn.click();};
 document.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')animateTo(index+1,'next');if(e.key==='ArrowRight')animateTo(index-1,'prev');});
 let timer;
 function onRotate(){clearTimeout(timer);timer=setTimeout(()=>{const newLandscape=isLandscape();if(newLandscape!==landscape)build();else prepare();},220);}
 window.addEventListener('resize',onRotate);
 window.addEventListener('orientationchange',()=>{setTimeout(onRotate,300);setTimeout(onRotate,650);});
 build();
})();
