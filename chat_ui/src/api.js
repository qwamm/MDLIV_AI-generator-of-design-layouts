const BASE_URL = 'http://localhost';

async function sendChatMessage(message) {
  const url_pattern = 'https?:\\/\\/[^\\s]+'
  let url_regex = new RegExp(url_pattern)
  let url = message.match(url_regex)
  let prompt = message.replace(url_regex, '')
  prompt = prompt[0] === ' ' ? prompt.substring(1) : prompt
  prompt = prompt[prompt.length - 1] === ' ' ? prompt.substring(0, prompt.length - 1) : prompt

  if (!url[0])
  {
    alert("Incorrect prompt without source site url")
    throw new Error("Request prompt is invalid")
  }
  const res = await fetch(BASE_URL + `/api/design/redesign`, {
    method: 'POST',
    headers: {
          'Content-Type': 'application/json'
    },
    body: JSON.stringify({ 'url':  url[0], 'prompt': prompt})
  });
  if (!res.ok) {
    return Promise.reject({ status: res.status, data: await res.json() });
  }
  return res.json();
}

export default {
   sendChatMessage
};