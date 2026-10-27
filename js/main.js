/* GoldBrief V1 • light, accessible enhancement; content is readable without JS. */
(()=>{"use strict";
const drawer=document.getElementById("nav-drawer"),toggle=document.querySelector(".nav-toggle"),close=document.querySelector(".nav-drawer__close");
let lastFocus=null;
function setOpen(open){if(!drawer||!toggle)return;drawer.hidden=!open;drawer.dataset.open=String(open);document.body.dataset.drawerOpen=String(open);toggle.setAttribute("aria-expanded",String(open));if(open){lastFocus=document.activeElement;close?.focus()}else if(drawer.contains(document.activeElement))toggle.focus()}
toggle?.addEventListener("click",()=>setOpen(drawer.hidden));close?.addEventListener("click",()=>setOpen(false));
drawer?.addEventListener("click",e=>{if(e.target.closest("a"))setOpen(false)});
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!drawer?.hidden){e.preventDefault();setOpen(false)}if(e.key==="Tab"&&!drawer?.hidden){const focusable=[...drawer.querySelectorAll("a,button")].filter(x=>!x.disabled);const first=focusable[0],last=focusable.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}});
document.addEventListener("pointerdown",e=>{if(drawer&&!drawer.hidden&&!drawer.contains(e.target)&&!toggle.contains(e.target))setOpen(false)});
const mq=matchMedia("(min-width: 1200px)");mq.addEventListener?.("change",()=>{if(mq.matches&&!drawer?.hidden)setOpen(false)});
function wireFilter(field,selector,fn){const input=document.getElementById(field),nodes=[...document.querySelectorAll(selector)],counter=document.getElementById("result-count");if(!input||!nodes.length)return;const run=()=>{const q=input.value.trim().toLowerCase();let visible=0;nodes.forEach(node=>{let match=(node.dataset.search||"").includes(q);if(fn)match=match&&fn(node);node.hidden=!match;if(match)visible++});if(counter)counter.textContent=visible+" results";};input.addEventListener("input",run);document.getElementById("app-category")?.addEventListener("change",run);run()}
wireFilter("company-search","#company-grid .company-card");
wireFilter("glossary-search","#glossary-grid .card");
wireFilter("app-search","#app-grid .company-card",node=>{const selected=document.getElementById("app-category")?.value||"all";return selected==="all"||node.dataset.category===selected});
const feed=document.getElementById("daily-feed");
if(feed){fetch("data/daily.json",{cache:"no-cache"}).then(r=>{if(!r.ok)throw Error("feed unavailable");return r.json()}).then(d=>{
 const s=Array.isArray(d.stories)?d.stories.slice(0,20):[];
 if(!s.length){feed.textContent="Daily external edition not yet available. The curated news above remains accessible.";return}
 feed.replaceChildren();
 const meta=document.createElement("p");meta.className="last-review";meta.textContent="External RSS headlines • automatically collected "+(d.generated_at||"date unavailable")+" • Not independently verified";feed.append(meta);
 s.forEach(item=>{try{const u=new URL(item.url);if(!["http:","https:"].includes(u.protocol))return;const article=document.createElement("article");article.className="article-row";const date=document.createElement("time");date.className="article-row__date";date.textContent=item.date||"Source feed";const wrap=document.createElement("div"),h=document.createElement("h3");h.className="article-row__title";const a=document.createElement("a");a.className="text-link";a.href=u.href;a.rel="noopener noreferrer";a.target="_blank";a.textContent=item.title+" ↗";h.append(a);const p=document.createElement("p");p.className="article-row__source";p.textContent=(item.source||"External source")+" • Automated headline, not GoldBrief reporting";wrap.append(h,p);article.append(date,wrap);feed.append(article)}catch(_){}});
 }).catch(()=>{feed.textContent="Daily headlines could not be loaded. Read the sourced editorial archive above."})}
})();