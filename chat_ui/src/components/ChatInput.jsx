import useAutosize from '@/hooks/useAutosize';
import sendIcon from '@/assets/images/send.svg';

function ChatInput({ newMessage, isLoading, setNewMessage, submitNewMessage, dark_mode, setDarkMode }) {
  const textareaRef = useAutosize(newMessage);

  function handleKeyDown(e) {
    if(e.keyCode === 13 && !e.shiftKey && !isLoading) {
      e.preventDefault();
      submitNewMessage();
    }
  }


  let input_style = dark_mode ? 'sticky bottom-10 shrink-0 py- bg-3b3c3a' : 'sticky bottom-10 shrink-0 bg-white py-';
  let d_1_style = dark_mode ? 'pr-0.5 relative shrink-0 rounded-3xl overflow-hidden bg-black ring-primary-blue ring-1 focus-within:ring-2 transition-all' : 'pr-0.5 relative shrink-0 rounded-3xl overflow-hidden ring-primary-blue ring-1 focus-within:ring-2 transition-all'
  let d_2_style = dark_mode ? 'block w-full max-h-[140px] py-2 px-4 pr-11 bg-black rounded-3xl resize-none text-white placeholder:leading-4 placeholder:-translate-y-1 sm:placeholder:leading-normal sm:placeholder:translate-y-0 focus:outline-none' :
      'block w-full max-h-[140px] py-2 px-4 pr-11 rounded-3xl resize-none text-black placeholder:leading-4 placeholder:-translate-y-1 sm:placeholder:leading-normal sm:placeholder:translate-y-0 focus:outline-none'
  return(
    <div className={input_style}>
      <div className='p-1.5 bg-primary-blue/35 rounded-3xl z-50 font-mono origin-bottom animate-chat duration-400'>
        <div className={d_1_style}>
          <textarea
            className= {d_2_style}
            ref={textareaRef}
            rows='1'
            value={newMessage}
            onChange={e => setNewMessage(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            className='absolute top-1/2 -translate-y-1/2 right-3 p-1 rounded-md hover:bg-primary-blue/20'
            onClick={submitNewMessage}
          >
            <img src={sendIcon} alt='send' />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatInput;