/**
 * Cloudflare Pages Function — DeepSeek 代理
 * POST /api/chat
 * 环境变量: DEEPSEEK_API_KEY (必填), DEEPSEEK_MODEL (可选, 默认 deepseek-chat)
 */

interface Env {
  DEEPSEEK_API_KEY: string;
  DEEPSEEK_MODEL?: string;
  TAVILY_API_KEY?: string;
}

interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface ChatRequest {
  message: string;
  history?: ChatMessage[];
}

const SYSTEM_PROMPT = `你是"GitHub 中文手把手教程"的智能助教。你的职责是帮助中文用户理解和使用 GitHub。

课程内容覆盖 15 节课:
01-注册与设置 / 02-读代码-仓库主页 / 03-读代码-文件与历史 / 04-Issue基础 / 05-Issue高级 / 06-PR-Fork与Clone / 07-PR创建 / 08-PR生命周期与合并 / 09-Code Review / 10-Actions-CI概念 / 11-Actions-日志 / 12-项目管理-Projects / 13-Wiki-Release / 14-安全与权限 / 15-附录速查

规则:
1. 用中文回答
2. 简洁直接，每次回复控制在 300 字以内
3. 涉及 GitHub 界面操作时，先说"点击哪里"，再说"会怎样"
4. 如果问题超出课程范围，礼貌告知并建议用户查阅相关文档
5. 可以引用课程中的术语和概念`;

export async function onRequestPost({ request, env }: { request: Request; env: Env }) {
  // CORS
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  }

  if (!env.DEEPSEEK_API_KEY) {
    return json({ error: 'API key 未配置。请在 Cloudflare 环境变量中设置 DEEPSEEK_API_KEY。' }, 500);
  }

  let body: ChatRequest;
  try {
    body = await request.json();
  } catch {
    return json({ error: '无效的 JSON 请求体' }, 400);
  }

  const { message, history = [] } = body;
  if (!message || typeof message !== 'string') {
    return json({ error: '请提供 message 字段' }, 400);
  }

  const model = env.DEEPSEEK_MODEL || 'deepseek-chat';
  const messages: ChatMessage[] = [
    { role: 'system', content: SYSTEM_PROMPT },
    ...history.slice(-10),
    { role: 'user', content: message },
  ];

  try {
    const resp = await fetch('https://api.deepseek.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${env.DEEPSEEK_API_KEY}`,
      },
      body: JSON.stringify({
        model,
        messages,
        max_tokens: 600,
        temperature: 0.7,
      }),
    });

    if (!resp.ok) {
      const errText = await resp.text();
      return json({ error: `DeepSeek API 错误 (${resp.status}): ${errText.slice(0, 200)}` }, resp.status);
    }

    const data = await resp.json() as any;
    const reply = data.choices?.[0]?.message?.content || '（空回复）';

    return json({ reply }, 200);
  } catch (e: any) {
    return json({ error: `请求失败: ${e.message}` }, 500);
  }
}

// 处理非 POST 请求
export async function onRequest(context: any) {
  if (context.request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  }
  if (context.request.method !== 'POST') {
    return json({ error: '仅支持 POST 请求' }, 405);
  }
  return onRequestPost(context);
}

function json(data: any, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
  });
}
