import {ChatBox, Content, Header} from './pages'
import {ReactNode, useState} from "react";
import {analyze, sendMessage} from "./functions/api.ts";

export type Message = {
  text: string | ReactNode,
  isUser: boolean,
}


function App() {

  const [messages, setMessages] = useState<Message[]>([])


  const onSendMessage = async (message: string) => {
    const sendingMessage: Message = {
      text: 'Sending message...',
      isUser: false
    };

    setMessages((messages) => [...messages,
      {
        text: message,
        isUser: true
      },
      sendingMessage]);

    const response = await sendMessage(message);
    sendingMessage.text = response.response;
    setMessages((messages) => [...messages]);
  }

  const onAnalyze = async (jd: string) => {
    const sendingMessage: Message = {
      text: 'Analyzing your resume...',
      isUser: false
    };

    setMessages((messages) => [...messages,
      {
        text: 'Analyze my resume based on the following job description:\n' + jd,
        isUser: true
      },
      sendingMessage]);

    // handle message sent, update conversation section
    const response = await analyze(jd);
    if (null === response) {
      sendingMessage.text = "Something went wrong, please try again later."
    } else {
      const analysis = response.analysis;
      sendingMessage.text = (
        <>
          <div className="font-bold">Analysis Result:</div>
          {
            Object.keys(analysis.explanations).map(key => (
              <>
                <div className="font-bold" key={key}>
                  {key}: {analysis.explanations[key].score}
                </div>
                <div>
                  {analysis.explanations[key].explanation}
                </div>
                <br/>
              </>
            ))
          }
          <div className="font-bold">Total Score:
            {Object.values(analysis.scores).reduce((acc, cur) => acc + cur, 0)}</div>
        </>
      );
    }
    setMessages((messages) => [...messages]);
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
