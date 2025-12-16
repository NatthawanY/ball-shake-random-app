#!/usr/bin/env python3
# Ball Shake Random App (run from terminal)
# เปิดเว็บที่ http://localhost:8000

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
      min-height:100vh;
      display:flex; align-items:center; justify-content:center;
      padding:24px;
    }
    .app{
      width:min(980px, 100%);
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
    header h1{
      font-size:18px; margin:0;
      display:flex; align-items:center; gap:10px;
    }
    .badge{
      font-size:12px; padding:5px 10px;
      border-radius:999px; background:#fff;
      border:1px solid rgba(0,0,0,.06);
      color:var(--muted);
    }
    main{ padding:18px 20px 22px; display:grid; gap:16px; grid-template-columns: 1.2fr .8fr;}
    @media (max-width: 860px){ main{grid-template-columns:1fr;} }

    .card{
      background:#fff;
      border:1px solid rgba(0,0,0,.06);
      border-radius: var(--radius);
      box-shadow: 0 8px 20px rgba(0,0,0,.06);
      padding:16px;
    }
    .row{display:flex; gap:10px; flex-wrap:wrap; align-items:center;}
    input[type="text"]{
      flex:1;
      padding:12px 12px;
      border-radius:14px;
      border:1px solid rgba(0,0,0,.12);
      outline:none;
      font-size:14px;
    }
    input[type="text"]:focus{border-color: rgba(255,105,180,.55); box-shadow: 0 0 0 4px rgba(255,105,180,.12);}
    button{
      border:none; cursor:pointer;
      padding:11px 14px;
      border-radius: 14px;
      font-weight:700;
      transition:.15s transform, .15s opacity;
      user-select:none;
    }
    button:active{transform: scale(.98);}
    .btn-add{background: linear-gradient(90deg,#7cf0c9,#67b7ff); color:#063b2b;}
    .btn-shake{background: linear-gradient(90deg,#ff7ab6,#ffd56a); color:#4a2a00;}
    .btn-clear{background:#f3f3f3; color:#333;}
    .btn-mini{
      padding:7px 10px; font-weight:700; border-radius: 12px;
      background:#f4f6ff; color:#2d3a8c;
    }
    .btn-mini.danger{background:#fff0f0; color:#a01818;}
    .muted{color:var(--muted); font-size:13px; margin:6px 0 0;}
    .balls{
      display:flex; flex-wrap:wrap; gap:10px;
      margin-top:12px;
      min-height:62px;
      align-items:center;
    }
    .ball{
      width:54px; height:54px;
      border-radius: 50%;
      display:flex; align-items:center; justify-content:center;
      color:#fff; font-weight:900;
      box-shadow: inset 0 -8px 18px rgba(0,0,0,.18), 0 10px 18px rgba(0,0,0,.10);
      position:relative;
      transform: translateZ(0);
    }
    .ball span{
      display:block;
      max-width:46px;
      font-size:12px;
      line-height:1.05;
      text-align:center;
      padding:0 6px;
      text-shadow: 0 2px 6px rgba(0,0,0,.25);
      overflow:hidden;
      white-space:nowrap;
      text-overflow:ellipsis;
    }
    .ball.selected{
      outline: 4px solid rgba(255,255,255,.95);
      box-shadow: 0 0 0 6px rgba(255,105,180,.25), inset 0 -8px 18px rgba(0,0,0,.18), 0 16px 30px rgba(0,0,0,.18);
      animation: pop .35s ease both;
    }
    @keyframes pop{ from{transform:scale(.9)} to{transform:scale(1)} }

    .shake-area{
      display:flex; align-items:center; justify-content:center;
      padding:18px 12px 8px;
    }
    .jar{
      width:210px; height:210px; border-radius: 34px;
      background: linear-gradient(180deg, #ffffff, #f7f7ff);
      border:1px solid rgba(0,0,0,.06);
      box-shadow: var(--shadow);
      position:relative;
      overflow:hidden;
      display:flex; align-items:center; justify-content:center;
    }
    .jar::before{
      content:"";
      position:absolute; inset:-40px -40px auto auto;
      width:120px; height:120px;
      background: radial-gradient(circle, rgba(255,122,182,.35), transparent 60%);
      transform: rotate(25deg);
    }
    .jar .bigball{
      width:120px; height:120px; border-radius:50%;
      background: radial-gradient(circle at 30% 25%, rgba(255,255,255,.9), rgba(255,255,255,.0) 30%),
                  linear-gradient(135deg,#ff7ab6,#67b7ff);
      box-shadow: inset 0 -12px 24px rgba(0,0,0,.18), 0 18px 28px rgba(0,0,0,.16);
      display:flex; align-items:center; justify-content:center;
      font-weight:900; color:#fff; text-shadow: 0 2px 8px rgba(0,0,0,.25);
      position:relative;
    }
    .jar .bigball small{
      display:block; opacity:.95; font-size:12px; font-weight:800;
      padding:0 12px; text-align:center;
    }
    .jar.shaking{ animation: shake .6s ease-in-out; }
    @keyframes shake{
      0%,100%{transform:translateX(0) rotate(0deg)}
      15%{transform:translateX(-6px) rotate(-3deg)}
      30%{transform:translateX(6px) rotate(3deg)}
      45%{transform:translateX(-5px) rotate(-2deg)}
      60%{transform:translateX(5px) rotate(2deg)}
      75%{transform:translateX(-3px) rotate(-1deg)}
    }

    .result{
      margin-top:10px;
      padding:12px 14px;
      border-radius: 14px;
      background: #f7fbff;
      border:1px solid rgba(103,183,255,.35);
    }
    .result strong{font-size:14px;}
    .list{
      margin-top:10px;
      display:grid; gap:8px;
    }
    .item-row{
      display:flex; align-items:center; justify-content:space-between; gap:10px;
      padding:10px 12px;
      border-radius: 14px;
      border:1px solid rgba(0,0,0,.06);
      background:#fff;
    }
    .item-row .name{font-weight:800;}
    .hint{font-size:12px; color:var(--muted); margin-top:10px; line-height:1.5;}
    .counter{font-weight:900;}
  </style>
</head>
<body>
  <div class="app">
    <header>
      <h1>🫧 Ball Shake Random App <span class="badge">รันจาก Terminal • ใช้ใน Browser</span></h1>
      <div class="badge">เหลือ <span class="counter" id="count">0</span> รายการ</div>
    </header>

    <main>
      <!-- Left: items / balls -->
      <section class="card">
        <div class="row">
          <input id="itemInput" type="text" placeholder="พิมพ์รายการ… เช่น 'กินชาบู' แล้วกด เพิ่ม" />
          <button class="btn-add" id="addBtn">➕ เพิ่ม</button>
          <button class="btn-clear" id="resetBtn" title="ล้างรายการทั้งหมด">🧹 ล้างทั้งหมด</button>
        </div>
        <div class="muted">เพิ่มได้หลายรายการ • แก้ไข/ลบได้ • ลูกบอล 1 ลูก = 1 รายการ</div>

        <div class="balls" id="balls"></div>

        <div class="list" id="list"></div>

        <div class="hint">
          ✅ ความยุติธรรม: สุ่มแบบ uniform (โอกาสเท่ากันทุก item) <br/>
          ✅ หลังสุ่ม: ระบบจะลบ item ที่ถูกสุ่มออก เพื่อสุ่มครั้งถัดไป
        </div>
      </section>

      <!-- Right: shake + result -->
      <aside class="card">
        <div class="shake-area">
          <div class="jar" id="jar">
            <div class="bigball" id="bigball"><small>กด “เขย่า” เพื่อสุ่ม</small></div>
          </div>
        </div>
        <div class="row" style="justify-content:center; margin-top:8px;">
          <button class="btn-shake" id="shakeBtn" style="min-width:180px;">🫨 เขย่า!</button>
        </div>

        <div class="result" id="resultBox" aria-live="polite">
          <strong>ผลลัพธ์:</strong>
          <div id="resultText" class="muted" style="margin-top:6px;">ยังไม่ได้สุ่ม</div>
        </div>

        <div class="hint">
          ทิป: ดับเบิลคลิกชื่อรายการในลิสต์เพื่อแก้ไขเร็ว ๆ ก็ได้
        </div>
      </aside>
    </main>
  </div>

<script>
  // ===== Data layer (localStorage) =====
  const KEY = "ball_shake_items_v1";

  /** @type {{id:string, name:string, color:string}[]} */
  let items = [];

  const palette = [
    "#ff7ab6","#67b7ff","#7cf0c9","#ffd56a","#b88cff",
    "#ff8a65","#4dd0e1","#81c784","#f06292","#9575cd"
  ];

  const $ = (id)=>document.getElementById(id);

  function uid(){
    return Math.random().toString(16).slice(2) + Date.now().toString(16);
  }

  function save(){
    localStorage.setItem(KEY, JSON.stringify(items));
  }

  function load(){
    try{
      const raw = localStorage.getItem(KEY);
      items = raw ? JSON.parse(raw) : [];
      if(!Array.isArray(items)) items = [];
    }catch(e){
      items = [];
    }
  }

  function pickColor(i){
    // เลือกสีวน ๆ เพื่อให้ดูหลากหลาย
    return palette[i % palette.length];
  }

  // ===== UI render =====
  function render(){
    $("count").textContent = items.length.toString();

    // Balls
    const balls = $("balls");
    balls.innerHTML = "";
    items.forEach((it, idx)=>{
      const d = document.createElement("div");
      d.className = "ball";
      d.style.background = `radial-gradient(circle at 30% 25%, rgba(255,255,255,.85), rgba(255,255,255,0) 32%), ${it.color}`;
      d.title = it.name;
      const s = document.createElement("span");
      s.textContent = it.name;
      d.appendChild(s);
      balls.appendChild(d);
    });

    // List
    const list = $("list");
    list.innerHTML = "";
    items.forEach((it)=>{
      const row = document.createElement("div");
      row.className = "item-row";

      const name = document.createElement("div");
      name.className = "name";
      name.textContent = it.name;
      name.style.cursor = "pointer";
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
  }

  // ===== CRUD =====
  function addItem(name){
    const trimmed = (name ?? "").trim();
    if(!trimmed){
      alert("กรุณาพิมพ์ชื่อรายการก่อน");
      return;
    }
    // สร้าง item ใหม่
    const it = {
      id: uid(),
      name: trimmed,
      color: pickColor(items.length)
    };
    items.push(it);
    save();
    render();
  }

  function removeItem(id){
    items = items.filter(x => x.id !== id);
    save();
    render();
  }

  function startEdit(id){
    const it = items.find(x => x.id === id);
    if(!it) return;

    const next = prompt("แก้ไขชื่อรายการ:", it.name);
    if(next === null) return; // cancel
    const trimmed = next.trim();
    if(!trimmed){
      alert("ชื่อรายการต้องไม่ว่าง");
      return;
    }
    it.name = trimmed;
    save();
    render();
  }

  function resetAll(){
    if(!confirm("ล้างรายการทั้งหมดจริงไหม?")) return;
    items = [];
    save();
    render();
    setResult("ล้างรายการแล้ว ✅");
  }

  // ===== Random / Shake =====
  function setResult(text){
    $("resultText").textContent = text;
    $("bigball").innerHTML = `<small>${escapeHtml(text)}</small>`;
  }

  function escapeHtml(s){
    return String(s)
      .replaceAll("&","&amp;")
      .replaceAll("<","&lt;")
      .replaceAll(">","&gt;");
  }

  function sleep(ms){ return new Promise(r=>setTimeout(r, ms)); }

  async function shake(){
    if(items.length === 0){
      alert("ยังไม่มีรายการให้สุ่ม — เพิ่มรายการก่อนนะ");
      return;
    }

    // ทำ animation เขย่า
    const jar = $("jar");
    jar.classList.add("shaking");
    setResult("กำลังเขย่า… 🫨");
    await sleep(650);
    jar.classList.remove("shaking");

    // สุ่มแบบยุติธรรม: uniform random index
    const idx = Math.floor(Math.random() * items.length);
    const picked = items[idx];

    // ไฮไลท์ลูกบอลที่ถูกเลือก
    const ballEls = Array.from(document.querySelectorAll(".ball"));
    ballEls.forEach(b => b.classList.remove("selected"));
    if(ballEls[idx]) ballEls[idx].classList.add("selected");

    setResult(`สุ่มได้: ${picked.name} 🎉`);

    // ลบรายการที่ถูกสุ่มออก (ตาม requirement)
    items.splice(idx, 1);
    save();

    // render หลังหน่วงนิดนึงให้เห็น highlight
    await sleep(550);
    render();

    if(items.length === 0){
      await sleep(200);
      setResult("สุ่มครบแล้ว 🎊 (รายการหมด)");
    }
  }

  // ===== Wire up =====
  function init(){
    load();
    // เติมสีให้ item เก่า (เผื่อเวอร์ชันก่อนหน้า)
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

    $("itemInput").addEventListener("keydown", (e)=>{
      if(e.key === "Enter") $("addBtn").click();
    });

    $("shakeBtn").onclick = shake;
    $("resetBtn").onclick = resetAll;
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

        if self.path == "/health":
            data = b"ok"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
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

