/* BMSCE Chatbot - Desktop Premium Script */

// ===== STATE =====
const chatTabs = [{ id: 1, name: 'Chat 1', messages: [], el: null }];
let activeTab = 1;
let tabCounter = 1;
let queryCount = 0;
let trustStats = { official: 0, verified: 0, opinion: 0, total: 0 };
let messageHistory = [];
let historyIndex = -1;
const popQCounts = {};

// ===== DOM =====
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const scrollBtn = document.getElementById('scrollBtn');
const toast = document.getElementById('toast');
const tabBar = document.getElementById('tabBar');
const searchOverlay = document.getElementById('searchOverlay');
const searchInput = document.getElementById('searchInput');
const searchCount = document.getElementById('searchCount');

// ===== PARTICLE BACKGROUND =====
(function initParticles() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let w, h, particles = [];
    function resize() { w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight; }
    resize(); window.addEventListener('resize', resize);
    for (let i = 0; i < 60; i++) {
        particles.push({ x: Math.random() * w, y: Math.random() * h, r: Math.random() * 1.5 + 0.5,
            dx: (Math.random() - 0.5) * 0.3, dy: (Math.random() - 0.5) * 0.3, o: Math.random() * 0.3 + 0.1 });
    }
    function draw() {
        ctx.clearRect(0, 0, w, h);
        particles.forEach(p => {
            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(99,102,241,${p.o})`; ctx.fill();
            p.x += p.dx; p.y += p.dy;
            if (p.x < 0 || p.x > w) p.dx *= -1;
            if (p.y < 0 || p.y > h) p.dy *= -1;
        });
        requestAnimationFrame(draw);
    }
    draw();
})();

// ===== PARALLAX =====
document.addEventListener('mousemove', (e) => {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;
    const x = (e.clientX / window.innerWidth - 0.5) * 10;
    const y = (e.clientY / window.innerHeight - 0.5) * 10;
    canvas.style.transform = `translate(${x}px, ${y}px)`;
});

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); userInput.focus(); }
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') { e.preventDefault(); addNewTab(); }
    if ((e.ctrlKey || e.metaKey) && e.key === 'e') { e.preventDefault(); exportChat(); }
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') { e.preventDefault(); toggleSearch(); }
    if (e.key === 'Escape') { closeSearch(); userInput.value = ''; userInput.blur(); }
});

userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    if (e.ctrlKey && e.key === 'ArrowUp') { e.preventDefault(); cycleMsgHistory(-1); }
    if (e.ctrlKey && e.key === 'ArrowDown') { e.preventDefault(); cycleMsgHistory(1); }
});

userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
});

chatMessages.addEventListener('scroll', () => {
    const diff = chatMessages.scrollHeight - chatMessages.scrollTop - chatMessages.clientHeight;
    scrollBtn.classList.toggle('visible', diff > 150);
});

function scrollToBottom() { chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' }); }

// ===== MESSAGE HISTORY CYCLING =====
function cycleMsgHistory(dir) {
    if (!messageHistory.length) return;
    historyIndex = Math.max(0, Math.min(messageHistory.length - 1, historyIndex + dir));
    userInput.value = messageHistory[historyIndex];
}

// ===== TOAST =====
function showToast(text) {
    toast.textContent = text;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2200);
}

// ===== DESKTOP NOTIFICATIONS =====
function requestNotifPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}
requestNotifPermission();

function showNotification(title, body) {
    if ('Notification' in window && Notification.permission === 'granted' && document.hidden) {
        new Notification(title, { body: body.substring(0, 100), icon: '' });
    }
}

// ===== RICH TEXT RENDERING =====
function renderRichText(text) {
    let h = text;
    h = h.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    // Bold: **text** or __text__
    h = h.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    h = h.replace(/__(.+?)__/g, '<strong>$1</strong>');
    // Inline code
    h = h.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Line breaks
    h = h.replace(/\n/g, '<br>');
    // Bullet points: lines starting with - or •
    h = h.replace(/(^|<br>)([-•]\s)/g, '$1<span style="color:var(--accent-light)">$2</span>');
    return h;
}

// ===== TIME HELPER =====
function getTime() {
    return new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

// ===== ADD USER MESSAGE =====
function addUserMsg(text) {
    const div = document.createElement('div');
    div.className = 'msg-row user';
    div.innerHTML = `<div class="msg-card user-card"><div class="bubble-content">${renderRichText(text)}</div><div class="user-time">${getTime()}</div></div>`;
    chatMessages.appendChild(div);
    scrollToBottom();
    // Store in tab
    const tab = chatTabs.find(t => t.id === activeTab);
    if (tab) tab.messages.push({ type: 'user', text, time: getTime() });
}

// ===== ADD BOT MESSAGE =====
function addBotMsg(data) {
    const trustLabels = { 1: 'Official', 2: 'Verified', 3: 'Opinion' };
    const trustClass = `t${data.trust_level || 1}`;
    const label = trustLabels[data.trust_level] || 'Info';
    const source = data.source || 'BMSCE Bot';
    const time = getTime();

    const div = document.createElement('div');
    div.className = 'msg-row bot';
    div.innerHTML = `<div class="msg-card bot-card">
        <div class="bot-card-header">
            <span class="source-chip">${source}<span class="tooltip">Source: ${source}</span></span>
            <span class="trust-pill ${trustClass}">${label}</span>
        </div>
        <div class="bot-card-body">${renderRichText(data.response)}</div>
        <div class="bot-card-footer">
            <span class="msg-time">${time}</span>
            <div class="card-actions">
                <button class="card-action-btn" onclick="copyWithSource(this)">Copy</button>
                <button class="card-action-btn" onclick="copyRaw(this)">Raw</button>
            </div>
        </div>
    </div>`;
    chatMessages.appendChild(div);
    scrollToBottom();
    showNotification('BMSCE Bot', data.response);

    // Store in tab and update stats
    const tab = chatTabs.find(t => t.id === activeTab);
    if (tab) tab.messages.push({ type: 'bot', data, time });
    updateTrustStats(data.trust_level);
}

// ===== COPY FUNCTIONS =====
function copyWithSource(btn) {
    const card = btn.closest('.bot-card');
    const body = card.querySelector('.bot-card-body').innerText;
    const source = card.querySelector('.source-chip').childNodes[0].textContent.trim();
    const trust = card.querySelector('.trust-pill').textContent.trim();
    const time = card.querySelector('.msg-time').textContent;
    const full = `${body}\n\n--- Source: ${source} | Trust: ${trust} | Time: ${time} ---`;
    navigator.clipboard.writeText(full).then(() => { btn.textContent = 'Copied!'; showToast('Copied with source'); setTimeout(() => btn.textContent = 'Copy', 1500); });
}

function copyRaw(btn) {
    const card = btn.closest('.bot-card');
    const text = card.querySelector('.bot-card-body').innerText;
    navigator.clipboard.writeText(text).then(() => { btn.textContent = 'Done!'; showToast('Raw text copied'); setTimeout(() => btn.textContent = 'Raw', 1500); });
}

// ===== TYPING INDICATOR =====
function showTyping() {
    let el = document.getElementById('typingEl');
    if (!el) { el = document.createElement('div'); el.id = 'typingEl'; el.className = 'typing-indicator active'; el.innerHTML = '<span></span><span></span><span></span>'; chatMessages.appendChild(el); }
    else el.classList.add('active');
    scrollToBottom();
}
function hideTyping() { const el = document.getElementById('typingEl'); if (el) el.remove(); }

// ===== SEND MESSAGE =====
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    const wc = document.querySelector('.welcome-container');
    if (wc) wc.remove();

    messageHistory.push(text);
    historyIndex = messageHistory.length;
    addUserMsg(text);
    userInput.value = '';
    userInput.style.height = 'auto';
    sendBtn.disabled = true;
    showTyping();

    try {
        const res = await fetch('/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: text }) });
        const data = await res.json();
        hideTyping();
        if (data.error) addBotMsg({ response: 'Error: ' + data.error, trust_level: 1, source: 'System' });
        else { addBotMsg(data); queryCount++; updateStats(); }
    } catch (err) {
        hideTyping();
        addBotMsg({ response: 'Connection error. Is the server running?', trust_level: 1, source: 'System' });
    }
    sendBtn.disabled = false;
    userInput.focus();
}

function askQuick(text) { userInput.value = text; sendMessage(); }

// ===== CHAT TABS =====
function renderTabs() {
    let html = '';
    chatTabs.forEach(t => {
        const active = t.id === activeTab ? 'active' : '';
        const closeBtn = chatTabs.length > 1 ? `<span class="close-tab" onclick="event.stopPropagation();closeTab(${t.id})">&times;</span>` : '';
        html += `<button class="chat-tab ${active}" onclick="switchTab(${t.id})">${t.name}${closeBtn}</button>`;
    });
    html += `<button class="new-tab-btn" onclick="addNewTab()" title="New Chat (Ctrl+N)">+</button>`;
    tabBar.innerHTML = html;
}

function addNewTab() {
    tabCounter++;
    const newTab = { id: tabCounter, name: `Chat ${tabCounter}`, messages: [] };
    chatTabs.push(newTab);
    switchTab(tabCounter);
    showToast(`Chat ${tabCounter} opened`);
}

function switchTab(id) {
    // Save current scroll
    activeTab = id;
    renderTabs();
    // Rebuild chat messages
    chatMessages.innerHTML = '';
    const tab = chatTabs.find(t => t.id === id);
    if (!tab || tab.messages.length === 0) {
        chatMessages.innerHTML = `<div class="welcome-container"><div class="welcome-emoji">&#127963;</div><h2>BMSCE Campus Assistant</h2><p>Ask me anything about BMS College of Engineering.</p></div>`;
    } else {
        tab.messages.forEach(m => {
            if (m.type === 'user') addUserMsg(m.text);
            else addBotMsg(m.data);
        });
    }
    scrollBtn.innerHTML = '<button class="scroll-bottom-btn" id="scrollBtn" onclick="scrollToBottom()">&#8595;</button>';
}

function closeTab(id) {
    const idx = chatTabs.findIndex(t => t.id === id);
    if (idx === -1 || chatTabs.length <= 1) return;
    chatTabs.splice(idx, 1);
    if (activeTab === id) activeTab = chatTabs[0].id;
    switchTab(activeTab);
}

// ===== EXPORT CHAT =====
function exportChat() {
    const tab = chatTabs.find(t => t.id === activeTab);
    if (!tab || tab.messages.length === 0) { showToast('No messages to export'); return; }
    // JSON export
    const jsonData = {
        name: tab.name,
        exported: new Date().toISOString(),
        messages: tab.messages.map(m => m.type === 'user'
            ? { role: 'user', text: m.text, time: m.time }
            : { role: 'bot', response: m.data.response, source: m.data.source, trust_level: m.data.trust_level, time: m.time }
        )
    };
    const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `bmsce-chat-${tab.name.replace(/\s/g, '-')}.json`;
    a.click();
    showToast('Chat exported as JSON!');
}

// ===== LOCAL STORAGE PERSISTENCE =====
function saveState() {
    try {
        const state = { chatTabs, activeTab, tabCounter, queryCount, trustStats, popQCounts, messageHistory };
        localStorage.setItem('bmsce_chat_state', JSON.stringify(state));
    } catch (e) { /* storage full or unavailable */ }
}

function loadState() {
    try {
        const raw = localStorage.getItem('bmsce_chat_state');
        if (!raw) return;
        const state = JSON.parse(raw);
        if (state.chatTabs && state.chatTabs.length) {
            chatTabs.length = 0;
            state.chatTabs.forEach(t => chatTabs.push(t));
            activeTab = state.activeTab || chatTabs[0].id;
            tabCounter = state.tabCounter || chatTabs.length;
            queryCount = state.queryCount || 0;
            trustStats = state.trustStats || trustStats;
            Object.assign(popQCounts, state.popQCounts || {});
            messageHistory.push(...(state.messageHistory || []));
            historyIndex = messageHistory.length;
            switchTab(activeTab);
            updateStats();
            updatePopQCounters();
            const fill = document.getElementById('trustMeterFill');
            const lbl = document.getElementById('trustMeterPct');
            const pct = trustStats.total ? Math.round((trustStats.official / trustStats.total) * 100) : 0;
            if (fill) fill.style.width = pct + '%';
            if (lbl) lbl.textContent = pct + '% Official';
        }
    } catch (e) { /* ignore parse errors */ }
}

// Auto-save after every message
const _origAddBotMsg = addBotMsg;
const _origAddUserMsg = addUserMsg;
window._saveAfterMsg = () => setTimeout(saveState, 100);


// ===== SEARCH IN CHAT =====
function toggleSearch() {
    searchOverlay.classList.toggle('active');
    if (searchOverlay.classList.contains('active')) { searchInput.focus(); searchInput.value = ''; }
    else clearHighlights();
}
function closeSearch() { searchOverlay.classList.remove('active'); clearHighlights(); }

searchInput?.addEventListener('input', () => {
    clearHighlights();
    const q = searchInput.value.trim().toLowerCase();
    if (!q) { searchCount.textContent = ''; return; }
    const bodies = chatMessages.querySelectorAll('.bot-card-body, .bubble-content');
    let count = 0;
    bodies.forEach(el => {
        const html = el.innerHTML;
        const regex = new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        if (regex.test(el.textContent)) {
            el.innerHTML = html.replace(regex, '<span class="search-highlight">$1</span>');
            count++;
        }
    });
    searchCount.textContent = count ? `${count} found` : 'No matches';
});

function clearHighlights() {
    chatMessages.querySelectorAll('.search-highlight').forEach(el => {
        const parent = el.parentNode;
        parent.replaceChild(document.createTextNode(el.textContent), el);
        parent.normalize();
    });
    if (searchCount) searchCount.textContent = '';
}

// ===== STATS & TRUST METER =====
function updateStats() {
    const el = document.getElementById('statQueries');
    if (el) el.textContent = queryCount;
}

function updateTrustStats(level) {
    trustStats.total++;
    if (level === 1) trustStats.official++;
    else if (level === 2) trustStats.verified++;
    else trustStats.opinion++;
    const pct = trustStats.total ? Math.round((trustStats.official / trustStats.total) * 100) : 0;
    const fill = document.getElementById('trustMeterFill');
    const lbl = document.getElementById('trustMeterPct');
    if (fill) fill.style.width = pct + '%';
    if (lbl) lbl.textContent = pct + '% Official';
}

// ===== POPULAR QUESTIONS COUNTER =====
const origAskQuick = askQuick;
window.askQuick = function(text) {
    popQCounts[text] = (popQCounts[text] || 0) + 1;
    updatePopQCounters();
    origAskQuick(text);
};

function updatePopQCounters() {
    document.querySelectorAll('.pop-q-item').forEach(el => {
        const q = el.getAttribute('data-q');
        const countEl = el.querySelector('.pop-q-count');
        if (q && countEl && popQCounts[q]) countEl.textContent = popQCounts[q];
    });
}

// ===== RESIZABLE COLUMNS =====
function initResizer(resizerId, targetEl, side) {
    const resizer = document.getElementById(resizerId);
    if (!resizer || !targetEl) return;
    let startX, startW;
    resizer.addEventListener('mousedown', (e) => {
        startX = e.clientX;
        startW = targetEl.offsetWidth;
        resizer.classList.add('active');
        document.addEventListener('mousemove', onMove);
        document.addEventListener('mouseup', onUp);
        e.preventDefault();
    });
    function onMove(e) {
        const diff = e.clientX - startX;
        const newW = side === 'left' ? startW + diff : startW - diff;
        if (newW > 180 && newW < 450) targetEl.style.width = newW + 'px';
    }
    function onUp() {
        resizer.classList.remove('active');
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
    }
}

// ===== DRAG & DROP =====
function initDragDrop() {
    const area = chatMessages;
    const dz = document.getElementById('dropZone');
    if (!area || !dz) return;
    ['dragenter', 'dragover'].forEach(ev => area.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.add('active'); }));
    ['dragleave', 'drop'].forEach(ev => dz.addEventListener(ev, () => dz.classList.remove('active')));
    area.addEventListener('drop', (e) => {
        e.preventDefault(); dz.classList.remove('active');
        const file = e.dataTransfer.files[0];
        if (!file || !file.name.endsWith('.txt')) { showToast('Only .txt files supported'); return; }
        const reader = new FileReader();
        reader.onload = (ev) => {
            const preview = ev.target.result.substring(0, 500);
            addUserMsg(`[Dropped file: ${file.name}]\n${preview}${ev.target.result.length > 500 ? '\n...(truncated)' : ''}`);
        };
        reader.readAsText(file);
    });
}

// ===== NAV =====
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');
    });
});

// ===== THEME TOGGLE =====
document.getElementById('themeToggle')?.addEventListener('click', function () {
    this.classList.toggle('active');
    showToast(this.classList.contains('active') ? 'Dark mode active' : 'Light mode (coming soon)');
});

// ===== TRENDING BARS ANIMATE =====
window.addEventListener('load', () => {
    document.querySelectorAll('.trend-bar-fill').forEach(bar => {
        const w = bar.getAttribute('data-width');
        setTimeout(() => { bar.style.width = w; }, 400);
    });
    renderTabs();
    loadState();
    const left = document.querySelector('.sidebar-left');
    const right = document.querySelector('.sidebar-right');
    initResizer('resizerLeft', left, 'left');
    initResizer('resizerRight', right, 'right');
    initDragDrop();
});

// Intercept sendMessage completion to auto-save
const _origSend = sendMessage;
window.sendMessage = async function() {
    await _origSend();
    saveState();
};

