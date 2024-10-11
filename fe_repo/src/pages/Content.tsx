import {useEffect, useRef} from "react";
import {Message} from "../App";

interface IContentProps {
  messages: Message[];
}

export const Content = ({messages}: IContentProps) => {
  const contentRef = useRef<HTMLDivElement>(document.createElement('div'));

  useEffect(() => {
    if (contentRef.current) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div
      className="border-2 p-4 flex-1 overflow-y-auto bg-white rounded-lg shadow-md mb-5"
      ref={contentRef}
    >
      {messages.map((msg, index) => (
        <div
          key={index}
          /* set user's message to right and others to left */
          style={{
            padding: '8px',
            display: 'flex',
            justifyContent: msg.isUser ? 'flex-end' : 'flex-start',
          }}
        >
          <div
            className="max-w-xs p-2 rounded-lg w-full"
            style={{
              padding: '8px',
              borderRadius: '12px',
              backgroundColor: msg.isUser ? '#3498db' : '#A8E6A1',
              color: msg.isUser ? 'white' : 'black',
            }}
          >
            {msg.text}
          </div>
        </div>
      ))}
    </div>
  )
}

