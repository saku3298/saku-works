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
function fit(){
  if(landscape)return;
  const s=slides[index]; if(!s)return;
  const img=s.querySelector('img'); if(!img)return;
  const apply=()=>{
    const w=viewer.clientWidth || window.innerWidth;
    if(img.naturalWidth && img.naturalHeight){
      viewer.style.height=Math.round(w*img.naturalHeight/img.naturalWidth)+'px';
    }
  };
  if(img.complete) requestAnimationFrame(apply);
  else img.addEventListener('load',()=>requestAnimationFrame(apply),{once:true});
})();