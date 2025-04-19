const chatContainer = document.getElementById('chatContainer')
const userInput = document.getElementById('userInput')
const sendButton = document.querySelector('.input-container button')

function splitIntoLines(text, maxLength) {
  const chunks = []
  let remainingText = text
  while (remainingText.length > maxLength) {
    let splitIndex = remainingText.lastIndexOf(' ', maxLength)
    if (splitIndex === -1 || splitIndex === 0) {
      splitIndex = maxLength
    }
    if (splitIndex > remainingText.length) {
      splitIndex = remainingText.length
    }
    chunks.push(remainingText.slice(0, splitIndex).trim())
    remainingText = remainingText
      .slice(splitIndex === maxLength ? splitIndex : splitIndex + 1)
      .trim()
  }
  if (remainingText.trim()) {
    chunks.push(remainingText.trim())
  }
  return chunks
}

function addMessageToChat({ text, sender, buttons }) {
  const messageWrapper = document.createElement('div')
  messageWrapper.className = `message-wrapper ${sender}`

  const messageContent = document.createElement('div')
  messageContent.className = 'message-content'

  const authorName = document.createElement('div')
  authorName.className = 'author-name'
  authorName.textContent = sender === 'user' ? 'Вы' : 'Умнопёс'

  const messageBubble = document.createElement('div')
  messageBubble.className = `message ${sender}-message`
  messageBubble.innerHTML = splitIntoLines(text, 30).join('<br>')

  messageContent.append(authorName, messageBubble)

  if (buttons && Array.isArray(buttons)) {
    const buttonsContainer = document.createElement('div')
    buttonsContainer.className = 'message-buttons'
    buttons.forEach(({ text, value }) => {
      const btn = document.createElement('button')
      btn.className = 'message-button'
      btn.textContent = text
      btn.dataset.value = value
      btn.addEventListener('click', () => {
        userInput.value = btn.dataset.value
        userInput.focus()
      })
      buttonsContainer.appendChild(btn)
    })
    messageContent.appendChild(buttonsContainer)
  }

  if (sender === 'bot') {
    const botAvatar = document.createElement('img')
    botAvatar.className = 'avatar'
    botAvatar.src = 'static/img/avatar.png'
    botAvatar.alt = 'Аватар бота'
    messageWrapper.append(botAvatar, messageContent)
  } else {
    messageWrapper.appendChild(messageContent)
  }

  chatContainer.appendChild(messageWrapper)
  setTimeout(() => {
    chatContainer.scrollTop = chatContainer.scrollHeight
  }, 50)
}

async function sendMessage() {
  const text = userInput.value.trim()
  if (!text) return

  addMessageToChat({ text, sender: 'user' })
  userInput.value = ''
  sendButton.disabled = true
  sendButton.classList.add('disabled', 'cooldown')

  try {
    const resp = await fetch('/api/requests/match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: text })
    })
    if (!resp.ok) throw new Error(resp.statusText)
    const data = await resp.json()
//    const answer = data[0]?.answer || 'Извините, не удалось найти ответ.'
    const score = data[0]?.score
    if (score < 0.7) {
        addMessageToChat({ text: 'Не можем найти ответ, попробуйте перефразировать запрос', sender: 'bot' })
    } else {
      const answer = data[0]?.answer || 'Извините, не удалось найти ответ.'
      addMessageToChat({ text: answer, sender: 'bot' })
    }
  } catch {
    addMessageToChat({ text: 'Ошибка сети, попробуйте ещё раз.', sender: 'bot' })
  } finally {
    sendButton.disabled = false
    sendButton.classList.remove('disabled', 'cooldown')
    userInput.focus()
  }
}

userInput.addEventListener('keypress', e => {
  if (e.key === 'Enter' && !e.shiftKey && !sendButton.disabled) {
    e.preventDefault()
    sendMessage()
  }
})

sendButton.addEventListener('click', () => {
  if (!sendButton.disabled) sendMessage()
})

document.addEventListener('DOMContentLoaded', () => {
  addMessageToChat({
    text: 'Привет! Я ваш Чат-бот. Чем я могу вам помочь сегодня? Выберите опцию:',
    sender: 'bot',
    buttons: [
      { text: 'Узнать о сервисе', value: 'Расскажи мне о сервисе' },
      { text: 'Посмотреть новости', value: 'Покажи последние новости' },
      { text: 'Задать другой вопрос', value: 'У меня другой вопрос...' }
    ]
  })
  userInput.focus()
})
