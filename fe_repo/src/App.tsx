import {ChatBox, Content, Header} from './pages'
import {useState} from "react";
import {analyze, sendMessage} from "./functions/api.ts";

export type Message = {
  text: string,
  isUser: boolean,
}

function App() {

  const [messages, setMessages] = useState<Message[]>([])

  const onSendMessage = (message: string) => {
    const sendingMessage = {
      text: 'Sending message...',
      isUser: false
    };

    setMessages((messages) => [...messages,
      {
        text: message,
        isUser: true
      },
      sendingMessage]);

    setTimeout(() => {
      // handle message sent, update conversation section
      // const response = {text: sendMessage(message), isUser: false}
      // remove sending prompt message
      sendingMessage.text = sendMessage(message);
      setMessages((messages) => [...messages]);
    }, 1000);
  }

  const onAnalyze = (jd: string) => {
    const sendingMessage = {
      text: 'Analyzing your resume...',
      isUser: false
    };

    setMessages((messages) => [...messages,
      {
        text: 'Analyze my resume based on the following job description:\n' + jd,
        isUser: true
      },
      sendingMessage]);

    setTimeout(() => {
      // handle message sent, update conversation section
      // const response = {text: sendMessage(message), isUser: false}
      // remove sending prompt message
      sendingMessage.text = analyze(jd);
      setMessages((messages) => [...messages]);
    }, 1000);
  }

  return (
    <div className="flex flex-col h-screen bg-gray-100 p-5">
      <Header/>
      <Content messages={messages}></Content>
      <ChatBox onSendMessage={onSendMessage} onAnalyze={onAnalyze}></ChatBox>
    </div>
  )
}

export default App
