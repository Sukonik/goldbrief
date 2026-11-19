/* GoldBrief Markets: delayed LED price panels. Prices come from Payout Lab's published data.json (unofficial Yahoo Finance / Tiingo data).
   Nothing here is a live feed: each price shows when it was last updated, and dims as it ages. The page works without JS (server-rendered snapshot). */
(()=>{"use strict";
const URL_="https://sukonik.github.io/payout-lab/data.json",TTL=30000,fmtET=(d,o)=>new Intl.DateTimeFormat("en-US",{timeZone:"America/New_York",...o}).format(d)+" ET";
const stamp=d=>fmtET(d,{month:"short",day:"numeric",hour:"numeric",minute:"2-digit"}),money=n=>"$"+Number(n).toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});
const leds=[...document.querySelectorAll(".led[data-ticker]")],status=document.getElementById("quote-status"),fetchBtn=document.getElementById("fetch-quotes");
let cache=null,busy=false;
function age(ms){const m=Math.floor(ms/60000);if(m<1)return"just now";if(m<60)return m+" min ago";const h=Math.floor(m/60);if(h<24)return h+" h ago";const d=Math.floor(h/24);return d+(d===1?" day":" days")+" ago"}
function paint(el){const u=el.dataset.updated?new Date(el.dataset.updated):null,ageEl=el.querySelector(".led__age"),has=u&&!isNaN(u)&&el.dataset.price!=="";
 el.classList.remove("led--aging","led--stale");
 if(!has){ageEl.textContent="";return}
 const ms=Date.now()-u.getTime();ageEl.textContent="· "+age(ms);
 if(ms>=7*864e5){el.classList.add("led--stale");ageEl.textContent+=" · STALE"}else if(ms>=864e5){el.classList.add("led--aging")}
 el.querySelector(".led__asof").textContent="Updated "+stamp(u)}
function show(el,rec){const v=money(rec.p);el.dataset.price=rec.p;el.dataset.updated=rec.u;el.dataset.source=rec.src||"unknown";
 el.querySelector(".led__value").textContent=v;el.querySelector(".led__ghost").textContent=v.replace(/\d/g,"8");
 el.querySelector(".led__src").textContent=(rec.src||"unknown")+" via Payout Lab · delayed, not live";
 if(!matchMedia("(prefers-reduced-motion: reduce)").matches){el.classList.remove("led--tick");void el.offsetWidth;el.classList.add("led--tick")}
 paint(el)}
async function load(){if(cache&&Date.now()-cache.t<TTL)return cache.d;const r=await fetch(URL_,{cache:"no-cache"});if(!r.ok)throw Error("HTTP "+r.status);const d=await r.json();if(!d||!d.tickers)throw Error("unexpected file");cache={t:Date.now(),d};return d}
function busyState(on,btns){busy=on;[fetchBtn,...leds.map(l=>l.querySelector(".led__refresh"))].filter(Boolean).forEach(b=>{b.disabled=on;b.classList.toggle("is-loading",on&&btns.includes(b))});if(status)status.setAttribute("aria-busy",String(on))}
async function refresh(targets,btn){if(busy)return;busyState(true,[btn]);if(status)status.textContent="Fetching the latest Payout Lab file…";
 try{const d=await load();let changed=0,unchanged=0,missing=0;
  targets.forEach(el=>{const rec=d.tickers[el.dataset.ticker];if(rec&&typeof rec.p==="number"&&rec.p>0&&rec.u){if(String(rec.p)!==el.dataset.price||rec.u!==el.dataset.updated)changed++;else unchanged++;show(el,rec)}else missing++});
  const lab=d.updated?stamp(new Date(d.updated)):"unknown";
  if(status)status.textContent="Fetched "+stamp(new Date())+". Payout Lab file updated "+lab+". "+changed+" price"+(changed===1?"":"s")+" updated, "+unchanged+" unchanged"+(missing?", "+missing+" not in the file":"")+". Each ticker keeps its own update time."}
 catch(err){if(status)status.textContent="Could not reach Payout Lab ("+err.message+"). Showing the saved snapshot."}
 finally{busyState(false,[])}}
leds.forEach(el=>{paint(el);el.querySelector(".led__refresh")?.addEventListener("click",e=>refresh([el],e.currentTarget))});
fetchBtn?.addEventListener("click",()=>refresh(leds,fetchBtn));
setInterval(()=>leds.forEach(paint),60000);
})();
