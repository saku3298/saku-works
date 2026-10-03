(()=> {
const viewer=document.getElementById('viewer');
let originals=[...viewer.querySelectorAll('.manga-page')];
const counter=document.getElementById('counter'),topBtn=document.getElementById('top');
const prevBtn=document.getElementById('prev'),nextBtn=document.getElementById('next');
let slides=[],index=0,currentPage=0,landscape=false,startX=0,startY=0,dx=0,dy=0,dragging=false,axis=null;

const isLandscape=()=>window.innerWidth>window.innerHeight;
const blank=()=>{const d=document.createElement('div');d.className='manga-page blank-page';d.setAttribute('aria-hidden','true');return d};
function addSpread(rightPage,leftPage,start,end){
 const s=document.createElement('div');s.className='reader-slide spread';s.dataset.start=start;s.dataset.end=end;
 // Existing Ogre Kingdom convention: first element = right, second = left, with row-reverse.
 s.append(rightPage,leftPage);viewer.appendChild(s);slides.push(s);
}
function build(){
 currentPage=slides[index]?Number(slides[index].dataset.start||0):currentPage;
 viewer.innerHTML='';slides=[];landscape=isLandscape();
 if(landscape){
   // Same as current Ogre Kingdom: page 1 is LEFT, blank is RIGHT.
   addSpread(blank(),originals[0],0,0);
   let i=1;
   // Body: even-numbered page RIGHT, following odd-numbered page LEFT.
   for(;i+1<originals.length;i+=2) addSpread(originals[i],originals[i+1],i,i+1);
   // If one remains: final page RIGHT, blank LEFT.
   if(i<originals.length) addSpread(originals[i],blank(),i,i);
 }else{
   originals.forEach((p,i)=>{const s=document.createElement('div');s.className='reader-slide single';s.dataset.start=i;s.dataset.end=i;s.appendChild(p);viewer.appendChild(s);slides.push(s)});
 }
 index=Math.max(0,slides.findIndex(s=>currentPage>=+s.dataset.start&&currentPage<=+s.dataset.end));prepare();fit();
}
function prepare(){
 slides.forEach((s,i)=>s.classList.toggle('is-active',i===index));
 const s=slides[index],a=+s.dataset.start,b=+s.dataset.end;currentPage=a;
 counter.textContent=(landscape&&b>a?`${a+1}-${b+1}`:`${a+1}`)+` / ${originals.length}`;
}
function fit(){if(landscape)return;const s=slides[index],img=s?.querySelector('img');if(!img)return;const apply=()=>viewer.style.height=s.offsetHeight+'px';img.complete?requestAnimationFrame(apply):img.addEventListener('load',()=>requestAnimationFrame(apply),{once:true})}
function go(delta){const n=Math.max(0,Math.min(slides.length-1,index+delta));if(n===index)return;index=n;prepare();fit()}
prevBtn.onclick=()=>go(1);nextBtn.onclick=()=>go(-1);topBtn.onclick=()=>{index=0;prepare();fit()};
viewer.addEventListener('touchstart',e=>{if(e.touches.length!==1){dragging=false;return}startX=e.touches[0].clientX;startY=e.touches[0].clientY;dx=dy=0;axis=null;dragging=true},{passive:true});
viewer.addEventListener('touchmove',e=>{if(!dragging||e.touches.length!==1)return;dx=e.touches[0].clientX-startX;dy=e.touches[0].clientY-startY;if(!axis&&Math.max(Math.abs(dx),Math.abs(dy))>8)axis=Math.abs(dx)>Math.abs(dy)?'x':'y'},{passive:true});
viewer.addEventListener('touchend',()=>{if(dragging&&axis==='x'&&Math.abs(dx)>45){dx<0?go(1):go(-1)}dragging=false},{passive:true});
window.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')go(1);if(e.key==='ArrowRight')go(-1)});
let timer;window.addEventListener('resize',()=>{clearTimeout(timer);timer=setTimeout(build,160)});
build();
})();