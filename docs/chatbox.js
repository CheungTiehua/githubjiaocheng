/* GitHub 中文教程 — 智能助教聊天框 */

(function () {
  const API = '/api/chat';
  let history = [];
  let open = false;

  // ── 构建 DOM ──
  const container = document.createElement('div');
  container.className = 'chatbox-container';
  container.innerHTML = `
    <button class="chatbox-btn" id="chatbox-toggle" title="智能助教">💬</button>
    <div class="chatbox-window" id="chatbox-window">
      <div class="chatbox-header">
        <span class="title">智能助教 <span class="subtitle">DeepSeek · 课程问答</span></span>
        <button class="chatbox-close" id="chatbox-close">✕</button>
      </div>
      <div class="chatbox-messages" id="chatbox-messages">
        <div class="chat-msg assistant">你好！我是本课程的智能助教。<br>可以问我 GitHub 相关的任何问题，比如：<br>• Fork 和 Clone 有什么区别？<br>• 怎么创建 PR？<br>• Merge conflict 怎么解决？</div>
      </div>
      <div class="chat-typing" id="chatbox-typing"><span class="dot">●</span><span class="dot">●</span><span class="dot">●</span></div>
      <div class="chatbox-input-area">
        <textarea id="chatbox-input" rows="1" placeholder="输入问题..." onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();document.getElementById('chatbox-send').click()}"></textarea>
        <button class="chatbox-send" id="chatbox-send">发送</button>
      </div>
    </div>`;
  document.body.appendChild(container);

  const toggle = document.getElementById('chatbox-toggle');
  const windowEl = document.getElementById('chatbox-window');
  const close = document.getElementById('chatbox-close');
  const messages = document.getElementById('chatbox-messages');
  const typing = document.getElementById('chatbox-typing');
  const input = document.getElementById('chatbox-input');
  const send = document.getElementById('chatbox-send');

  toggle.addEventListener('click', () => {
    open = !open;
    windowEl.classList.toggle('open', open);
    if (open) setTimeout(() => input.focus(), 100);
  });
  close.addEventListener('click', () => {
    open = false;
    windowEl.classList.remove('open');
  });

  function addMsg(role, text) {
    const div = document.createElement('div');
    div.className = `chat-msg ${role}`;
    div.innerHTML = text.replace(/\n/g, '<br>');
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  // 简单的 Markdown → HTML（粗体、代码、列表）
  function simpleMd(text) {
    return text
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\n/g, '<br>');
  }

  send.addEventListener('click', async () => {
    const q = input.value.trim();
    if (!q) return;
    input.value = '';
    addMsg('user', simpleMd(q));
    history.push({ role: 'user', content: q });

    send.disabled = true;
    typing.classList.add('active');
    messages.scrollTop = messages.scrollHeight;

    try {
      const resp = await fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: q,
          history: history.slice(-10),
        }),
      });
      const data = await resp.json();
      typing.classList.remove('active');

      if (data.error) {
        addMsg('assistant', '抱歉，出了点问题：' + data.error);
      } else {
        const reply = data.reply || '（无回复）';
        addMsg('assistant', simpleMd(reply));
        history.push({ role: 'assistant', content: reply });
      }
    } catch (e) {
      typing.classList.remove('active');
      addMsg('assistant', '网络请求失败，请稍后再试。');
    }
    send.disabled = false;
    input.focus();
  });
})();
