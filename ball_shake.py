#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer

HTML = r"""<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Ball Shake Random App</title>
  <style>
    :root{
      --bg1:#fff2f8; --bg2:#f2fbff; --card:#ffffffcc;
      --text:#2b2b2b; --muted:#6b6b6b;
      --shadow: 0 10px 30px rgba(0,0,0,.08);
      --radius: 18px;
    }
    *{box-sizing:border-box;font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Arial;}
    body{
      margin:0; color:var(--text);
      background: radial-gradient(circle at 20% 10%, var(--bg2), transparent 40%),
                  radial-gradient(circle at 80% 0%, var(--bg1), transparent 45%),
                  linear-gradient(180deg, #ffffff, #f7f7ff);
      min-height:100vh; display:flex; align-items:center; justify-content:center;
      padding:24px;
    }
    .app{
      width:min(1280px, 100%);
      background:var(--card);
      backdrop-filter: blur(8px);
      border:1px solid rgba(255,255,255,.6);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
    }
    header{
      padding:18px 20px;
      background: linear-gradient(90deg, #ffe6f2, #e7fbff);
      display:flex; align-items:center; justify-content:space-between; gap:12px;
    }
    header h1{ font-size:18px; margin:0; display:flex; align-items:center; gap:10px; }
    .badge{
      font-size:12px; padding:5px 10px; border-radius:999px; background:#fff;
      border:1px solid rgba(0,0,0,.06); color:var(--muted);
    }

    main{ padding:18px 20px 22px; display:grid; gap:20px; grid-template-columns: 1fr 1fr;}
    @media (max-width: 960px){ main{grid-template-columns:1fr;} }

    .card{
      background:#fff; border:1px solid rgba(0,0,0,.06);
      border-radius: var(--radius); box-shadow: 0 8px 20px rgba(0,0,0,.06);
      padding:16px;
    }
    .row{display:flex; gap:10px; flex-wrap:wrap; align-items:center;}
    input[type="text"]{
      flex:1; padding:12px 12px; border-radius:14px;
      border:1px solid rgba(0,0,0,.12); outline:none; font-size:14px;
    }
    input[type="text"]:focus{border-color: rgba(255,105,180,.55); box-shadow: 0 0 0 4px rgba(255,105,180,.12);}

    button{
      border:none; cursor:pointer; padding:11px 14px;
      border-radius: 14px; font-weight:900;
      transition:.15s transform, .15s opacity; user-select:none;
    }
    button:active{transform: scale(.98);}
    .btn-add{background: linear-gradient(90deg,#7cf0c9,#67b7ff); color:#063b2b;}
    .btn-shake{background: linear-gradient(90deg,#ff7ab6,#ffd56a); color:#4a2a00; min-width:190px;}
    .btn-shuffle{background: linear-gradient(90deg,#b88cff,#67b7ff); color:#180b3a; min-width:190px;}
    .btn-clear{background:#f3f3f3; color:#333;}
    .btn-mini{ padding:7px 10px; font-weight:900; border-radius: 12px; background:#f4f6ff; color:#2d3a8c; }
    .btn-mini.danger{background:#fff0f0; color:#a01818;}
    .muted{color:var(--muted); font-size:13px; margin:6px 0 0;}
    .hint{font-size:12px; color:var(--muted); margin-top:10px; line-height:1.5;}
    .counter{font-weight:900;}

    /* Left balls */
    .balls{
      display:flex; flex-wrap:wrap; gap:10px;
      margin-top:12px; min-height:62px; align-items:center;
    }
    .ball{
      width:54px; height:54px; border-radius: 50%;
      display:flex; align-items:center; justify-content:center;
      color:#fff; font-weight:900;
      box-shadow: inset 0 -8px 18px rgba(0,0,0,.18), 0 10px 18px rgba(0,0,0,.10);
      position:relative;
    }
    .ball span{
      display:block; max-width:46px; font-size:12px; line-height:1.05;
      text-align:center; padding:0 6px; text-shadow: 0 2px 6px rgba(0,0,0,.25);
      overflow:hidden; white-space:nowrap; text-overflow:ellipsis;
    }
    .ball.selected{
      outline: 4px solid rgba(255,255,255,.95);
      box-shadow: 0 0 0 6px rgba(255,105,180,.25), inset 0 -8px 18px rgba(0,0,0,.18), 0 16px 30px rgba(0,0,0,.18);
      animation: pop .35s ease both;
    }
    @keyframes pop{ from{transform:scale(.9)} to{transform:scale(1)} }

    .list{ margin-top:10px; display:grid; gap:8px; }
    .item-row{
      display:flex; align-items:center; justify-content:space-between; gap:10px;
      padding:10px 12px; border-radius: 14px;
      border:1px solid rgba(0,0,0,.06); background:#fff;
    }
    .item-row .name{font-weight:900; cursor:pointer;}

    /* Right jar */
    .shake-area{ display:flex; align-items:center; justify-content:center; padding:20px 12px 10px; }
    
    .jar{
      width:460px; height:460px; 
      border-radius: 65px;
      background: linear-gradient(180deg, #ffffff, #f7f7ff);
      border:1px solid rgba(0,0,0,.06);
      box-shadow: 0 20px 50px rgba(0,0,0,.12);
      position:relative; overflow:hidden;
    }
    @media (max-width: 520px){
      .jar{ width:320px; height:320px; border-radius: 48px; }
    }

    .jar::before{
      content:""; position:absolute; inset:-80px -80px auto auto;
      width:220px; height:220px;
      background: radial-gradient(circle, rgba(255,122,182,.35), transparent 60%);
      transform: rotate(25deg);
      pointer-events:none;
    }
    .jar-inner{
      position:absolute; inset:20px;
      border-radius: 50px;
      background: radial-gradient(circle at 50% 0%, rgba(103,183,255,.18), transparent 45%),
                  radial-gradient(circle at 0% 100%, rgba(255,122,182,.14), transparent 50%);
      border:1px dashed rgba(0,0,0,.10);
    }

    .jar.shaking{ animation: jarShake .75s ease-in-out; }
    @keyframes jarShake{
      0%,100%{transform:translateX(0) rotate(0deg)}
      15%{transform:translateX(-14px) rotate(-4deg)}
      30%{transform:translateX(14px) rotate(4deg)}
      45%{transform:translateX(-10px) rotate(-3deg)}
      60%{transform:translateX(10px) rotate(3deg)}
      75%{transform:translateX(-6px) rotate(-2deg)}
    }

    /* Small balls inside jar - แก้ไขขนาดให้ใหญ่สะใจที่นี่ */
    .jar-balls{ position:absolute; inset:20px; border-radius:50px; }
    .jball{
      position:absolute;
      /* ปรับขนาดเป็น 75px (EXTRA LARGE) */
      width:75px; height:75px; border-radius:50%;
      display:flex; align-items:center; justify-content:center;
      color:#fff; font-weight:900; 
      font-size:15px; /* เพิ่มขนาดตัวอักษรให้อ่านง่าย */
      text-shadow: 0 2px 6px rgba(0,0,0,.22);
      box-shadow: inset 0 -10px 18px rgba(0,0,0,.18), 0 12px 18px rgba(0,0,0,.10);
      will-change: left, top, transform;
      transition: left .08s linear, top .08s linear;
    }
    .jball small{
      max-width:65px; padding:0 5px;
      overflow:hidden; white-space:nowrap; text-overflow:ellipsis;
    }

    /* Picked ball pops up */
    .picked-float{
      position:absolute; left:50%; top:88%;
      transform:translate(-50%,-50%) scale(.95);
      width:140px; height:140px;
      border-radius:50%;
      display:flex; align-items:center; justify-content:center;
      opacity:0; pointer-events:none;
      color:#fff; font-weight:900; font-size:18px;
      text-shadow: 0 2px 10px rgba(0,0,0,.30);
      box-shadow: inset 0 -14px 28px rgba(0,0,0,.18), 0 22px 34px rgba(0,0,0,.16);
    }
    .picked-float span{
      display:block; max-width:120px;
      overflow:hidden; white-space:nowrap; text-overflow:ellipsis;
      padding:0 10px;
    }
    .picked-float.show{
      animation: floatUp 1.0s ease both;
      opacity:1;
    }
    @keyframes floatUp{
      0%{ transform:translate(-50%,-8%) scale(.88); opacity:0; }
      25%{ opacity:1; }
      60%{ transform:translate(-50%,-80%) scale(1.1); }
      100%{ transform:translate(-50%,-70%) scale(1); opacity:1; }
    }

    .result{
      margin-top:10px; padding:12px 14px;
      border-radius: 14px; background: #f7fbff;
      border:1px solid rgba(103,183,255,.35);
    }
    .result strong{font-size:14px;}

    /* History */
    .history{
      margin-top:10px;
      border-radius:14px;
      border:1px solid rgba(0,0,0,.06);
      overflow:hidden;
    }
    .history-head{
      padding:10px 12px;
      background: linear-gradient(90deg, #e7fbff, #ffe6f2);
      display:flex; align-items:center; justify-content:space-between;
      gap:10px;
    }
    .history-list{
      max-height:220px; overflow:auto;
      background:#fff;
    }
    .hrow{
      padding:10px 12px;
      border-top:1px solid rgba(0,0,0,.06);
      display:flex; align-items:flex-start; justify-content:space-between; gap:10px;
      font-size:13px;
    }
    .hrow b{font-weight:900;}

    /* Sound toggle */
    .sound-toggle{
      display:flex; align-items:center; gap:8px;
      padding:9px 12px;
      border-radius:14px;
      background:#fff;
      border:1px solid rgba(0,0,0,.08);
      font-size:13px;
      font-weight:900;
    }
    .sound-toggle input{ transform: scale(1.15); }
  </style>
</head>
<body>
  <div class="app">
    <header>
      <h1>🫧 Ball Shake Random App <span class="badge">XL BALLS • Sound • Shuffle</span></h1>
      <div class="badge">เหลือ <span class="counter" id="count">0</span> รายการ</div>
    </header>

    <main>
      <section class="card">
        <div class="row">
          <input id="itemInput" type="text" placeholder="พิมพ์รายการ… เช่น 'จอห์น' แล้วกด เพิ่ม" />
          <button class="btn-add" id="addBtn">➕ เพิ่ม</button>
          <button class="btn-clear" id="resetBtn" title="ล้างรายการทั้งหมด">🧹 ล้างทั้งหมด</button>
        </div>

        <div class="row" style="justify-content:space-between; margin-top:10px;">
          <div class="muted">ลูกบอล 1 ลูก = 1 รายการ • ดับเบิลคลิกชื่อเพื่อแก้ไข</div>
          <label class="sound-toggle" title="เปิด/ปิดเสียงเอฟเฟกต์">
            🔊 Sound
            <input type="checkbox" id="soundOn" checked>
          </label>
        </div>

        <div class="balls" id="balls"></div>
        <div class="list" id="list"></div>

        <div class="hint">
          ✅ สุ่มยุติธรรม: ทุก item โอกาสเท่ากัน (uniform) <br/>
          ✅ หลังสุ่ม: ลบ item ที่ถูกสุ่มออก พร้อมสุ่มครั้งถัดไป
        </div>
      </section>

      <aside class="card">
        <div class="shake-area">
          <div class="jar" id="jar">
            <div class="jar-inner"></div>
            <div class="jar-balls" id="jarBalls"></div>
            <div class="picked-float" id="pickedFloat"><span id="pickedFloatText"></span></div>
          </div>
        </div>

        <div class="row" style="justify-content:center; margin-top:10px;">
          <button class="btn-shake" id="shakeBtn">🫨 Shake!</button>
          <button class="btn-shuffle" id="shuffleBtn">🔀 Shuffle</button>
        </div>

        <div class="result" id="resultBox" aria-live="polite">
          <strong>ผลลัพธ์:</strong>
          <div id="resultText" class="muted" style="margin-top:6px;">ยังไม่ได้สุ่ม</div>
        </div>

        <div class="history">
          <div class="history-head">
            <div style="font-weight:900;">📜 ประวัติการสุ่ม</div>
            <button class="btn-mini danger" id="clearHistoryBtn">ล้างประวัติ</button>
          </div>
          <div class="history-list" id="historyList"></div>
        </div>

        <div class="hint">
          ประวัติ + รายการ จะเก็บไว้ในเครื่อง (localStorage) • ปิดเว็บแล้วเปิดใหม่ยังอยู่
        </div>
      </aside>
    </main>
  </div>

<script>
  // ===== Storage keys =====
  const KEY_ITEMS = "ball_shake_items_v3";
  const KEY_HIST  = "ball_shake_history_v2";
  const KEY_SOUND = "ball_shake_sound_v1";

  let items = [];
  let history = []; // {n, name, t}

  const palette = ["#ff7ab6","#67b7ff","#7cf0c9","#ffd56a","#b88cff","#ff8a65","#4dd0e1","#81c784","#f06292","#9575cd"];
  const $ = (id)=>document.getElementById(id);

  function uid(){ return Math.random().toString(16).slice(2) + Date.now().toString(16); }
  function pickColor(i){ return palette[i % palette.length]; }
  function nowText(){
    const d = new Date();
    return d.toLocaleString("th-TH", { hour12:false });
  }

  // ===== Cute sound effects (Web Audio) =====
  let audioCtx = null;

  function soundEnabled(){
    return $("soundOn")?.checked === true;
  }

  function ensureAudio(){
    if(!audioCtx){
      const AC = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AC();
    }
    if(audioCtx.state === "suspended"){
      audioCtx.resume();
    }
  }

  function playTone({freq=660, dur=0.08, type="sine", gain=0.04, ramp=0.02}){
    if(!soundEnabled()) return;
    ensureAudio();

    const t0 = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const g = audioCtx.createGain();

    osc.type = type;
    osc.frequency.setValueAtTime(freq, t0);

    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(gain, t0 + ramp);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);

    osc.connect(g).connect(audioCtx.destination);
    osc.start(t0);
    osc.stop(t0 + dur + 0.02);
  }

  function sfxShake(){
    const base = 520 + Math.random()*60;
    playTone({freq: base, dur: 0.06, type:"triangle", gain:0.03});
    setTimeout(()=>playTone({freq: base+160, dur:0.06, type:"triangle", gain:0.03}), 70);
    setTimeout(()=>playTone({freq: base+80, dur:0.06, type:"triangle", gain:0.03}), 140);
  }

  function sfxShuffle(){
    playTone({freq: 420, dur: 0.05, type:"square", gain:0.02});
    setTimeout(()=>playTone({freq: 620, dur:0.07, type:"sine", gain:0.03}), 60);
  }

  function sfxPop(){
    playTone({freq: 740, dur: 0.07, type:"sine", gain:0.05});
    setTimeout(()=>playTone({freq: 1040, dur:0.09, type:"sine", gain:0.05}), 80);
  }

  // ===== Persistence =====
  function save(){
    localStorage.setItem(KEY_ITEMS, JSON.stringify(items));
    localStorage.setItem(KEY_HIST, JSON.stringify(history));
    localStorage.setItem(KEY_SOUND, soundEnabled() ? "1" : "0");
  }
  function load(){
    try{
      items = JSON.parse(localStorage.getItem(KEY_ITEMS) || "[]");
      if(!Array.isArray(items)) items = [];
    }catch(e){ items = []; }

    try{
      history = JSON.parse(localStorage.getItem(KEY_HIST) || "[]");
      if(!Array.isArray(history)) history = [];
    }catch(e){ history = []; }

    const s = localStorage.getItem(KEY_SOUND);
    if(s === "0") $("soundOn").checked = false;
  }

  function ballBg(color){
    return `radial-gradient(circle at 30% 25%, rgba(255,255,255,.85), rgba(255,255,255,0) 32%), ${color}`;
  }

  // ===== Render helpers =====
  function escapeHtml(s){
    return String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");
  }

  function renderJarBalls(){
    const box = $("jarBalls");
    box.innerHTML = "";
    const W = box.clientWidth || 328;
    const H = box.clientHeight || 328;

    // จำกัดการแสดงผลไม่ให้แน่นเกินเพราะบอลใหญ่มาก
    const showN = Math.min(items.length, 20); 
    for(let i=0;i<showN;i++){
      const it = items[i];
      const d = document.createElement("div");
      d.className = "jball";
      d.style.background = ballBg(it.color);
      // ** แก้ไขตำแหน่งสุ่มสำหรับบอล 75px **
      const left = Math.floor(Math.random()*(W-75));
      const top  = Math.floor(Math.random()*(H-75));
      d.style.left = left + "px";
      d.style.top  = top  + "px";
      d.innerHTML = `<small>${escapeHtml(it.name)}</small>`;
      box.appendChild(d);
    }
  }

  function renderHistory(){
    const list = $("historyList");
    list.innerHTML = "";
    if(history.length === 0){
      list.innerHTML = `<div class="hrow"><span class="muted">ยังไม่มีประวัติการสุ่ม</span></div>`;
      return;
    }
    [...history].slice().reverse().forEach(h=>{
      const row = document.createElement("div");
      row.className = "hrow";
      row.innerHTML = `<div><b>ครั้งที่ ${h.n}</b> • ${escapeHtml(h.name)}</div><div class="muted">${escapeHtml(h.t)}</div>`;
      list.appendChild(row);
    });
  }

  function render(){
    $("count").textContent = String(items.length);

    const balls = $("balls");
    balls.innerHTML = "";
    items.forEach((it)=>{
      const d = document.createElement("div");
      d.className = "ball";
      d.style.background = ballBg(it.color);
      d.title = it.name;
      const s = document.createElement("span");
      s.textContent = it.name;
      d.appendChild(s);
      balls.appendChild(d);
    });

    const list = $("list");
    list.innerHTML = "";
    items.forEach((it)=>{
      const row = document.createElement("div");
      row.className = "item-row";

      const name = document.createElement("div");
      name.className = "name";
      name.textContent = it.name;
      name.title = "ดับเบิลคลิกเพื่อแก้ไข";
      name.ondblclick = ()=> startEdit(it.id);

      const actions = document.createElement("div");
      actions.className = "row";
      actions.style.gap = "8px";

      const editBtn = document.createElement("button");
      editBtn.className = "btn-mini";
      editBtn.textContent = "✏️ แก้ไข";
      editBtn.onclick = ()=> startEdit(it.id);

      const delBtn = document.createElement("button");
      delBtn.className = "btn-mini danger";
      delBtn.textContent = "🗑️ ลบ";
      delBtn.onclick = ()=> removeItem(it.id);

      actions.appendChild(editBtn);
      actions.appendChild(delBtn);

      row.appendChild(name);
      row.appendChild(actions);
      list.appendChild(row);
    });

    if(items.length === 0){
      balls.innerHTML = `<div class="muted">ยังไม่มีรายการ — เพิ่มรายการด้านบนได้เลย ✨</div>`;
      list.innerHTML = "";
    }

    renderHistory();
    setTimeout(renderJarBalls, 0);
  }

  // ===== CRUD =====
  function addItem(name){
    const trimmed = (name ?? "").trim();
    if(!trimmed){ alert("กรุณาพิมพ์ชื่อรายการก่อน"); return; }
    items.push({ id: uid(), name: trimmed, color: pickColor(items.length) });
    save(); render();
  }

  function removeItem(id){
    items = items.filter(x => x.id !== id);
    save(); render();
  }

  function startEdit(id){
    const it = items.find(x => x.id === id);
    if(!it) return;
    const next = prompt("แก้ไขชื่อรายการ:", it.name);
    if(next === null) return;
    const trimmed = next.trim();
    if(!trimmed){ alert("ชื่อรายการต้องไม่ว่าง"); return; }
    it.name = trimmed;
    save(); render();
  }

  function resetAll(){
    if(!confirm("ล้างรายการทั้งหมดจริงไหม?")) return;
    items = [];
    save(); render();
    setResult("ล้างรายการแล้ว ✅");
  }

  function clearHistory(){
    if(!confirm("ล้างประวัติการสุ่มทั้งหมดจริงไหม?")) return;
    history = [];
    save(); renderHistory();
  }

  function setResult(text){
    $("resultText").textContent = text;
  }

  // ===== Shuffle (new) =====
  function shuffleItems(){
    if(items.length <= 1){
      setResult("มีรายการไม่พอให้ Shuffle");
      return;
    }
    for(let i=items.length-1;i>0;i--){
      const j = Math.floor(Math.random()*(i+1));
      [items[i], items[j]] = [items[j], items[i]];
    }
    items = items.map((it, idx)=>({...it, color: pickColor(idx)}));
    save();
    render();
    sfxShuffle();
    setResult("Shuffle แล้ว! 🔀");
  }

  // ===== Shake animation =====
  function sleep(ms){ return new Promise(r=>setTimeout(r, ms)); }

  async function jitterJarBalls(msTotal){
    const box = $("jarBalls");
    const W = box.clientWidth || 328;
    const H = box.clientHeight || 328;
    const balls = Array.from(box.querySelectorAll(".jball"));
    const start = Date.now();
    while(Date.now() - start < msTotal){
      balls.forEach(b=>{
        // ** แก้ไขตำแหน่งสุ่มสำหรับบอล 75px **
        const left = Math.floor(Math.random()*(W-75));
        const top  = Math.floor(Math.random()*(H-75));
        b.style.left = left + "px";
        b.style.top  = top  + "px";
      });
      await sleep(80);
    }
  }

  async function popPickedBall(picked){
    const pf = $("pickedFloat");
    const txt = $("pickedFloatText");
    txt.textContent = picked.name;
    pf.style.background = ballBg(picked.color);
    pf.classList.remove("show");
    void pf.offsetWidth;
    pf.classList.add("show");
    sfxPop();
    await sleep(1000);
  }

  async function shake(){
    if(items.length === 0){ alert("ยังไม่มีรายการให้สุ่ม — เพิ่มรายการก่อนนะ"); return; }

    const jar = $("jar");
    jar.classList.add("shaking");
    setResult("กำลังเขย่า… 🫨");
    sfxShake();

    const jitterPromise = jitterJarBalls(750);
    await sleep(750);
    jar.classList.remove("shaking");
    await jitterPromise;

    const idx = Math.floor(Math.random() * items.length);
    const picked = items[idx];

    const ballEls = Array.from(document.querySelectorAll("#balls .ball"));
    ballEls.forEach(b => b.classList.remove("selected"));
    if(ballEls[idx]) ballEls[idx].classList.add("selected");

    await popPickedBall(picked);

    const n = history.length + 1;
    history.push({ n, name: picked.name, t: nowText() });

    setResult(`ครั้งที่ ${n}: ได้ "${picked.name}" 🎉`);

    items.splice(idx, 1);
    save();
    render();

    if(items.length === 0){
      await sleep(150);
      setResult("สุ่มครบแล้ว 🎊 (รายการหมด)");
    }
  }

  // ===== Init =====
  function init(){
    load();
    items = items.map((it, i)=>({
      id: it.id ?? uid(),
      name: it.name ?? "Unnamed",
      color: it.color ?? pickColor(i)
    }));
    save();
    render();

    $("addBtn").onclick = ()=>{
      addItem($("itemInput").value);
      $("itemInput").value = "";
      $("itemInput").focus();
    };
    $("itemInput").addEventListener("keydown", (e)=>{ if(e.key === "Enter") $("addBtn").click(); });

    $("shakeBtn").onclick = shake;
    $("shuffleBtn").onclick = shuffleItems;
    $("resetBtn").onclick = resetAll;
    $("clearHistoryBtn").onclick = clearHistory;

    $("soundOn").addEventListener("change", ()=>{
      save();
      if(soundEnabled()){
        playTone({freq:880, dur:0.06, type:"sine", gain:0.04});
        setTimeout(()=>playTone({freq:1100, dur:0.07, type:"sine", gain:0.04}), 80);
      }else{
        setResult("ปิดเสียงแล้ว 🔇");
      }
    });
    document.addEventListener("pointerdown", ()=>{ if(soundEnabled()) ensureAudio(); }, {once:true});
  }

  init();
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            data = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"404 Not Found")

def run(host="127.0.0.1", port=8000):
    httpd = HTTPServer((host, port), Handler)
    print("✅ Ball Shake Random App is running!")
    print(f"🌐 Open: http://{host}:{port}")
    print("🛑 Stop: Press Ctrl + C")
    httpd.serve_forever()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    run(host="0.0.0.0", port=port)