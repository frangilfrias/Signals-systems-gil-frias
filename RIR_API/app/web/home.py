"""HTML de la homepage de RIR-API."""

HOME_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RIR-API :: Acoustic Signal Engine</title>
<style>
  :root{
    --bg:#04060c;
    --cyan:#39f5ff;
    --magenta:#ff2ee0;
    --violet:#7c4dff;
    --green:#39ffb0;
    --panel:rgba(14,18,32,0.65);
    --border:rgba(57,245,255,0.25);
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;background:var(--bg);color:#eaf6ff;font-family:'Consolas','Segoe UI',monospace;overflow-x:hidden;}
  canvas#bg{position:fixed;inset:0;width:100%;height:100%;z-index:0;}
  .wrap{position:relative;z-index:1;max-width:980px;margin:0 auto;padding:4rem 1.5rem 5rem;}

  header{text-align:center;margin-bottom:3.5rem;}
  h1.logo{
    font-size:3.4rem;
    margin:0;
    letter-spacing:0.12em;
    font-weight:800;
    background:linear-gradient(90deg,var(--cyan),var(--violet),var(--magenta),var(--cyan));
    background-size:300% 100%;
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent;
    animation:hue 6s linear infinite;
    text-shadow:0 0 40px rgba(57,245,255,0.25);
    position:relative;
  }
  h1.logo::before{
    content:'RIR-API';
    position:absolute;left:2px;top:0;width:100%;
    color:var(--magenta);
    opacity:0.55;
    clip-path:inset(0 0 55% 0);
    animation:glitch 3.2s infinite steps(1);
  }
  @keyframes hue{ to{ background-position:300% 0; } }
  @keyframes glitch{
    0%,89%,100%{ transform:translate(0,0); opacity:0; }
    90%{ transform:translate(-3px,-1px); opacity:0.6; }
    92%{ transform:translate(3px,1px); opacity:0.5; }
    94%{ transform:translate(-2px,0); opacity:0; }
  }
  .subtitle{
    margin-top:0.6rem;
    letter-spacing:0.35em;
    text-transform:uppercase;
    font-size:0.8rem;
    color:#7fb8c9;
  }
  .status{
    display:inline-flex;align-items:center;gap:0.5rem;
    margin-top:1.4rem;padding:0.35rem 1rem;
    border:1px solid var(--border);border-radius:999px;
    font-size:0.75rem;color:var(--cyan);
    background:rgba(57,245,255,0.05);
  }
  .dot{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);animation:pulse 1.6s ease-in-out infinite;}
  @keyframes pulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.4;transform:scale(0.7);}}

  .tabs-bar{
    display:flex;flex-wrap:wrap;gap:1.6rem;
    margin:0 0 2rem;padding-bottom:1.4rem;
    border-bottom:1px solid var(--border);
  }
  .tab-group{display:flex;flex-direction:column;gap:0.6rem;}
  .tab-group-label{
    font-size:0.65rem;letter-spacing:0.25em;text-transform:uppercase;color:var(--violet);
  }
  .tab-buttons-row{display:flex;flex-wrap:wrap;gap:0.5rem;}
  .tab-btn{
    font-family:inherit;font-size:0.78rem;letter-spacing:0.02em;
    padding:0.5rem 0.9rem;border-radius:999px;cursor:pointer;
    border:1px solid var(--border);background:rgba(57,245,255,0.05);color:#9fb4c2;
    transition:all 0.2s ease;
  }
  .tab-btn:hover{color:#eaf6ff;border-color:var(--cyan);}
  .tab-btn.active{
    background:linear-gradient(90deg,var(--cyan),var(--magenta));
    color:#04060c;font-weight:700;border-color:transparent;
    box-shadow:0 0 18px rgba(57,245,255,0.35);
  }

  .tab-panel{display:none;}
  .tab-panel.active{display:block;animation:fadein 0.25s ease;}
  @keyframes fadein{ from{opacity:0;transform:translateY(6px);} to{opacity:1;transform:translateY(0);} }

  .panel{
    background:var(--panel);
    border:1px solid var(--border);
    border-radius:18px;
    padding:2rem;
    backdrop-filter:blur(10px);
    box-shadow:0 0 0 1px rgba(255,255,255,0.02), 0 20px 60px rgba(0,0,0,0.5);
    position:relative;
    overflow:hidden;
    margin-bottom:1.6rem;
  }
  .panel::before{
    content:'';position:absolute;inset:-2px;border-radius:18px;padding:1px;
    background:linear-gradient(120deg,var(--cyan),transparent 30%,transparent 70%,var(--magenta));
    -webkit-mask:linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
    -webkit-mask-composite:xor;mask-composite:exclude;
    opacity:0.5;pointer-events:none;
  }

  .endpoint-head{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.8rem;margin-bottom:0.4rem;}
  .method{
    background:linear-gradient(90deg,var(--magenta),var(--violet));
    padding:0.2rem 0.7rem;border-radius:6px;font-size:0.75rem;font-weight:700;letter-spacing:0.05em;
    color:#fff;
  }
  .method.get{background:linear-gradient(90deg,var(--green),var(--cyan));color:#04060c;}
  .path{font-size:1.05rem;color:#fff;}
  .desc{color:#9fb4c2;font-size:0.9rem;margin:0.6rem 0 1.6rem;line-height:1.5;}

  .controls{display:grid;grid-template-columns:1fr 1fr;gap:1.4rem;margin-bottom:1.6rem;}
  @media(max-width:640px){.controls{grid-template-columns:1fr;}}
  .param.full{grid-column:1 / -1;}

  label{display:block;font-size:0.72rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--cyan);margin-bottom:0.5rem;}
  .value-tag{float:right;color:#fff;background:rgba(124,77,255,0.25);padding:0 0.5rem;border-radius:4px;font-size:0.72rem;}

  input[type=range]{
    -webkit-appearance:none;width:100%;height:6px;border-radius:4px;
    background:linear-gradient(90deg,var(--cyan),var(--violet));outline:none;
  }
  input[type=range]::-webkit-slider-thumb{
    -webkit-appearance:none;width:18px;height:18px;border-radius:50%;
    background:#fff;box-shadow:0 0 10px var(--cyan),0 0 0 4px rgba(57,245,255,0.25);cursor:pointer;
  }

  select, input[type=file]{
    width:100%;padding:0.6rem 0.7rem;border-radius:8px;
    background:#0c1420;border:1px solid var(--border);color:#eaf6ff;font-family:inherit;font-size:0.9rem;
  }
  input[type=file]{border-style:dashed;color:#9fb4c2;font-size:0.82rem;}

  .generate-btn{
    position:relative;width:100%;padding:1rem;border:none;border-radius:12px;cursor:pointer;
    font-family:inherit;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;font-size:0.85rem;
    color:#04060c;background:linear-gradient(90deg,var(--cyan),var(--magenta));
    background-size:220% 100%;
    box-shadow:0 0 25px rgba(57,245,255,0.35);
    transition:transform 0.15s ease, box-shadow 0.15s ease, background-position 0.4s ease;
    overflow:hidden;
  }
  .generate-btn:hover{transform:translateY(-2px);box-shadow:0 6px 30px rgba(255,46,224,0.45);background-position:100% 0;}
  .generate-btn:active{transform:translateY(0);}
  .generate-btn:disabled{opacity:0.55;cursor:progress;transform:none;}

  .viz-wrap{margin-top:1.8rem;border-radius:12px;border:1px solid var(--border);background:#020409;overflow:hidden;}
  canvas.viz{display:block;width:100%;height:150px;}

  .player-row{display:flex;align-items:center;gap:0.9rem;margin-top:1rem;flex-wrap:wrap;}
  .icon-btn{
    width:44px;height:44px;border-radius:50%;border:1px solid var(--border);
    background:rgba(57,245,255,0.08);color:var(--cyan);font-size:1.1rem;cursor:pointer;
    display:flex;align-items:center;justify-content:center;transition:all 0.2s ease;flex:none;
  }
  .icon-btn:hover{background:var(--cyan);color:#04060c;box-shadow:0 0 15px var(--cyan);}
  .icon-btn:disabled{opacity:0.35;cursor:not-allowed;}
  .dl-link{
    color:var(--violet);text-decoration:none;font-size:0.8rem;letter-spacing:0.08em;
    border:1px solid var(--border);padding:0.6rem 1rem;border-radius:8px;transition:all 0.2s ease;
  }
  .dl-link:hover{background:rgba(124,77,255,0.15);color:#fff;}
  .meta{font-size:0.75rem;color:#7fb8c9;margin-left:auto;}

  .status-line{margin-top:0.9rem;font-size:0.78rem;color:#7fb8c9;min-height:1.1rem;}
  .status-line.error{color:#ff5d7a;}
  .status-line.ok{color:var(--green);}

  .result-box:not(:empty){margin-top:1.4rem;}
  .result-sub-title{font-size:0.72rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--cyan);margin:1rem 0 0.4rem;}
  .tag-row{display:flex;flex-wrap:wrap;gap:0.5rem;margin:0.6rem 0;}
  .tag-row .value-tag{float:none;}
  canvas.sparkline{width:100%;height:60px;display:block;margin-bottom:0.4rem;}
  .table-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:8px;}
  table{width:100%;border-collapse:collapse;font-size:0.78rem;}
  th,td{padding:0.45rem 0.7rem;text-align:right;border-bottom:1px solid rgba(255,255,255,0.06);white-space:nowrap;}
  th:first-child, td:first-child{text-align:left;color:var(--cyan);}
  thead th{color:#9fb4c2;font-weight:600;text-transform:uppercase;font-size:0.68rem;letter-spacing:0.05em;}

  footer{margin-top:4rem;text-align:center;color:#5a7180;font-size:0.75rem;letter-spacing:0.05em;}
  footer a{color:var(--cyan);text-decoration:none;}
  footer a:hover{text-decoration:underline;}
  .crew{margin-top:0.6rem;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;color:#9fb4c2;}
</style>
</head>
<body>
<canvas id="bg"></canvas>
<div class="wrap">

  <header>
    <h1 class="logo">RIR-API</h1>
    <div class="subtitle">Acoustic Signal Processing Engine · ISO 3382</div>
    <div class="status"><span class="dot"></span> SYSTEM ONLINE · v1.0.0</div>
  </header>

  <div class="tabs-bar">
    <div class="tab-group">
      <span class="tab-group-label">Señales</span>
      <div class="tab-buttons-row">
        <button class="tab-btn active" data-tab="pink-noise">Ruido rosa</button>
        <button class="tab-btn" data-tab="sine-sweep">Sine sweep</button>
        <button class="tab-btn" data-tab="synthetic-ir">RI sintética</button>
      </div>
    </div>
    <div class="tab-group">
      <span class="tab-group-label">Filtros</span>
      <div class="tab-buttons-row">
        <button class="tab-btn" data-tab="filter-band">Filtro de banda</button>
        <button class="tab-btn" data-tab="filter-frequencies">Bandas</button>
      </div>
    </div>
    <div class="tab-group">
      <span class="tab-group-label">Análisis y utilidades</span>
      <div class="tab-buttons-row">
        <button class="tab-btn" data-tab="acoustic-parameters">Parámetros</button>
        <button class="tab-btn" data-tab="acoustic-by-bands">Por banda</button>
        <button class="tab-btn" data-tab="analysis-ir">Análisis IR</button>
        <button class="tab-btn" data-tab="utils-schroeder">Schroeder</button>
        <button class="tab-btn" data-tab="utils-smoothing">Suavizado</button>
        <button class="tab-btn" data-tab="utils-log-scale">Escala log</button>
      </div>
    </div>
  </div>

  <div class="panel audio-card tab-panel active" data-tab-panel="pink-noise" data-endpoint="/api/v1/signals/pink-noise" data-filename="pink_noise.wav">
    <div class="endpoint-head">
      <div><span class="method">POST</span> <span class="path">/api/v1/signals/pink-noise</span></div>
      <span class="value-tag">audio/wav</span>
    </div>
    <p class="desc">Ruido rosa (densidad espectral 1/f): cada octava contiene la misma energía. Útil como
      excitación para mediciones acústicas.</p>
    <div class="controls">
      <div class="param" data-param="duracion" data-type="range" data-unit="s" data-decimals="1">
        <label>Duración <span class="value-tag param-value"></span></label>
        <input type="range" min="0.1" max="30" step="0.1" value="5">
      </div>
      <div class="param" data-param="fs" data-type="select">
        <label>Frecuencia de muestreo</label>
        <select>
          <option value="44100" selected>44100 Hz</option>
          <option value="48000">48000 Hz</option>
          <option value="88200">88200 Hz</option>
          <option value="96000">96000 Hz</option>
          <option value="176400">176400 Hz</option>
          <option value="192000">192000 Hz</option>
          <option value="352800">352800 Hz</option>
          <option value="384000">384000 Hz</option>
          <option value="705600">705600 Hz</option>
          <option value="768000">768000 Hz</option>
        </select>
      </div>
    </div>
    <button class="generate-btn">▶ Generar ruido rosa</button>
    <div class="viz-wrap"><canvas class="viz"></canvas></div>
    <div class="player-row">
      <button class="icon-btn play-btn" disabled>▶</button>
      <a class="dl-link" style="pointer-events:none;opacity:0.4;">⭳ Descargar WAV</a>
      <span class="meta"></span>
    </div>
    <div class="status-line">Esperando parámetros...</div>
  </div>

  <div class="panel audio-card tab-panel" data-tab-panel="sine-sweep" data-endpoint="/api/v1/signals/sine-sweep" data-filename="sine_sweep.wav">
    <div class="endpoint-head">
      <div><span class="method">POST</span> <span class="path">/api/v1/signals/sine-sweep</span></div>
      <span class="value-tag">audio/wav</span>
    </div>
    <p class="desc">Barrido senoidal (sine sweep) logarítmico entre dos frecuencias, usado para excitar
      recintos y luego derivar la respuesta al impulso.</p>
    <div class="controls">
      <div class="param" data-param="f1" data-type="range" data-unit="Hz">
        <label>Frecuencia inicial <span class="value-tag param-value"></span></label>
        <input type="range" min="10" max="1000" step="1" value="20">
      </div>
      <div class="param" data-param="f2" data-type="range" data-unit="Hz">
        <label>Frecuencia final <span class="value-tag param-value"></span></label>
        <input type="range" min="1000" max="22000" step="100" value="20000">
      </div>
      <div class="param" data-param="duracion" data-type="range" data-unit="s" data-decimals="1">
        <label>Duración <span class="value-tag param-value"></span></label>
        <input type="range" min="0.5" max="20" step="0.5" value="5">
      </div>
      <div class="param" data-param="fs" data-type="select">
        <label>Frecuencia de muestreo</label>
        <select>
          <option value="44100" selected>44100 Hz</option>
          <option value="48000">48000 Hz</option>
          <option value="96000">96000 Hz</option>
        </select>
      </div>
    </div>
    <button class="generate-btn">▶ Generar sine sweep</button>
    <div class="viz-wrap"><canvas class="viz"></canvas></div>
    <div class="player-row">
      <button class="icon-btn play-btn" disabled>▶</button>
      <a class="dl-link" style="pointer-events:none;opacity:0.4;">⭳ Descargar WAV</a>
      <span class="meta"></span>
    </div>
    <div class="status-line">Esperando parámetros...</div>
  </div>

  <div class="panel audio-card tab-panel" data-tab-panel="synthetic-ir" data-endpoint="/api/v1/signals/synthetic-ir" data-filename="synthetic_ir.wav">
    <div class="endpoint-head">
      <div><span class="method">POST</span> <span class="path">/api/v1/signals/synthetic-ir</span></div>
      <span class="value-tag">audio/wav</span>
    </div>
    <p class="desc">Respuesta al impulso sintética generada a partir de tiempos de reverberación
      predefinidos por banda de octava (125 Hz a 4 kHz).</p>
    <div class="controls">
      <div class="param" data-param="duracion" data-type="range" data-unit="s" data-decimals="1">
        <label>Duración <span class="value-tag param-value"></span></label>
        <input type="range" min="0.5" max="10" step="0.5" value="3">
      </div>
      <div class="param" data-param="fs" data-type="select">
        <label>Frecuencia de muestreo</label>
        <select>
          <option value="44100" selected>44100 Hz</option>
          <option value="48000">48000 Hz</option>
          <option value="96000">96000 Hz</option>
        </select>
      </div>
    </div>
    <button class="generate-btn">▶ Sintetizar RI</button>
    <div class="viz-wrap"><canvas class="viz"></canvas></div>
    <div class="player-row">
      <button class="icon-btn play-btn" disabled>▶</button>
      <a class="dl-link" style="pointer-events:none;opacity:0.4;">⭳ Descargar WAV</a>
      <span class="meta"></span>
    </div>
    <div class="status-line">Esperando parámetros...</div>
  </div>

  <div class="panel audio-card tab-panel" data-tab-panel="filter-band" data-endpoint="/api/v1/filters/band" data-filename="band_filtered.wav">
    <div class="endpoint-head">
      <div><span class="method">POST</span> <span class="path">/api/v1/filters/band</span></div>
      <span class="value-tag">audio/wav</span>
    </div>
    <p class="desc">Filtro pasabanda Butterworth de una octava (IEC 61260), aplicado sobre un archivo de
      audio propio.</p>
    <div class="controls">
      <div class="param full" data-param="__file" data-type="file">
        <label>Archivo de audio (WAV / FLAC)</label>
        <input type="file" name="archivo" accept=".wav,.flac">
      </div>
      <div class="param" data-param="fc" data-type="select">
        <label>Frecuencia central</label>
        <select>
          <option value="31.5">31.5 Hz</option>
          <option value="63">63 Hz</option>
          <option value="125">125 Hz</option>
          <option value="250">250 Hz</option>
          <option value="500">500 Hz</option>
          <option value="1000" selected>1000 Hz</option>
          <option value="2000">2000 Hz</option>
          <option value="4000">4000 Hz</option>
          <option value="8000">8000 Hz</option>
        </select>
      </div>
      <div class="param" data-param="orden" data-type="range">
        <label>Orden del filtro <span class="value-tag param-value"></span></label>
        <input type="range" min="2" max="8" step="2" value="4">
      </div>
    </div>
    <button class="generate-btn">▶ Aplicar filtro</button>
    <div class="viz-wrap"><canvas class="viz"></canvas></div>
    <div class="player-row">
      <button class="icon-btn play-btn" disabled>▶</button>
      <a class="dl-link" style="pointer-events:none;opacity:0.4;">⭳ Descargar WAV</a>
      <span class="meta"></span>
    </div>
    <div class="status-line">Subí un archivo para empezar.</div>
  </div>

  <div class="panel json-card tab-panel" data-tab-panel="filter-frequencies" data-endpoint="/api/v1/filters/frequencies" data-method="GET">
    <div class="endpoint-head">
      <div><span class="method get">GET</span> <span class="path">/api/v1/filters/frequencies</span></div>
      <span class="value-tag">json</span>
    </div>
    <p class="desc">Frecuencias centrales de las bandas de octava soportadas por el filtro pasabanda.</p>
    <button class="generate-btn">▶ Consultar bandas</button>
    <div class="result-box"></div>
    <div class="status-line">Esperando consulta...</div>
  </div>

  <div class="panel json-card tab-panel" data-tab-panel="acoustic-parameters" data-endpoint="/api/v1/acoustics/parameters" data-method="POST">
    <div class="endpoint-head">
      <div><span class="method">POST</span> <span class="path">/api/v1/acoustics/parameters</span></div>
      <span class="value-tag">json</span>
    </div>
    <p class="desc">Calcula los parámetros acústicos (T20, T30, EDT, C50, C80, etc.) de una respuesta al
      impulso, por banda de octava.</p>
    <div class="controls">
      <div class="param full" data-param="__file" data-type="file">
        <label>Respuesta al impulso (WAV / FLAC)</label>
        <input type="file" name="file" accept=".wav,.flac">
      </div>
    </div>
    <button class="generate-btn">▶ Calcular parámetros</button>
    <div class="result-box"></div>
    <div class="status-line">Subí un archivo para empezar.</div>
  </div>

  <div class="panel json-card tab-panel" data-tab-panel="acoustic-by-bands" data-endpoint="/api/v1/acoustics/by-bands" data-method="POST">
    <div class="endpoint-head">
      <div><span class="method">POST</span> <span class="path">/api/v1/acoustics/by-bands</span></div>
      <span class="value-tag">json</span>
    </div>
    <p class="desc">Misma métrica que el endpoint anterior, pero agrupada por banda de octava en lugar de
      por parámetro.</p>
    <div class="controls">
      <div class="param full" data-param="__file" data-type="file">
        <label>Respuesta al impulso (WAV / FLAC)</label>
        <input type="file" name="file" accept=".wav,.flac">
      </div>
    </div>
    <button class="generate-btn">▶ Calcular por banda</button>
    <div class="result-box"></div>
    <div class="status-line">Subí un archivo para empezar.</div>
  </div>

  <div class="panel json-card tab-panel" data-tab-panel="analysis-ir" data-endpoint="/api/v1/analysis/impulse-response" data-method="POST">
    <div class="endpoint-head">
      <div><span class="method">POST</span> <span class="path">/api/v1/analysis/impulse-response</span></div>
      <span class="value-tag">json</span>
    </div>
    <p class="desc">Análisis completo: curva de Schroeder en dB y parámetros acústicos, en una sola
      llamada.</p>
    <div class="controls">
      <div class="param full" data-param="__file" data-type="file">
        <label>Respuesta al impulso (WAV / FLAC)</label>
        <input type="file" name="file" accept=".wav,.flac">
      </div>
    </div>
    <button class="generate-btn">▶ Analizar</button>
    <div class="result-box"></div>
    <div class="status-line">Subí un archivo para empezar.</div>
  </div>

  <div class="panel json-card tab-panel" data-tab-panel="utils-schroeder" data-endpoint="/api/v1/utils/schroeder" data-method="POST">
    <div class="endpoint-head">
      <div><span class="method">POST</span> <span class="path">/api/v1/utils/schroeder</span></div>
      <span class="value-tag">json</span>
    </div>
    <p class="desc">Integral de Schroeder de una respuesta al impulso (curva de decaimiento energético).</p>
    <div class="controls">
      <div class="param full" data-param="__file" data-type="file">
        <label>Respuesta al impulso (WAV / FLAC)</label>
        <input type="file" name="file" accept=".wav,.flac">
      </div>
    </div>
    <button class="generate-btn">▶ Calcular integral</button>
    <div class="result-box"></div>
    <div class="status-line">Subí un archivo para empezar.</div>
  </div>

  <div class="panel json-card tab-panel" data-tab-panel="utils-smoothing" data-endpoint="/api/v1/utils/smoothing" data-method="POST">
    <div class="endpoint-head">
      <div><span class="method">POST</span> <span class="path">/api/v1/utils/smoothing</span></div>
      <span class="value-tag">json</span>
    </div>
    <p class="desc">Suaviza una señal mediante la envolvente de Hilbert o una media móvil de ventana
      configurable.</p>
    <div class="controls">
      <div class="param full" data-param="__file" data-type="file">
        <label>Señal de audio (WAV / FLAC)</label>
        <input type="file" name="file" accept=".wav,.flac">
      </div>
      <div class="param" data-param="method" data-type="select">
        <label>Método</label>
        <select>
          <option value="hilbert" selected>Hilbert</option>
          <option value="moving_average">Media móvil</option>
        </select>
      </div>
      <div class="param" data-param="window_ms" data-type="range" data-unit="ms">
        <label>Ventana <span class="value-tag param-value"></span></label>
        <input type="range" min="1" max="100" step="1" value="10">
      </div>
    </div>
    <button class="generate-btn">▶ Suavizar señal</button>
    <div class="result-box"></div>
    <div class="status-line">Subí un archivo para empezar.</div>
  </div>

  <div class="panel json-card tab-panel" data-tab-panel="utils-log-scale" data-endpoint="/api/v1/utils/log-scale" data-method="POST">
    <div class="endpoint-head">
      <div><span class="method">POST</span> <span class="path">/api/v1/utils/log-scale</span></div>
      <span class="value-tag">json</span>
    </div>
    <p class="desc">Convierte una señal a escala logarítmica (dB), útil para visualizar decaimientos y
      espectros.</p>
    <div class="controls">
      <div class="param full" data-param="__file" data-type="file">
        <label>Señal de audio (WAV / FLAC)</label>
        <input type="file" name="file" accept=".wav,.flac">
      </div>
    </div>
    <button class="generate-btn">▶ Convertir a dB</button>
    <div class="result-box"></div>
    <div class="status-line">Subí un archivo para empezar.</div>
  </div>

  <footer>
    Trabajo Práctico · Señales y Sistemas · Grupo 1
    <div class="crew">
      <span>Mora Sawczyk</span><span>·</span><span>Matias Moreira</span><span>·</span><span>Francisco Gil Frias</span>
    </div>
    <div style="margin-top:1rem;"><a href="/docs">Documentación completa de la API →</a></div>
  </footer>
</div>

<script>
// ---------- Fondo animado: campo de partículas ----------
const bg = document.getElementById('bg');
const bctx = bg.getContext('2d');
let W, H, particles = [];
function resizeBg(){
  W = bg.width = window.innerWidth;
  H = bg.height = window.innerHeight;
}
window.addEventListener('resize', resizeBg);
resizeBg();
const N_PARTICLES = 90;
for(let i=0;i<N_PARTICLES;i++){
  particles.push({
    x:Math.random()*W, y:Math.random()*H,
    vx:(Math.random()-0.5)*0.35, vy:(Math.random()-0.5)*0.35,
    r:Math.random()*1.8+0.4
  });
}
function drawBg(){
  bctx.clearRect(0,0,W,H);
  bctx.fillStyle = '#04060c';
  bctx.fillRect(0,0,W,H);
  for(const p of particles){
    p.x += p.vx; p.y += p.vy;
    if(p.x<0) p.x=W; if(p.x>W) p.x=0;
    if(p.y<0) p.y=H; if(p.y>H) p.y=0;
  }
  for(let i=0;i<particles.length;i++){
    for(let j=i+1;j<particles.length;j++){
      const a=particles[i], b=particles[j];
      const dx=a.x-b.x, dy=a.y-b.y;
      const d=Math.sqrt(dx*dx+dy*dy);
      if(d<130){
        bctx.strokeStyle = `rgba(57,245,255,${0.12*(1-d/130)})`;
        bctx.lineWidth=1;
        bctx.beginPath(); bctx.moveTo(a.x,a.y); bctx.lineTo(b.x,b.y); bctx.stroke();
      }
    }
  }
  for(const p of particles){
    bctx.beginPath();
    bctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    bctx.fillStyle = 'rgba(57,245,255,0.65)';
    bctx.fill();
  }
  requestAnimationFrame(drawBg);
}
drawBg();

// ---------- Helpers compartidos por las tarjetas de endpoints ----------
function bindParamLabels(paramEls){
  for(const p of paramEls){
    if(p.dataset.type !== 'range') continue;
    const input = p.querySelector('input');
    const label = p.querySelector('.param-value');
    const unit = p.dataset.unit || '';
    const decimals = p.dataset.decimals ? parseInt(p.dataset.decimals) : 0;
    const update = () => {
      const val = decimals > 0 ? parseFloat(input.value).toFixed(decimals) : input.value;
      label.textContent = val + (unit ? ' ' + unit : '');
    };
    input.addEventListener('input', update);
    update();
  }
}

function collectParams(paramEls){
  const qs = new URLSearchParams();
  let fileInput = null;
  for(const p of paramEls){
    if(p.dataset.type === 'file'){
      fileInput = p.querySelector('input[type=file]');
      continue;
    }
    const input = p.querySelector('input, select');
    qs.set(p.dataset.param, input.value);
  }
  return { qs, fileInput };
}

function buildUrl(endpoint, qs){
  const s = qs.toString();
  return s ? `${endpoint}?${s}` : endpoint;
}

function setStatus(el, msg, type){
  el.textContent = msg;
  el.className = 'status-line' + (type ? ' ' + type : '');
}

function sparkline(canvas, values){
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.clientWidth * devicePixelRatio;
  canvas.height = canvas.clientHeight * devicePixelRatio;
  const w = canvas.width, h = canvas.height;
  const min = Math.min(...values), max = Math.max(...values);
  const range = (max - min) || 1;
  ctx.clearRect(0,0,w,h);
  ctx.beginPath();
  values.forEach((v,i) => {
    const x = i/(values.length-1) * w;
    const y = h - ((v-min)/range) * h;
    i===0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
  });
  ctx.strokeStyle = '#39f5ff';
  ctx.lineWidth = 2;
  ctx.stroke();
  ctx.lineTo(w,h); ctx.lineTo(0,h); ctx.closePath();
  const grad = ctx.createLinearGradient(0,0,0,h);
  grad.addColorStop(0,'rgba(57,245,255,0.25)');
  grad.addColorStop(1,'rgba(57,245,255,0)');
  ctx.fillStyle = grad;
  ctx.fill();
}

function isScalarDict(obj){
  return obj && typeof obj === 'object' && !Array.isArray(obj) &&
    Object.values(obj).every(v => typeof v === 'number' || typeof v === 'string');
}
function isNestedScalarDict(obj){
  return obj && typeof obj === 'object' && !Array.isArray(obj) &&
    Object.values(obj).every(v => isScalarDict(v));
}
function formatNumber(v){
  return typeof v === 'number' ? (Number.isInteger(v) ? v : v.toFixed(3)) : v;
}
function renderTable(obj){
  const outerKeys = Object.keys(obj);
  const innerKeys = [...new Set(outerKeys.flatMap(k => Object.keys(obj[k])))];
  let html = '<div class="table-wrap"><table><thead><tr><th></th>' +
    innerKeys.map(k => `<th>${k}</th>`).join('') + '</tr></thead><tbody>';
  for(const ok of outerKeys){
    html += `<tr><th>${ok}</th>` +
      innerKeys.map(ik => `<td>${formatNumber(obj[ok][ik] ?? '—')}</td>`).join('') +
      '</tr>';
  }
  html += '</tbody></table></div>';
  return html;
}

function renderJsonResult(resultBox, json){
  const scalarEntries = [], previewEntries = [], tableEntries = [], arrayEntries = [];
  for(const [k,v] of Object.entries(json)){
    if(Array.isArray(v) && k.endsWith('_preview')) previewEntries.push([k,v]);
    else if(Array.isArray(v)) arrayEntries.push([k,v]);
    else if(isNestedScalarDict(v)) tableEntries.push([k,v]);
    else if(typeof v !== 'object') scalarEntries.push([k,v]);
  }
  let html = '';
  if(scalarEntries.length){
    html += '<div class="tag-row">' +
      scalarEntries.map(([k,v]) => `<span class="value-tag">${k}: ${formatNumber(v)}</span>`).join('') +
      '</div>';
  }
  for(const [k,v] of arrayEntries){
    html += `<div class="result-sub-title">${k}</div><div class="tag-row">` +
      v.map(x => `<span class="value-tag">${x}</span>`).join('') + '</div>';
  }
  for(const [k,v] of tableEntries){
    html += `<div class="result-sub-title">${k}</div>` + renderTable(v);
  }
  for(const [k,v] of previewEntries){
    html += `<div class="result-sub-title">${k} (${v.length} muestras)</div><canvas class="sparkline"></canvas>`;
  }
  resultBox.innerHTML = html;
  resultBox.querySelectorAll('canvas.sparkline').forEach((canvas, i) => {
    sparkline(canvas, previewEntries[i][1]);
  });
}

// ---------- Tarjetas que generan/transforman audio ----------
class AudioGenCard{
  constructor(panel){
    this.panel = panel;
    this.endpoint = panel.dataset.endpoint;
    this.filename = panel.dataset.filename;
    this.paramEls = [...panel.querySelectorAll('.param')];
    this.genBtn = panel.querySelector('.generate-btn');
    this.playBtn = panel.querySelector('.play-btn');
    this.dlLink = panel.querySelector('.dl-link');
    this.statusLine = panel.querySelector('.status-line');
    this.metaInfo = panel.querySelector('.meta');
    this.vizCanvas = panel.querySelector('.viz');
    this.vctx = this.vizCanvas.getContext('2d');
    this.audioCtx = null; this.analyser = null; this.sourceNode = null; this.audioEl = null;
    this.vizRunning = false; this.idleTimer = Math.random()*10;

    bindParamLabels(this.paramEls);
    this.fitCanvas();
    window.addEventListener('resize', () => this.fitCanvas());
    this.idleWave();

    this.genBtn.addEventListener('click', () => this.generate());
    this.playBtn.addEventListener('click', () => this.togglePlay());

    panel.__card = this;
  }
  fitCanvas(){
    this.vizCanvas.width = this.vizCanvas.clientWidth * devicePixelRatio;
    this.vizCanvas.height = this.vizCanvas.clientHeight * devicePixelRatio;
  }
  idleWave(){
    const vctx = this.vctx, canvas = this.vizCanvas;
    vctx.clearRect(0,0,canvas.width,canvas.height);
    const midY = canvas.height/2;
    vctx.strokeStyle = 'rgba(124,77,255,0.5)';
    vctx.lineWidth = 2;
    vctx.beginPath();
    for(let x=0;x<canvas.width;x++){
      const y = midY + Math.sin((x*0.02)+this.idleTimer)*6;
      x===0 ? vctx.moveTo(x,y) : vctx.lineTo(x,y);
    }
    vctx.stroke();
    this.idleTimer += 0.06;
    if(!this.vizRunning) requestAnimationFrame(() => this.idleWave());
  }
  drawSpectrum(){
    if(!this.analyser) return;
    const bufferLength = this.analyser.frequencyBinCount;
    const data = new Uint8Array(bufferLength);
    const canvas = this.vizCanvas, vctx = this.vctx;
    const frame = () => {
      if(!this.vizRunning) return;
      this.analyser.getByteFrequencyData(data);
      vctx.clearRect(0,0,canvas.width,canvas.height);
      const barW = canvas.width/bufferLength*2.5;
      let x = 0;
      for(let i=0;i<bufferLength;i++){
        const v = data[i]/255, barH = v*canvas.height;
        const grad = vctx.createLinearGradient(0,canvas.height-barH,0,canvas.height);
        grad.addColorStop(0,'#ff2ee0'); grad.addColorStop(1,'#39f5ff');
        vctx.fillStyle = grad;
        vctx.fillRect(x, canvas.height-barH, barW, barH);
        x += barW+1;
        if(x>canvas.width) break;
      }
      requestAnimationFrame(frame);
    };
    frame();
  }
  async generate(){
    const { qs, fileInput } = collectParams(this.paramEls);
    if(fileInput && !fileInput.files.length){
      setStatus(this.statusLine, 'Subí un archivo de audio primero.', 'error');
      return;
    }
    this.genBtn.disabled = true;
    this.playBtn.disabled = true;
    this.dlLink.style.pointerEvents = 'none';
    this.dlLink.style.opacity = '0.4';
    const originalText = this.genBtn.textContent;
    this.genBtn.textContent = '◌ Procesando...';
    setStatus(this.statusLine, 'Enviando solicitud al servidor...');
    try{
      const url = buildUrl(this.endpoint, qs);
      let res;
      if(fileInput){
        const fd = new FormData();
        fd.append(fileInput.name || 'archivo', fileInput.files[0]);
        res = await fetch(url, { method: 'POST', body: fd });
      }else{
        res = await fetch(url, { method: 'POST' });
      }
      if(!res.ok){
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || 'Error procesando la solicitud.');
      }
      const blob = await res.blob();
      const objUrl = URL.createObjectURL(blob);

      if(this.audioEl){ this.audioEl.pause(); this.vizRunning = false; }
      this.audioEl = new Audio(objUrl);

      if(!this.audioCtx) this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if(this.sourceNode) this.sourceNode.disconnect();
      this.sourceNode = this.audioCtx.createMediaElementSource(this.audioEl);
      this.analyser = this.audioCtx.createAnalyser();
      this.analyser.fftSize = 128;
      this.sourceNode.connect(this.analyser);
      this.analyser.connect(this.audioCtx.destination);

      this.dlLink.href = objUrl;
      this.dlLink.download = this.filename;
      this.dlLink.style.pointerEvents = 'auto';
      this.dlLink.style.opacity = '1';
      this.playBtn.disabled = false;
      this.playBtn.textContent = '▶';
      this.metaInfo.textContent = `${(blob.size/1024).toFixed(1)} KB`;
      setStatus(this.statusLine, 'Listo. Reproducí o descargá el resultado.', 'ok');

      this.audioEl.addEventListener('ended', () => {
        this.vizRunning = false;
        this.playBtn.textContent = '▶';
      });
    }catch(e){
      setStatus(this.statusLine, e.message || 'Ocurrió un error al procesar la solicitud.', 'error');
    }finally{
      this.genBtn.disabled = false;
      this.genBtn.textContent = originalText;
    }
  }
  async togglePlay(){
    if(!this.audioEl) return;
    if(this.audioCtx.state === 'suspended') await this.audioCtx.resume();
    if(this.audioEl.paused){
      this.audioEl.play();
      this.playBtn.textContent = '❚❚';
      this.vizRunning = true;
      this.drawSpectrum();
    }else{
      this.audioEl.pause();
      this.playBtn.textContent = '▶';
      this.vizRunning = false;
      setTimeout(() => this.idleWave(), 50);
    }
  }
}

// ---------- Tarjetas que devuelven JSON ----------
class JsonCard{
  constructor(panel){
    this.panel = panel;
    this.endpoint = panel.dataset.endpoint;
    this.method = panel.dataset.method || 'POST';
    this.paramEls = [...panel.querySelectorAll('.param')];
    this.genBtn = panel.querySelector('.generate-btn');
    this.resultBox = panel.querySelector('.result-box');
    this.statusLine = panel.querySelector('.status-line');

    bindParamLabels(this.paramEls);
    this.genBtn.addEventListener('click', () => this.run());
  }
  async run(){
    const { qs, fileInput } = collectParams(this.paramEls);
    if(fileInput && !fileInput.files.length){
      setStatus(this.statusLine, 'Subí un archivo primero.', 'error');
      return;
    }
    this.genBtn.disabled = true;
    const original = this.genBtn.textContent;
    this.genBtn.textContent = '◌ Procesando...';
    setStatus(this.statusLine, 'Consultando al servidor...');
    this.resultBox.innerHTML = '';
    try{
      const url = buildUrl(this.endpoint, qs);
      const opts = { method: this.method };
      if(fileInput){
        const fd = new FormData();
        fd.append(fileInput.name || 'file', fileInput.files[0]);
        opts.body = fd;
      }
      const res = await fetch(url, opts);
      const data = await res.json();
      if(!res.ok) throw new Error(data.detail || 'Error procesando la solicitud.');
      renderJsonResult(this.resultBox, data);
      setStatus(this.statusLine, 'Análisis completado con éxito.', 'ok');
    }catch(e){
      setStatus(this.statusLine, e.message || 'Ocurrió un error al procesar la solicitud.', 'error');
    }finally{
      this.genBtn.disabled = false;
      this.genBtn.textContent = original;
    }
  }
}

document.querySelectorAll('.audio-card').forEach(el => new AudioGenCard(el));
document.querySelectorAll('.json-card').forEach(el => new JsonCard(el));

// ---------- Tabs: un endpoint por tab ----------
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const name = btn.dataset.tab;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b === btn));
    document.querySelectorAll('.tab-panel').forEach(panel => {
      const isActive = panel.dataset.tabPanel === name;
      panel.classList.toggle('active', isActive);
      if(isActive && panel.__card) panel.__card.fitCanvas();
    });
  });
});
</script>
</body>
</html>
"""
