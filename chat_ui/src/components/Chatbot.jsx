import { useState } from 'react';
import { useImmer } from 'use-immer';
import api from '@/api';
import ChatMessages from '@/components/ChatMessages';
import ChatInput from '@/components/ChatInput';

function Chatbot({dark_mode, setDarkMode}) {
  const [messages, setMessages] = useImmer([]);
  const [newMessage, setNewMessage] = useState('');

  const isLoading = messages.length && messages[messages.length - 1].loading;

  async function submitNewMessage() {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage || isLoading) return;

    setMessages(draft => [...draft,
      { role: 'user', content: trimmedMessage },
      { role: 'assistant', content: '', sources: [], loading: true }
    ]);

    setNewMessage('');

    try {
      const model_response = await api.sendChatMessage(trimmedMessage);

      setMessages(draft => {
        draft[draft.length - 1].loading = false;
      });
      setMessages(draft => {
        draft[draft.length - 1].content += model_response.response;
      });

    } catch (err) {
      console.log(err);
      setMessages(draft => {
        draft[draft.length - 1].loading = false;
        draft[draft.length - 1].error = true;
      });
    }
  }

  let text_style = dark_mode ? 'mt-3 font-urbanist text-white text-xl font-light space-y-2' : 'mt-3 font-urbanist text-black text-xl font-light space-y-2';
  return (
    <div className='relative grow flex flex-col gap-6 pt-6'>
      {messages.length === 0 &&
          <div className={text_style}>
            <p>Приветствую! Я - AI-ассистент, который умеет изменять дизайн сайта на любой вкус.</p>
            <p>Просто напишите URL сайта, который вы хотите преобразить, и опишите как должен выглядеть результат. (:</p>
            <p>P.S. Для корректной работы ассистента запрос должен быть в формате &#34;URL-ссылка + Запрос с описанием желаемых изменений исходного ресурса&#34;</p>
          </div>
      }
      <ChatMessages
          messages={messages}
          isLoading={isLoading}
          dark_mode={dark_mode}
        setDarkMode={setDarkMode}
      />
      <ChatInput
        newMessage={newMessage}
        isLoading={isLoading}
        setNewMessage={setNewMessage}
        submitNewMessage={submitNewMessage}
        dark_mode={dark_mode}
        setDarkMode={setDarkMode}
      />
    </div>
  );
}

export default Chatbot;