DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI-Powered Website Link Analysis | Live Demo</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    code, pre { font-family: 'JetBrains Mono', monospace; }
    .glass { background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
    .glass-card { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.08); }
    .glow { box-shadow: 0 0 40px -10px rgba(59, 130, 246, 0.3); }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col antialiased selection:bg-blue-600 selection:text-white">

  <header class="border-b border-slate-800/80 sticky top-0 z-50 glass">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 flex items-center justify-center font-extrabold text-white text-lg shadow-lg shadow-blue-500/20">
          AI
        </div>
        <div>
          <span class="font-bold text-lg text-white tracking-tight">LinkIntel</span>
          <span class="text-xs px-2 py-0.5 ml-2 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">Gemini 2.5 Flash</span>
        </div>
      </div>
      <div class="flex items-center space-x-3">
        <a href="/docs" target="_blank" class="px-3.5 py-1.5 rounded-lg text-sm font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center space-x-1.5">
          <span>Swagger Docs</span>
          <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
        </a>
        <a href="https://github.com/Samar-111/AI-Powered-Website-Link-Analysis-API" target="_blank" class="px-3.5 py-1.5 rounded-lg text-sm font-semibold bg-blue-600 hover:bg-blue-500 text-white transition shadow-sm flex items-center space-x-1.5">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
          <span>GitHub</span>
        </a>
      </div>
    </div>
  </header>

  <main class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full">
    <div class="text-center max-w-3xl mx-auto mb-10">
      <h1 class="text-4xl sm:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-100 to-slate-400 tracking-tight mb-4">
        AI-Powered Website Link Analysis
      </h1>
      <p class="text-slate-400 text-base sm:text-lg">
        Submit any website URL to extract deep business overview, competitor intelligence, search discovery queries, technical SEO improvements, and target audience personas using Gemini 2.5 Flash.
      </p>
    </div>

    <div class="max-w-3xl mx-auto glass rounded-2xl p-6 sm:p-8 glow mb-10">
      <form id="analyzeForm" class="space-y-4">
        <div>
          <label for="urlInput" class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Target Website URL</label>
          <div class="flex flex-col sm:flex-row gap-3">
            <div class="relative flex-1">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
              </div>
              <input type="text" id="urlInput" required placeholder="https://stripe.com" value="https://stripe.com" class="w-full pl-11 pr-4 py-3 bg-slate-900 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm">
            </div>
            <button type="submit" id="submitBtn" class="px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-sm transition shadow-lg shadow-blue-500/25 flex items-center justify-center space-x-2 disabled:opacity-50">
              <span id="btnText">Analyze Website</span>
              <svg id="btnSpinner" class="hidden animate-spin w-4 h-4 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg>
            </button>
          </div>
        </div>
        <div class="flex items-center space-x-2 text-xs text-slate-400 pt-1">
          <span>Quick test:</span>
          <button type="button" onclick="setUrl('https://stripe.com')" class="px-2.5 py-1 rounded-md bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700/60 transition">Stripe</button>
          <button type="button" onclick="setUrl('https://shopify.com')" class="px-2.5 py-1 rounded-md bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700/60 transition">Shopify</button>
          <button type="button" onclick="setUrl('https://notion.so')" class="px-2.5 py-1 rounded-md bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700/60 transition">Notion</button>
          <button type="button" onclick="setUrl('https://github.com')" class="px-2.5 py-1 rounded-md bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700/60 transition">GitHub</button>
        </div>
      </form>
    </div>

    <div id="loadingIndicator" class="hidden max-w-xl mx-auto py-12 text-center">
      <div class="inline-flex p-4 rounded-2xl bg-blue-500/10 text-blue-400 mb-4 animate-pulse">
        <svg class="w-8 h-8 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg>
      </div>
      <h3 class="text-lg font-bold text-white mb-1">Analyzing Website Content</h3>
      <p class="text-sm text-slate-400">Fetching HTML, parsing page structure, and generating 5 sections of intelligence via Gemini 2.5 Flash...</p>
    </div>

    <div id="errorAlert" class="hidden max-w-3xl mx-auto p-4 mb-8 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm flex items-start space-x-3">
      <svg class="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      <div>
        <p class="font-semibold text-red-200">Analysis Failed</p>
        <p id="errorText" class="mt-1 text-xs text-red-300"></p>
      </div>
    </div>

    <div id="resultsContainer" class="hidden space-y-8">
      <div class="glass rounded-2xl p-6 sm:p-8">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6 mb-6">
          <div>
            <div class="flex items-center space-x-3">
              <h2 id="resBrandName" class="text-3xl font-extrabold text-white tracking-tight"></h2>
              <span id="resCategoryBadge" class="text-xs px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-semibold"></span>
            </div>
            <p id="resWebsiteUrl" class="text-xs text-slate-400 mt-1 font-mono"></p>
          </div>
          <div id="resMetadata" class="flex flex-wrap gap-2 text-xs text-slate-400"></div>
        </div>
        <p id="resBrandSummary" class="text-slate-300 text-sm leading-relaxed mb-6"></p>
        <div>
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2">Core Products & Services</span>
          <div id="resProductsList" class="flex flex-wrap gap-2"></div>
        </div>
      </div>

      <div class="border-b border-slate-800 flex overflow-x-auto gap-2">
        <button onclick="switchTab('competitors')" class="tab-btn px-4 py-2.5 text-sm font-semibold border-b-2 border-blue-500 text-blue-400 transition" data-tab="competitors">1. Competitors</button>
        <button onclick="switchTab('queries')" class="tab-btn px-4 py-2.5 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition" data-tab="queries">2. Search Queries</button>
        <button onclick="switchTab('seo')" class="tab-btn px-4 py-2.5 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition" data-tab="seo">3. SEO Improvements</button>
        <button onclick="switchTab('services')" class="tab-btn px-4 py-2.5 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition" data-tab="services">4. Top 5 Services</button>
        <button onclick="switchTab('audience')" class="tab-btn px-4 py-2.5 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition" data-tab="audience">5. Target Audience</button>
        <button onclick="switchTab('rawjson')" class="tab-btn px-4 py-2.5 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 transition" data-tab="rawjson">Raw JSON</button>
      </div>

      <div id="tab-competitors" class="tab-content space-y-6">
        <div id="competitorCards" class="grid grid-cols-1 md:grid-cols-3 gap-5"></div>
        <div class="glass rounded-xl p-6">
          <h3 class="text-base font-bold text-white mb-4">Competitor Comparison Matrix</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border-collapse">
              <thead>
                <tr class="border-b border-slate-800 text-slate-400 font-semibold uppercase">
                  <th class="py-3 px-4">Aspect</th>
                  <th class="py-3 px-4 text-blue-400">Your Brand</th>
                  <th class="py-3 px-4 text-indigo-400">Competitor</th>
                </tr>
              </thead>
              <tbody id="comparisonTableBody" class="divide-y divide-slate-800/60 text-slate-300"></tbody>
            </table>
          </div>
        </div>
      </div>

      <div id="tab-queries" class="tab-content hidden space-y-4">
        <div id="queriesList" class="grid grid-cols-1 md:grid-cols-2 gap-4"></div>
      </div>

      <div id="tab-seo" class="tab-content hidden space-y-6">
        <div class="glass-card rounded-xl p-6">
          <h4 class="text-xs uppercase font-bold text-slate-400 tracking-wider mb-2">Google Search Snippet Preview</h4>
          <div class="p-4 bg-slate-900 rounded-lg border border-slate-800">
            <div id="seoPreviewUrl" class="text-xs text-slate-400 font-mono mb-0.5"></div>
            <div id="seoPreviewTitle" class="text-blue-400 font-medium text-base hover:underline cursor-pointer"></div>
            <div id="seoPreviewDesc" class="text-xs text-slate-300 mt-1 line-clamp-2"></div>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div class="glass rounded-xl p-5">
            <h4 class="text-xs uppercase font-bold text-slate-400 tracking-wider mb-3">Keyword Architecture</h4>
            <div class="space-y-3 text-xs">
              <div>
                <span class="text-slate-500 block">Primary Keyword</span>
                <span id="seoPrimaryKeyword" class="font-bold text-white text-sm"></span>
              </div>
              <div>
                <span class="text-slate-500 block mb-1">Secondary Keywords</span>
                <div id="seoSecondaryKeywords" class="flex flex-wrap gap-1.5"></div>
              </div>
              <div>
                <span class="text-slate-500 block mb-1">Long-Tail Keywords</span>
                <div id="seoLongTailKeywords" class="flex flex-wrap gap-1.5"></div>
              </div>
            </div>
          </div>
          <div class="glass rounded-xl p-5">
            <h4 class="text-xs uppercase font-bold text-slate-400 tracking-wider mb-3">Recommended Supporting Content</h4>
            <ul id="seoSupportingContent" class="space-y-2 text-xs text-slate-300 list-disc list-inside"></ul>
          </div>
        </div>
      </div>

      <div id="tab-services" class="tab-content hidden">
        <div id="servicesList" class="grid grid-cols-1 md:grid-cols-2 gap-5"></div>
      </div>

      <div id="tab-audience" class="tab-content hidden space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div class="glass rounded-xl p-5">
            <h4 class="text-xs uppercase font-bold text-slate-400 tracking-wider mb-2">Primary Segments</h4>
            <div id="audiencePrimary" class="flex flex-wrap gap-1.5"></div>
          </div>
          <div class="glass rounded-xl p-5">
            <h4 class="text-xs uppercase font-bold text-slate-400 tracking-wider mb-2">Target Industries</h4>
            <div id="audienceIndustries" class="flex flex-wrap gap-1.5"></div>
          </div>
          <div class="glass rounded-xl p-5">
            <h4 class="text-xs uppercase font-bold text-slate-400 tracking-wider mb-2">Business Types</h4>
            <div id="audienceBusinessTypes" class="flex flex-wrap gap-1.5"></div>
          </div>
        </div>
        <div class="glass rounded-xl p-6">
          <h4 class="text-xs uppercase font-bold text-slate-400 tracking-wider mb-4">Customer Needs & Pain Points</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <span class="text-emerald-400 font-semibold block mb-2">Core Needs:</span>
              <ul id="audienceNeeds" class="space-y-1.5 text-slate-300 list-disc list-inside"></ul>
            </div>
            <div>
              <span class="text-rose-400 font-semibold block mb-2">Challenges / Gaps:</span>
              <ul id="audienceChallenges" class="space-y-1.5 text-slate-300 list-disc list-inside"></ul>
            </div>
          </div>
        </div>
      </div>

      <div id="tab-rawjson" class="tab-content hidden">
        <div class="relative glass rounded-xl p-4">
          <button onclick="copyJson()" class="absolute top-4 right-4 px-3 py-1 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg text-slate-300 border border-slate-700 transition">Copy JSON</button>
          <pre id="rawJsonBlock" class="text-xs text-emerald-400 overflow-x-auto max-h-[600px] p-2 leading-relaxed"></pre>
        </div>
      </div>
    </div>
  </main>

  <footer class="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
    <p>AI-Powered Website Link Analysis API</p>
  </footer>

  <script>
    let currentData = null;

    function setUrl(url) {
      document.getElementById('urlInput').value = url;
    }

    function switchTab(tabName) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('border-blue-500', 'text-blue-400');
        btn.classList.add('border-transparent', 'text-slate-400');
      });
      document.getElementById('tab-' + tabName).classList.remove('hidden');
      const activeBtn = document.querySelector(`[data-tab="${tabName}"]`);
      if (activeBtn) {
        activeBtn.classList.remove('border-transparent', 'text-slate-400');
        activeBtn.classList.add('border-blue-500', 'text-blue-400');
      }
    }

    function copyJson() {
      if (currentData) {
        navigator.clipboard.writeText(JSON.stringify(currentData, null, 2));
        alert('JSON copied to clipboard!');
      }
    }

    document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const url = document.getElementById('urlInput').value.trim();
      if (!url) return;

      const submitBtn = document.getElementById('submitBtn');
      const btnText = document.getElementById('btnText');
      const btnSpinner = document.getElementById('btnSpinner');
      const loading = document.getElementById('loadingIndicator');
      const errorAlert = document.getElementById('errorAlert');
      const errorText = document.getElementById('errorText');
      const resultsContainer = document.getElementById('resultsContainer');

      errorAlert.classList.add('hidden');
      resultsContainer.classList.add('hidden');
      loading.classList.remove('hidden');
      submitBtn.disabled = true;
      btnText.textContent = 'Analyzing...';
      btnSpinner.classList.remove('hidden');

      try {
        const response = await fetch('/link-analysis', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: url })
        });
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || data.error || 'Server returned error ' + response.status);
        }

        currentData = data;
        renderResults(data);
        resultsContainer.classList.remove('hidden');
      } catch (err) {
        errorText.textContent = err.message;
        errorAlert.classList.remove('hidden');
      } finally {
        loading.classList.add('hidden');
        submitBtn.disabled = false;
        btnText.textContent = 'Analyze Website';
        btnSpinner.classList.add('hidden');
      }
    });

    function renderResults(data) {
      document.getElementById('resBrandName').textContent = data.brand.name || 'Identified Brand';
      document.getElementById('resCategoryBadge').textContent = data.brand.category || 'Business';
      document.getElementById('resWebsiteUrl').textContent = data.website;
      document.getElementById('resBrandSummary').textContent = data.brand.summary || '';

      const productsList = document.getElementById('resProductsList');
      productsList.innerHTML = '';
      (data.brand.main_products_and_services || []).forEach(p => {
        const span = document.createElement('span');
        span.className = 'text-xs px-2.5 py-1 rounded-md bg-slate-800 text-slate-300 border border-slate-700/80';
        span.textContent = p;
        productsList.appendChild(span);
      });

      const metaEl = document.getElementById('resMetadata');
      metaEl.innerHTML = '';
      if (data.metadata) {
        metaEl.innerHTML = `
          <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">Model: ${data.metadata.model_used || 'Gemini'}</span>
          <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">Latency: ${data.metadata.response_time_seconds || '0'}s</span>
          <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">Tokens: ${data.metadata.total_tokens || '0'}</span>
        `;
      }

      const compCards = document.getElementById('competitorCards');
      compCards.innerHTML = '';
      (data.analysis.competitor_analysis.competitors || []).forEach(c => {
        const card = document.createElement('div');
        card.className = 'glass-card rounded-xl p-5 flex flex-col justify-between';
        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-bold text-white text-base">${c.brand_name}</h4>
              <span class="text-[10px] px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">Competitor</span>
            </div>
            <p class="text-xs text-slate-400 mb-3"><strong class="text-slate-300">Service:</strong> ${c.main_service}</p>
            <p class="text-xs text-slate-400 mb-3"><strong class="text-slate-300">Target:</strong> ${c.target_market}</p>
            <div class="space-y-2 text-xs">
              <div class="text-emerald-400"><strong>Strength:</strong> ${c.key_strength}</div>
              <div class="text-rose-400"><strong>Weakness/Gap:</strong> ${(c.weaknesses_or_gaps || []).join(', ') || 'N/A'}</div>
            </div>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-800/80 text-[11px] text-amber-300/90">
            <strong>Opportunity:</strong> ${c.opportunity}
          </div>
        `;
        compCards.appendChild(card);
      });

      const tableBody = document.getElementById('comparisonTableBody');
      tableBody.innerHTML = '';
      (data.analysis.competitor_analysis.comparison_matrix || []).forEach(row => {
        const tr = document.createElement('tr');
        tr.className = 'border-b border-slate-800/40 hover:bg-slate-900/40 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-4 font-medium text-slate-300">${row.aspect}</td>
          <td class="py-2.5 px-4 text-slate-200 font-semibold">${row.your_brand}</td>
          <td class="py-2.5 px-4 text-slate-400">${row.competitor}</td>
        `;
        tableBody.appendChild(tr);
      });

      const queriesList = document.getElementById('queriesList');
      queriesList.innerHTML = '';
      (data.analysis.target_search_queries || []).forEach((q, idx) => {
        const item = document.createElement('div');
        item.className = 'glass-card rounded-xl p-5';
        const platformBadges = (q.platforms || []).map(p => `<span class="text-[10px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">${p}</span>`).join(' ');
        item.innerHTML = `
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-mono text-slate-500">#0${idx + 1}</span>
            <div class="flex gap-1">${platformBadges}</div>
          </div>
          <h4 class="font-bold text-white text-base mb-2">"${q.query}"</h4>
          <div class="space-y-1.5 text-xs text-slate-400">
            <p><strong class="text-slate-300">Intent:</strong> <span class="text-cyan-400">${q.intent}</span></p>
            <p><strong class="text-slate-300">Target Audience:</strong> ${q.target_audience}</p>
            <p class="pt-1 text-slate-300 text-[11px]">${q.business_relevance}</p>
          </div>
        `;
        queriesList.appendChild(item);
      });

      const seo = data.analysis.seo_improvements;
      document.getElementById('seoPreviewUrl').textContent = data.website;
      document.getElementById('seoPreviewTitle').textContent = seo.recommended_title || data.brand.name;
      document.getElementById('seoPreviewDesc').textContent = seo.meta_description || '';
      document.getElementById('seoPrimaryKeyword').textContent = seo.primary_keyword;

      const secKw = document.getElementById('seoSecondaryKeywords');
      secKw.innerHTML = (seo.secondary_keywords || []).map(k => `<span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">${k}</span>`).join('');

      const ltKw = document.getElementById('seoLongTailKeywords');
      ltKw.innerHTML = (seo.long_tail_keywords || []).map(k => `<span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">${k}</span>`).join('');

      const supContent = document.getElementById('seoSupportingContent');
      supContent.innerHTML = (seo.supporting_content || []).map(c => `<li>${c}</li>`).join('');

      const servicesList = document.getElementById('servicesList');
      servicesList.innerHTML = '';
      (data.analysis.top_services || []).forEach(s => {
        const div = document.createElement('div');
        div.className = 'glass-card rounded-xl p-5';
        const tag = s.is_inferred 
          ? `<span class="text-[10px] px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">Inferred</span>`
          : `<span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Extracted</span>`;
        div.innerHTML = `
          <div class="flex items-center justify-between mb-2">
            <h4 class="font-bold text-white text-base">${s.service_name}</h4>
            ${tag}
          </div>
          <p class="text-xs text-slate-300 mb-3">${s.description}</p>
          <div class="space-y-1 text-xs text-slate-400 pt-2 border-t border-slate-800/60">
            <p><strong class="text-slate-300">Target Industry:</strong> ${s.target_industry}</p>
            <p><strong class="text-slate-300">Target Customer:</strong> ${s.target_customer}</p>
            <p class="text-cyan-300 font-medium mt-1"><strong>Benefit:</strong> ${s.main_benefit}</p>
          </div>
        `;
        servicesList.appendChild(div);
      });

      const aud = data.analysis.target_audience;
      document.getElementById('audiencePrimary').innerHTML = (aud.primary_audience || []).map(a => `<span class="px-2.5 py-1 rounded-md bg-blue-500/10 text-blue-300 border border-blue-500/20 text-xs">${a}</span>`).join('');
      document.getElementById('audienceIndustries').innerHTML = (aud.industries || []).map(i => `<span class="px-2.5 py-1 rounded-md bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 text-xs">${i}</span>`).join('');
      document.getElementById('audienceBusinessTypes').innerHTML = (aud.business_types || []).map(b => `<span class="px-2.5 py-1 rounded-md bg-slate-800 text-slate-300 border border-slate-700 text-xs">${b}</span>`).join('');

      document.getElementById('audienceNeeds').innerHTML = (aud.customer_needs || []).map(n => `<li>${n}</li>`).join('');
      document.getElementById('audienceChallenges').innerHTML = (aud.customer_challenges || []).map(c => `<li>${c}</li>`).join('');

      document.getElementById('rawJsonBlock').textContent = JSON.stringify(data, null, 2);
    }
  </script>
</body>
</html>
"""
