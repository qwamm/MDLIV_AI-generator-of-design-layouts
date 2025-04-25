import Chatbot from '@/components/Chatbot';
import React from "react";
import sun_logo from '@/assets/images/sun.svg'
import crescent_logo from '@/assets/images/crescent.svg'

function App() {

    const [dark_mode, setDarkMode] = React.useState(false);

    function toggle_mode(e) {
        console.log(dark_mode)
        setDarkMode(!dark_mode);
        document.body.classList.toggle('dark-mode');
    }

    let bg = dark_mode ? 'bg-black' : 'bg-white';
    let button_text = dark_mode ? 'Switch to light mode' : 'Switch to dark mode';
    let btn_logo = dark_mode ? crescent_logo : sun_logo
    let title_style = dark_mode ? 'font-urbanist text-[1.65rem] font-semibold text-lime-400' : 'font-urbanist text-[1.65rem] font-semibold text-red-900'
  return (
    <div className='flex flex-col min-h-full w-full max-w-3xl mx-auto px-4'>
        <header className={'sticky top-0 shrink-0 z-20' + bg}>
            <div className='h-full w-full gap-1 pt-4 pb-2 flex items-stretch space-x-80'>
                <h1 className={title_style}>Web Design Wizard</h1>
                <button type="button" onClick={toggle_mode}
                        className={"text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700 flex items-center gap-2"}>
                    <img src={btn_logo} alt="sun"></img>
                    {button_text}
                </button>
            </div>
        </header>
        <Chatbot dark_mode = {dark_mode} setDarkMode={setDarkMode} />
    </div>
  );
}

export default App;